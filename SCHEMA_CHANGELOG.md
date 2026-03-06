# Schema Changelog

## Unreleased

### Added
- `release_context` fields in canonical schema and metainfo adapter (`release_tag`, `release_commit_sha`).
- Release-aware extractor options: `--release-tag`, `--release-sha`, `--update-front-file`.

### Changed
- Reusable extraction workflow supports release-driven rolling PR mode with standard PR body and diff summary.
- Release caller template now triggers on `release.published` (+ `workflow_dispatch`) and creates/updates a metadata PR.

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
