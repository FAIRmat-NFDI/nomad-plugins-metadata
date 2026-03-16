from pathlib import Path

from nomad_plugins_metadata.extractor.extract import (
    build_generated_metadata_with_release_context,
)


class _FakeDist:
    def __init__(self, name: str):
        self.name = name


class _FakeEntryPoint:
    def __init__(self, name: str, value: str, dist_name: str, loaded: object):
        self.name = name
        self.value = value
        self.dist = _FakeDist(dist_name)
        self._loaded = loaded

    def load(self):
        return self._loaded


class _FakeParserEntryPoint:
    entry_point_type = 'parser'
    id = 'parsers/fake-parser'
    name = 'Fake Parser'
    description = 'Parses fake files'
    level = 2
    aliases = ['fake', 'fake-parser']
    mainfile_name_re = r'.*\\.(csv|xlsx)$'
    mainfile_contents_re = 'FAKE_HEADER'
    mainfile_contents_dict = {'__has_all_keys': ['time', 'value']}
    mainfile_mime_re = 'text/csv'
    mainfile_binary_header = b'CSV'
    mainfile_binary_header_re = b'CSV.*'
    mainfile_alternative = False
    supported_compressions = ['gz', 'xz']
    metadata = {
        'tableOfFiles': '\n'.join(
            [
                '| Input Filename | Description |',
                '| --- | --- |',
                '| `main.csv` | **Mainfile** |',
                '| `auxiliary.json` | Auxiliary file |',
            ]
        )
    }


def test_extracts_installed_entry_point_parser_metadata(
    tmp_path: Path, monkeypatch
) -> None:
    parser_level = 2
    repo = tmp_path / 'repo'
    repo.mkdir()
    (repo / 'pyproject.toml').write_text(
        '\n'.join(
            [
                '[project]',
                'name = "example-plugin"',
                'version = "1.2.3"',
                '',
                'dependencies = ["numpy>=1.26", "pandas"]',
                '',
                '[project.entry-points."nomad.plugin"]',
                'fake_parser = "example.parsers:fake_parser"',
            ]
        ),
        encoding='utf-8',
    )

    fake_eps = [
        _FakeEntryPoint(
            name='fake_parser',
            value='example.parsers:fake_parser',
            dist_name='example-plugin',
            loaded=_FakeParserEntryPoint(),
        )
    ]
    monkeypatch.setattr(
        'nomad_plugins_metadata.extractor.extract.metadata.entry_points',
        lambda group=None: fake_eps,
    )
    monkeypatch.setattr(
        'nomad_plugins_metadata.extractor.extract._fetch_github_repo_metadata',
        lambda repository_url: None,
    )

    generated = build_generated_metadata_with_release_context(
        repo_path=repo,
        release_tag='v1.2.3',
        release_sha='deadbeef',
    )

    assert generated['entry_points'][0]['entry_point_name'] == 'fake_parser'
    assert generated['entry_points'][0]['capability_type'] == 'parser'

    capability = generated['capabilities'][0]
    assert capability['capability_type'] == 'parser'
    parser_details = capability['parser_details']
    assert parser_details['mainfile_name_re'] == r'.*\\.(csv|xlsx)$'
    assert parser_details['compression_support'] == ['gz', 'xz']
    assert parser_details['parser_level'] == parser_level
    assert parser_details['parser_aliases'] == ['fake', 'fake-parser']
    assert parser_details['mainfile_contents_dict'] == '{"__has_all_keys": ["time", "value"]}'
    assert parser_details['mainfile_binary_header'] == '435356'
    assert parser_details['mainfile_binary_header_re'] == '4353562e2a'
    assert parser_details['mainfile_alternative'] is False
    assert 'auxiliary.json' in parser_details['auxiliary_file_patterns']
    assert '.json' in generated['supported_filetypes']
    assert any(
        entry.get('id') == 'json' and '.json' in entry.get('extensions', [])
        for entry in generated['file_format_support']
    )

    deps = {item['package_name']: item for item in generated['schema_dependencies']}
    assert deps['numpy']['version_range'] == '>=1.26'
    assert deps['pandas']['version_range'] == ''

    assert generated['release_context']['release_tag'] == 'v1.2.3'
    assert generated['release_context']['release_commit_sha'] == 'deadbeef'
    assert generated['maturity'] == 'stable'


def test_maturity_archived_precedence_over_version(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / 'repo'
    repo.mkdir()
    (repo / 'pyproject.toml').write_text(
        '\n'.join(
            [
                '[project]',
                'name = "example-plugin"',
                'version = "1.2.3"',
                '',
                '[project.urls]',
                'Repository = "https://github.com/example/repo"',
            ]
        ),
        encoding='utf-8',
    )
    monkeypatch.setattr(
        'nomad_plugins_metadata.extractor.extract._fetch_github_repo_metadata',
        lambda repository_url: {'archived': True},
    )

    generated = build_generated_metadata_with_release_context(
        repo_path=repo,
        release_tag=None,
        release_sha=None,
    )
    assert generated['maturity'] == 'archived'
    assert generated['archived'] is True


def test_documentation_and_homepage_fallbacks(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / 'repo'
    repo.mkdir()
    (repo / 'pyproject.toml').write_text(
        '\n'.join(
            [
                '[project]',
                'name = "example-plugin"',
                'version = "0.4.0"',
                '',
                '[project.urls]',
                'Repository = "https://github.com/example/repo"',
            ]
        ),
        encoding='utf-8',
    )
    monkeypatch.setattr(
        'nomad_plugins_metadata.extractor.extract._fetch_github_repo_metadata',
        lambda repository_url: None,
    )
    monkeypatch.setattr(
        'nomad_plugins_metadata.extractor.extract._check_github_pages_exists',
        lambda repository_url: 'https://example.github.io/repo/',
    )

    generated = build_generated_metadata_with_release_context(
        repo_path=repo,
        release_tag=None,
        release_sha=None,
    )

    assert generated['documentation'] == 'https://example.github.io/repo/'
    assert generated['homepage'] == 'https://github.com/example/repo'


def test_citation_cff_is_primary_for_authors(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / 'repo'
    repo.mkdir()
    (repo / 'pyproject.toml').write_text(
        '\n'.join(
            [
                '[project]',
                'name = "example-plugin"',
                'version = "0.4.0"',
                '',
                '[[project.maintainers]]',
                'name = "Pyproject Maintainer"',
                'email = "maintainer@example.org"',
                '',
                '[[project.authors]]',
                'name = "Pyproject Author"',
                'email = "pyproject@example.org"',
            ]
        ),
        encoding='utf-8',
    )
    (repo / 'CITATION.cff').write_text(
        '\n'.join(
            [
                'cff-version: 1.2.0',
                'authors:',
                '  - family-names: Doe',
                '    given-names: Jane',
                '    email: jane@example.org',
                '    affiliation: FAIRmat',
            ]
        ),
        encoding='utf-8',
    )
    monkeypatch.setattr(
        'nomad_plugins_metadata.extractor.extract._fetch_github_repo_metadata',
        lambda repository_url: None,
    )

    generated = build_generated_metadata_with_release_context(
        repo_path=repo,
        release_tag=None,
        release_sha=None,
    )

    assert generated['authors'] == [
        {
            'name': 'Jane Doe',
            'email': 'jane@example.org',
            'affiliation': 'FAIRmat',
        }
    ]
    assert generated['maintainers'] == [
        {'name': 'Pyproject Maintainer', 'email': 'maintainer@example.org'}
    ]
    assert any(
        p.get('source') == 'citation_cff'
        for p in generated.get('metadata_provenance', [])
    )


def test_citation_cff_url_fallbacks_for_repository_and_homepage(
    tmp_path: Path, monkeypatch
) -> None:
    repo = tmp_path / 'repo'
    repo.mkdir()
    (repo / 'pyproject.toml').write_text(
        '\n'.join(
            [
                '[project]',
                'name = "example-plugin"',
                'version = "0.4.0"',
            ]
        ),
        encoding='utf-8',
    )
    (repo / 'CITATION.cff').write_text(
        '\n'.join(
            [
                'cff-version: 1.2.0',
                "repository-code: 'https://github.com/example/repo'",
                "url: 'https://example.github.io/repo/'",
            ]
        ),
        encoding='utf-8',
    )
    monkeypatch.setattr(
        'nomad_plugins_metadata.extractor.extract._fetch_github_repo_metadata',
        lambda repository_url: None,
    )
    monkeypatch.setattr(
        'nomad_plugins_metadata.extractor.extract._check_github_pages_exists',
        lambda repository_url: None,
    )

    generated = build_generated_metadata_with_release_context(
        repo_path=repo,
        release_tag=None,
        release_sha=None,
    )

    assert generated['upstream_repository'] == 'https://github.com/example/repo'
    assert generated['homepage'] == 'https://example.github.io/repo/'
    assert 'documentation' not in generated
    assert any(
        p.get('source') == 'citation_cff'
        for p in generated.get('metadata_provenance', [])
    )


def test_github_telemetry_fields_are_extracted(tmp_path: Path, monkeypatch) -> None:
    stars_count = 42
    repo = tmp_path / 'repo'
    repo.mkdir()
    (repo / 'pyproject.toml').write_text(
        '\n'.join(
            [
                '[project]',
                'name = "example-plugin"',
                'version = "0.4.0"',
                '',
                '[project.urls]',
                'Repository = "https://github.com/example/repo"',
            ]
        ),
        encoding='utf-8',
    )
    monkeypatch.setattr(
        'nomad_plugins_metadata.extractor.extract._fetch_github_repo_metadata',
        lambda repository_url: {
            'stargazers_count': stars_count,
            'owner': {'login': 'example', 'type': 'Organization'},
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2025-01-01T00:00:00Z',
            'archived': False,
        },
    )

    generated = build_generated_metadata_with_release_context(
        repo_path=repo,
        release_tag=None,
        release_sha=None,
    )

    assert generated['stars'] == stars_count
    assert generated['owner'] == 'example'
    assert generated['owner_type'] == 'Organization'
    assert generated['created'] == '2024-01-01T00:00:00Z'
    assert generated['last_updated'] == '2025-01-01T00:00:00Z'
    assert generated['archived'] is False


class _FakeMimeOnlyParserEntryPoint:
    entry_point_type = 'parser'
    id = 'parsers/mime-only'
    name = 'MimeOnly Parser'
    description = 'Parses based on mime'
    mainfile_name_re = r'.*'
    mainfile_mime_re = 'application/x-custom'
    supported_compressions = []
    metadata = {}


def test_file_format_support_falls_back_to_specific_mime(
    tmp_path: Path, monkeypatch
) -> None:
    repo = tmp_path / 'repo'
    repo.mkdir()
    (repo / 'pyproject.toml').write_text(
        '\n'.join(
            [
                '[project]',
                'name = "example-plugin"',
                '',
                '[project.entry-points."nomad.plugin"]',
                'mime_parser = "example.parsers:mime_parser"',
            ]
        ),
        encoding='utf-8',
    )

    fake_eps = [
        _FakeEntryPoint(
            name='mime_parser',
            value='example.parsers:mime_parser',
            dist_name='example-plugin',
            loaded=_FakeMimeOnlyParserEntryPoint(),
        )
    ]
    monkeypatch.setattr(
        'nomad_plugins_metadata.extractor.extract.metadata.entry_points',
        lambda group=None: fake_eps,
    )
    monkeypatch.setattr(
        'nomad_plugins_metadata.extractor.extract._fetch_github_repo_metadata',
        lambda repository_url: None,
    )

    generated = build_generated_metadata_with_release_context(
        repo_path=repo,
        release_tag=None,
        release_sha=None,
    )
    assert generated['file_format_support'][0]['mime_types'] == ['application/x-custom']
    assert generated['file_format_support'][0]['id'] == 'application-x-custom'
