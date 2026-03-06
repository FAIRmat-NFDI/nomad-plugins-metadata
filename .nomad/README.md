# `.nomad/` metadata artifacts

This directory is workflow-managed output from `nomad-plugin-metadata extract`.

## Files and meaning

- `plugin-metadata.generated.yaml`
  - Raw extractor output from repository introspection.
  - Machine-owned baseline.
  - Should not be manually edited.

- `plugin-metadata.effective.yaml`
  - Deterministic merge result used by downstream consumers.
  - Merge contract: manual metadata in `nomad_plugin_metadata.yaml` overrides generated metadata.
  - This is the resolved "what the registry should use" view.

- `plugin-metadata.override-report.yaml`
  - Warning/report file for merge conflicts where manual metadata blocked generated values.
  - Rewritten on each extraction run (not appended).

## Editing rules

- Edit `nomad_plugin_metadata.yaml` for curated/manual metadata.
- Do not edit files in `.nomad/` manually.
- Re-run extraction after plugin code or manual metadata changes.
