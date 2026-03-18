# `nomad-plugins-metadata`

Canonical schema and tooling package for generating, validating, and merging NOMAD plugin metadata.

## What this package is for

`nomad-plugins-metadata` is the shared foundation for plugin metadata across:

- plugin repositories (metadata authoring + automated extraction),
- `nomad-plugins` ingestion (transitional adapter mapping),
- `nomad-docs` registry rendering and filtering.

The package standardizes both metadata structure and automation behavior so plugin metadata is reproducible across repositories.

## Metadata model at a glance

- Manual metadata: `.metadata/nomad_plugin_metadata.manual.yaml`
- Auto metadata: `.metadata/nomad_plugin_metadata.auto.yaml`
- Effective metadata (consumer-facing): `nomad_plugin_metadata.yaml`
- Override report: `.metadata/plugin-metadata.override-report.yaml`

Merge precedence is deterministic:

non-empty values from `.metadata/nomad_plugin_metadata.manual.yaml` > `.metadata/nomad_plugin_metadata.auto.yaml`

## Core capabilities

- Canonical LinkML schema definition.
- NOMAD metainfo adapter classes.
- Metadata extraction CLI for plugin repositories.
- Deterministic merge contract: manual metadata overrides generated metadata.
- Override report generation for fields blocked by manual edits.
- Reusable GitHub Actions workflow for repository-level automation.

## Tooling artifacts

- Schema: `src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml`
- Metainfo adapter: `src/nomad_plugins_metadata/schema_packages/schema_package.py`
- Datatractor mapping: `src/nomad_plugins_metadata/schema_packages/datatractor_mapping.md`
- NOMAD adapter mapping: `src/nomad_plugins_metadata/adapters/nomad_mapping.md`
- Examples: `src/nomad_plugins_metadata/examples/`

## Where to go next

- See [How-to: Install This Plugin](how_to/install_this_plugin.md).
- See [How-to: Use This Plugin](how_to/use_this_plugin.md).
- See [How-to: Apply To Plugin Repo](how_to/apply_to_plugin_repo.md).
- See [Explanation](explanation/explanation.md) for architecture rationale.
- See [Reference: CLI and API](reference/cli_reference.md).
- See [Reference: Schema](reference/schema_reference.md).
