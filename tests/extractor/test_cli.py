from pathlib import Path

import yaml

from nomad_plugins_metadata.extractor.cli import run_extract


def test_run_extract_writes_generated_effective_and_report(tmp_path: Path):
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
                'Repository = "https://github.com/example/repo"',
            ]
        ),
        encoding='utf-8',
    )

    manual_path = repo / 'nomad_plugin_metadata.yaml'
    manual_path.write_text(
        'name: Manual Name\nmaturity: alpha\n',
        encoding='utf-8',
    )

    generated = repo / '.nomad/plugin-metadata.generated.yaml'
    effective = repo / '.nomad/plugin-metadata.effective.yaml'
    report = repo / '.nomad/plugin-metadata.override-report.yaml'

    run_extract(repo, manual_path, generated, effective, report)

    generated_data = yaml.safe_load(generated.read_text(encoding='utf-8'))
    effective_data = yaml.safe_load(effective.read_text(encoding='utf-8'))
    report_data = yaml.safe_load(report.read_text(encoding='utf-8'))

    assert generated_data['name'] == 'example-plugin'
    assert effective_data['name'] == 'Manual Name'
    assert effective_data['maturity'] == 'alpha'
    assert report_data['summary']['overridden_field_count'] >= 1
