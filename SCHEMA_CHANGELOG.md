# Schema Changelog

## Unreleased

### Added
- `release_context` fields in canonical schema and metainfo adapter (`release_tag`, `release_commit_sha`).
- Release-aware extractor options: `--release-tag`, `--release-sha`.
- Technical metadata extraction from installed `nomad.plugin` entry points (parser matcher fields, compression support, capability metadata).
- Automated LinkML export from NOMAD metainfo source (`scripts/export_linkml_schema.py`).
- Drift checks ensuring committed LinkML export matches NOMAD metainfo source in tests/validation.
- DataTractor compatibility tests for core shared fields and `supported_filetypes` shape.

### Changed
- Source-of-truth orientation changed: NOMAD metainfo schema is canonical; LinkML is generated interoperability export.
- Reusable extraction workflow supports release-driven rolling PR mode with standard PR body and diff summary.
- Release caller template now triggers on `release.published` (+ `workflow_dispatch`) and creates/updates a metadata PR.
- Canonical repository field renamed from `source_repository` to `upstream_repository`.
- Deprecated keys (`source_repository`, `repository_url`) are automatically removed from effective/front-facing metadata during extraction.
- Metadata pipeline switched to explicit four-file contract:
  - `nomad_plugin_metadata.auto.yaml` (machine)
  - `nomad_plugin_metadata.manual.yaml` (maintainer)
  - `nomad_plugin_metadata.yaml` (effective/query)
  - `.metadata/plugin-metadata.override-report.yaml` (conflict report)
- `metadata_provenance` no longer includes `confidence` (removed as non-computed field).
- Provenance source label `static_code_scan` replaced with `plugin_entry_points` for entry-point-derived metadata.
- `DependencyType` simplified to: `nomad_plugin`, `python_package`.
- Auto-maturity heuristics in extractor:
  - `archived` if GitHub repository is archived
  - else `stable` for plugin versions `>=1.0.0`
  - manual metadata still overrides auto values.

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
