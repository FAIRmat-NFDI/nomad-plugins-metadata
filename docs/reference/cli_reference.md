# CLI and API Reference

## CLI

Command:

```bash
nomad-plugin-metadata extract [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `--repo-path` | `Path` | `.` |  |
| `--manual-path` | `Path` | `.metadata/nomad_plugin_metadata.manual.yaml` |  |
| `--auto-path` | `Path` | `.metadata/nomad_plugin_metadata.auto.yaml` |  |
| `--effective-path` | `Path` | `nomad_plugin_metadata.yaml` |  |
| `--report-path` | `Path` | `.metadata/plugin-metadata.override-report.yaml` |  |
| `--release-tag` | `str` | `` | Release tag to embed in generated/effective metadata. |
| `--release-sha` | `str` | `` | Release commit SHA to embed in generated/effective metadata. |
| `--create-manual-template-if-missing, --no-create-manual-template-if-missing` | `bool flag` | `True` | Create .metadata/nomad_plugin_metadata.manual.yaml template when manual file is missing. |

## API (Docstrings)

This section is generated from Python docstrings.

### `ExtractRunConfig`

Runtime configuration for one extraction run.

### `run_extract`

Generate auto metadata and materialize merged/report artifacts.

The resulting precedence is deterministic:
non-empty manual values override generated values.

### `build_parser`

Build the CLI argument parser for `nomad-plugin-metadata`.

### `main`

CLI entrypoint.

### `build_generated_metadata`

Generate baseline metadata from repo-local static sources.

### `build_generated_metadata_with_release_context`

Generate baseline metadata from repo-local and discoverable plugin sources.

Sources include:
- `pyproject.toml` project metadata and entry-point declarations
- installed `nomad.plugin` entry points from the target package
- optional `CITATION.cff` / `citation.cff`
- best-effort repository API lookups (GitHub)

### `merge_generated_and_manual`

Merge plugin metadata with deterministic `manual > generated` precedence.
