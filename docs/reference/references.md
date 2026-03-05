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

## Metadata files

- Manual override file:
  - `nomad_plugin_metadata.yaml`
- Generated file:
  - `.nomad/plugin-metadata.generated.yaml`
- Effective merged file:
  - `.nomad/plugin-metadata.effective.yaml`
- Override report:
  - `.nomad/plugin-metadata.override-report.yaml`

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
- `repo_path`
- `manual_path`
- `generated_path`
- `effective_path`
- `report_path`
- `auto_commit`
- `commit_message`
