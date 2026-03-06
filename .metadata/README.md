# `.metadata/` metadata artifact

This directory contains workflow-managed report output from `nomad-plugin-metadata extract`.

## File and meaning

- `plugin-metadata.override-report.yaml`
  - Conflict report between machine-generated `auto` metadata and non-empty maintainer values from `manual`.
  - Contains only conflicting fields.
  - Rewritten on each extraction run (not appended).

## Editing rules

- Do not edit `.metadata/plugin-metadata.override-report.yaml` manually.
- Maintainer edits belong in `nomad_plugin_metadata.manual.yaml`.

## Reset note

- Removing files under `.metadata/` resets only report artifacts.
- It does not reset `auto`, `manual`, or effective metadata files in repository root.
