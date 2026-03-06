# `nomad-plugins-metadata`

Canonical schema and tooling package for generating, validating, and merging NOMAD plugin metadata.

## What this package is for

`nomad-plugins-metadata` is the shared foundation for plugin metadata across:

- plugin repositories (metadata authoring + automated extraction),
- `nomad-plugins` ingestion (transitional adapter mapping),
- `nomad-docs` registry rendering and filtering.

The package standardizes both metadata structure and automation behavior so plugin metadata is reproducible across repositories.

## Core capabilities

- Canonical LinkML schema definition.
- NOMAD metainfo adapter classes.
- Metadata extraction CLI for plugin repositories.
- Deterministic merge contract: manual metadata overrides generated metadata.
- Override report generation for fields blocked by manual edits.
- Reusable GitHub Actions workflow for repository-level automation.

## Main artifacts

- Schema: `src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml`
- Metainfo adapter: `src/nomad_plugins_metadata/schema_packages/schema_package.py`
- Datatractor mapping: `src/nomad_plugins_metadata/schema_packages/datatractor_mapping.md`
- NOMAD adapter mapping: `src/nomad_plugins_metadata/adapters/nomad_mapping.md`
- Examples: `src/nomad_plugins_metadata/examples/`

## Typical plugin-repo flow

1. Maintainer edits `nomad_plugin_metadata.yaml` (manual override file).
2. CI runs `nomad-plugin-metadata extract`.
3. Workflow writes:
   - `.nomad/plugin-metadata.generated.yaml`
   - `.nomad/plugin-metadata.effective.yaml`
   - `.nomad/plugin-metadata.override-report.yaml`
4. In release PR mode, workflow also updates:
   - `nomad_plugin_metadata.yaml`
5. Consumers ingest effective metadata.

Merge precedence is always:

`nomad_plugin_metadata.yaml` > `.nomad/plugin-metadata.generated.yaml`

## Where to go next

- See [Tutorial](tutorial/tutorial.md) for end-to-end usage.
- See [Explanation](explanation/explanation.md) for architecture rationale.
- See [Reference](reference/references.md) for commands, files, and workflow inputs.
