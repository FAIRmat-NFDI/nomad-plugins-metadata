# `.metadata/` metadata artifact

This directory contains workflow-managed metadata artifacts from `nomad-plugin-metadata extract`.

## File and meaning

- `nomad_plugin_metadata.manual.yaml`
  - Maintainer-owned override/template file.
  - Created automatically if missing.
- `nomad_plugin_metadata.auto.yaml`
  - Machine-generated baseline metadata.
- `plugin-metadata.override-report.yaml`
  - Conflict report between machine-generated `auto` metadata and non-empty maintainer values from `manual`.
  - Contains only conflicting fields.
  - Rewritten on each extraction run (not appended).

## Editing rules

- Do not edit `.metadata/plugin-metadata.override-report.yaml` manually.
- Maintainer edits belong in `.metadata/nomad_plugin_metadata.manual.yaml`.

## Reset note

- Removing files under `.metadata/` resets manual/auto/report artifacts.
- Effective metadata remains at repository root: `nomad_plugin_metadata.yaml`.
