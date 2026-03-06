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
    mainfile_name_re = r'.*\\.(csv|xlsx)$'
    mainfile_contents_re = 'FAKE_HEADER'
    mainfile_mime_re = 'text/csv'
    mainfile_binary_header = ''
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
        'nomad_plugins_metadata.extractor.extract._is_github_repo_archived',
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
    assert 'auxiliary.json' in parser_details['auxiliary_file_patterns']

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
        'nomad_plugins_metadata.extractor.extract._is_github_repo_archived',
        lambda repository_url: True,
    )

    generated = build_generated_metadata_with_release_context(
        repo_path=repo,
        release_tag=None,
        release_sha=None,
    )
    assert generated['maturity'] == 'archived'
