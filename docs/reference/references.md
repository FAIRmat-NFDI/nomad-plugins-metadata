# Reference

## CLI

Command:

```sh
nomad-plugin-metadata extract [options]
```

Options:

- `--repo-path` (default: `.`)
- `--manual-path` (default: `nomad_plugin_metadata.yaml`)
- `--generated-path` (default: `.nomad/plugin-metadata.generated.yaml`)
- `--effective-path` (default: `.nomad/plugin-metadata.effective.yaml`)
- `--report-path` (default: `.nomad/plugin-metadata.override-report.yaml`)
- `--release-tag` (default: empty)
- `--release-sha` (default: empty)
- `--update-front-file` (default: unset)

Extractor behavior notes:

- Baseline metadata is read from `pyproject.toml`.
- Technical metadata is additionally read from installed `nomad.plugin` entry points
  (for example parser matcher fields and supported compressions).
- If plugin entry points are not installed/importable, extraction falls back to static
  `pyproject` entry-point declarations.

## Metadata files

- Manual override file:
  - `nomad_plugin_metadata.yaml`
- Generated file:
  - `.nomad/plugin-metadata.generated.yaml`
- Effective merged file:
  - `.nomad/plugin-metadata.effective.yaml`
- Override report:
  - `.nomad/plugin-metadata.override-report.yaml`
- Forward-facing file updated in release PR mode:
  - `nomad_plugin_metadata.yaml`

## Canonical schema and mappings

- LinkML schema:
  - `src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml`
- Datatractor mapping:
  - `src/nomad_plugins_metadata/schema_packages/datatractor_mapping.md`
- NOMAD adapter mapping:
  - `src/nomad_plugins_metadata/adapters/nomad_mapping.md`

## Reusable GitHub workflow

Workflow path:

- `.github/workflows/extract-plugin-metadata.yml`

Caller template:

- `docs/templates/update-plugin-metadata.yml`

Key workflow inputs:

- `package_spec`
- `install_repo_package`
- `install_repo_extras`
- `repo_path`
- `manual_path`
- `generated_path`
- `effective_path`
- `report_path`
- `release_tag`
- `release_sha`
- `forward_file_path`
- `create_pr`
- `pr_branch`
- `pr_title`
- `pr_body`
- `auto_commit`
- `check_only`
- `commit_message`
