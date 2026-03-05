# Schema Changelog

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
