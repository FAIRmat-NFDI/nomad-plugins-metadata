from pathlib import Path

import yaml

from nomad_plugins_metadata.extractor.cli import ExtractRunConfig, run_extract


def test_run_extract_writes_auto_effective_report_and_keeps_manual_file(tmp_path: Path):
    repo = tmp_path / 'repo'
    repo.mkdir()

    (repo / 'pyproject.toml').write_text(
        '\n'.join(
            [
                '[project]',
                'name = "example-plugin"',
                'version = "0.3.0"',
                'description = "Example plugin"',
                '',
                '[project.urls]',
                'Repository = "https://example.org/repo"',
            ]
        ),
        encoding='utf-8',
    )

    manual_path = repo / '.metadata/nomad_plugin_metadata.manual.yaml'
    manual_path.parent.mkdir(parents=True, exist_ok=True)
    manual_path.write_text(
        (
            'name: Manual Name\n'
            'maturity: alpha\n'
            'plugin_version: ""\n'
            'suggested_usages:\n'
            '  - id: ""\n'
            '    title: ""\n'
        ),
        encoding='utf-8',
    )

    auto_path = repo / '.metadata/nomad_plugin_metadata.auto.yaml'
    effective_path = repo / 'nomad_plugin_metadata.yaml'
    report_path = repo / '.metadata/plugin-metadata.override-report.yaml'

    run_extract(
        repo,
        ExtractRunConfig(
            manual_path=manual_path,
            auto_path=auto_path,
            effective_path=effective_path,
            report_path=report_path,
            release_tag='v0.3.0',
            release_sha='abc123',
        ),
    )

    auto_data = yaml.safe_load(auto_path.read_text(encoding='utf-8'))
    effective_data = yaml.safe_load(effective_path.read_text(encoding='utf-8'))
    report_data = yaml.safe_load(report_path.read_text(encoding='utf-8'))
    manual_after = yaml.safe_load(manual_path.read_text(encoding='utf-8'))

    assert auto_data['name'] == 'example-plugin'
    assert effective_data['name'] == 'Manual Name'
    # Empty manual value should not override generated value.
    assert effective_data['plugin_version'] == '0.3.0'
    # Empty placeholder list item should be ignored.
    assert 'suggested_usages' not in effective_data
    assert report_data['summary']['overridden_field_count'] >= 1
    assert auto_data['release_context']['release_tag'] == 'v0.3.0'
    assert auto_data['release_context']['release_commit_sha'] == 'abc123'
    # Manual file is maintainer-owned and not modified by extractor.
    assert manual_after['name'] == 'Manual Name'


def test_run_extract_creates_manual_template_if_missing(tmp_path: Path):
    repo = tmp_path / 'repo'
    repo.mkdir()
    (repo / 'pyproject.toml').write_text(
        '\n'.join(['[project]', 'name = "template-test"']),
        encoding='utf-8',
    )
    manual_path = repo / '.metadata/nomad_plugin_metadata.manual.yaml'
    auto_path = repo / '.metadata/nomad_plugin_metadata.auto.yaml'
    effective_path = repo / 'nomad_plugin_metadata.yaml'
    report_path = repo / '.metadata/plugin-metadata.override-report.yaml'

    run_extract(
        repo,
        ExtractRunConfig(
            manual_path=manual_path,
            auto_path=auto_path,
            effective_path=effective_path,
            report_path=report_path,
        ),
    )

    assert manual_path.exists()
    manual_data = yaml.safe_load(manual_path.read_text(encoding='utf-8'))
    assert 'subject' in manual_data
    assert 'deployment' in manual_data
    assert 'suggested_usages' in manual_data
    assert 'file_format_support' in manual_data
    assert 'name' not in manual_data
