# `nomad-plugins-metadata`

NOMAD-first schema and tooling package for generating, validating, and merging NOMAD plugin metadata.

## What this package is for

`nomad-plugins-metadata` provides:

- a canonical metadata schema,
- extraction and merge tooling for plugin repositories,
- reproducible metadata artifacts for downstream consumers.

The package standardizes both metadata structure and automation behavior so plugin metadata is consistent across repositories.

## Metadata model at a glance

- Manual metadata: `.metadata/nomad_plugin_metadata.manual.yaml`
- Auto metadata: `.metadata/nomad_plugin_metadata.auto.yaml`
- Effective metadata (consumer-facing): `nomad_plugin_metadata.yaml`
- Override report: `.metadata/plugin-metadata.override-report.yaml`

Merge precedence is deterministic:

non-empty values from `.metadata/nomad_plugin_metadata.manual.yaml` > `.metadata/nomad_plugin_metadata.auto.yaml`

## Core capabilities

- Canonical NOMAD metainfo schema definition.
- Automated LinkML export for interoperability and validation.
- Metadata extraction CLI for plugin repositories.
- Deterministic merge contract: manual metadata overrides generated metadata.
- Override report generation for fields blocked by manual edits.
- Reusable GitHub Actions workflow for repository-level automation.

## Tooling artifacts

- Metainfo schema source: `src/nomad_plugins_metadata/schema_packages/schema_package.py`
- Generated LinkML export: `src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml`
- Datatractor mapping: `src/nomad_plugins_metadata/schema_packages/datatractor_mapping.md`
- NOMAD adapter mapping: `src/nomad_plugins_metadata/adapters/nomad_mapping.md`
- Examples: `src/nomad_plugins_metadata/examples/`

## Where to go next

- See [How-to: Install This Plugin](how_to/install_this_plugin.md).
- See [How-to: Use This Plugin](how_to/use_this_plugin.md).
- See [How-to: Apply To Plugin Repo](how_to/apply_to_plugin_repo.md).
- See [Architecture and Rationale](explanation/architecture_and_rationale.md).
- See [Field Semantics](explanation/field_semantics.md) for quantity meanings and intent.
- See [Reference: CLI and API](reference/cli_reference.md).
- See [Reference: Schema](reference/schema_reference.md).
