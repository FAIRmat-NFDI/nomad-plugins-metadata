from pathlib import Path

import yaml

from nomad_plugins_metadata.extractor.cli import ExtractRunConfig, run_extract


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
    front = repo / 'nomad_plugin_metadata.yaml'

    run_extract(
        repo,
        ExtractRunConfig(
            manual_path=manual_path,
            generated_path=generated,
            effective_path=effective,
            report_path=report,
            release_tag='v0.3.0',
            release_sha='abc123',
            update_front_file=front,
        ),
    )

    generated_data = yaml.safe_load(generated.read_text(encoding='utf-8'))
    effective_data = yaml.safe_load(effective.read_text(encoding='utf-8'))
    report_data = yaml.safe_load(report.read_text(encoding='utf-8'))
    front_data = yaml.safe_load(front.read_text(encoding='utf-8'))

    assert generated_data['name'] == 'example-plugin'
    assert effective_data['name'] == 'Manual Name'
    assert effective_data['maturity'] == 'alpha'
    assert report_data['summary']['overridden_field_count'] >= 1
    assert generated_data['release_context']['release_tag'] == 'v0.3.0'
    assert generated_data['release_context']['release_commit_sha'] == 'abc123'
    assert effective_data['release_context']['release_tag'] == 'v0.3.0'
    assert front_data == effective_data


def test_run_extract_overwrites_existing_report(tmp_path: Path):
    repo = tmp_path / 'repo'
    repo.mkdir()
    (repo / 'pyproject.toml').write_text(
        '\n'.join(['[project]', 'name = "overwrite-test"']),
        encoding='utf-8',
    )
    manual_path = repo / 'nomad_plugin_metadata.yaml'
    manual_path.write_text('name: overwrite-test\\n', encoding='utf-8')
    generated = repo / '.nomad/plugin-metadata.generated.yaml'
    effective = repo / '.nomad/plugin-metadata.effective.yaml'
    report = repo / '.nomad/plugin-metadata.override-report.yaml'
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text('legacy: should disappear\\n', encoding='utf-8')

    run_extract(
        repo,
        ExtractRunConfig(
            manual_path=manual_path,
            generated_path=generated,
            effective_path=effective,
            report_path=report,
        ),
    )

    report_data = yaml.safe_load(report.read_text(encoding='utf-8'))
    assert 'legacy' not in report_data
    assert 'summary' in report_data
