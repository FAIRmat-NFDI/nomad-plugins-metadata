# Schema Changelog

## Unreleased

### Added
- `release_context` fields in canonical schema and metainfo adapter (`release_tag`, `release_commit_sha`).
- Release-aware extractor options: `--release-tag`, `--release-sha`.
- Technical metadata extraction from installed `nomad.plugin` entry points (parser matcher fields, compression support, capability metadata).

### Changed
- Reusable extraction workflow supports release-driven rolling PR mode with standard PR body and diff summary.
- Release caller template now triggers on `release.published` (+ `workflow_dispatch`) and creates/updates a metadata PR.
- Canonical repository field renamed from `source_repository` to `upstream_repository`.
- Deprecated keys (`source_repository`, `repository_url`) are automatically removed from effective/front-facing metadata during extraction.
- Metadata pipeline switched to explicit four-file contract:
  - `nomad_plugin_metadata.auto.yaml` (machine)
  - `nomad_plugin_metadata.manual.yaml` (maintainer)
  - `nomad_plugin_metadata.yaml` (effective/query)
  - `.nomad/plugin-metadata.override-report.yaml` (conflict report)

## 1.0.0 - 2026-03-05

Initial baseline for canonical plugin metadata schema and metainfo adapter.

### Added
- Canonical LinkML schema at `src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml`.
- NOMAD metainfo classes in `src/nomad_plugins_metadata/schema_packages/schema_package.py`.
- Example metadata documents under `src/nomad_plugins_metadata/examples/`.
- Datatractor mapping doc at `src/nomad_plugins_metadata/schema_packages/datatractor_mapping.md`.
- NOMAD adapter mapping doc at `src/nomad_plugins_metadata/adapters/nomad_mapping.md`.

### Controlled vocabularies
- `domain_category`: `simulations`, `measurements`, `synthesis`, `cross-domain`, `workflow`, `infrastructure`.
- `maturity`: `alpha`, `beta`, `stable`, `archived`.

### Validation and consistency
- Added enum consistency tests between LinkML and metainfo definitions.
- Added schema validation script with LinkML CLI checks for examples.
