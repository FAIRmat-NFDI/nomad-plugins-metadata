# Canonical-to-NOMAD Adapter Mapping

This document defines how canonical LinkML metadata maps to the transitional `nomad-plugins` metainfo adapter.

## Strategy
1. Canonical schema (`src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml`) is the source of truth.
2. `nomad-plugins` metainfo schema is a compatibility adapter for ingestion/search/UI.
3. Adapter is transitional and can be retired once migration gates are met.

## Field mapping
| Canonical (`PluginPackage`) | `nomad-plugins` adapter target | Transition behavior |
|---|---|---|
| `id` | `Plugin.id` (or equivalent identifier quantity) | Must be preserved exactly. |
| `name` | `Plugin.name` | Direct copy. |
| `description` | `Plugin.description` | Direct copy. |
| `upstream_repository` | `Plugin.repository` / repo URL field | Direct copy. |
| `documentation` | `Plugin.plugin_documentation_url` | Direct copy where available. |
| `deployment.on_central` | `Plugin.on_central` | Direct copy. |
| `deployment.on_example_oasis` | `Plugin.on_example_oasis` | Direct copy. |
| `deployment.on_pypi` | `Plugin.on_pypi` | Direct copy. |
| `capabilities[]` | `Plugin.parser` / `Plugin.schema` / `Plugin.app` subsections | Mapped by `capability_type`. |
| `capabilities[].parser_details.mainfile_*` | parser matcher quantities | Direct copy from parser capability. |
| `supported_filetypes[]` | parser supported types / registry tags | Preserve IDs; no translation. |
| `file_format_support[]` | derived UI/search fields | Flatten if adapter cannot hold nested sections. |
| `schema_dependencies[]` | dependency subsection in adapter | New subsection in transition. |
| `suggested_usages[]` | UI filter payload fields | Flatten to filter tags as needed. |
| `release_context.release_tag` / `release_context.release_commit_sha` | release linkage fields | Keep in adapter payload for version traceability. |
| `metadata_provenance[]` | optional internal audit fields | Keep for traceability/debugging. |

## Precedence at ingest
1. Canonical auto metadata (`nomad_plugin_metadata.auto.yaml`)
2. Canonical manual override (`nomad_plugin_metadata.manual.yaml`)
3. Legacy crawler fallback (`pyproject.toml`, repository API)

## Query compatibility during migration
1. Keep existing adapter schema identity query paths active.
2. Add canonical-derived query paths in parallel.
3. Ensure registry filters accept both paths until recrawl/backfill is complete.

## Removal gates for adapter
1. Canonical metadata coverage is complete for actively maintained plugins.
2. No lossy mapping for required UI/app semantics.
3. Dual-schema mode passes release regression checks.
4. One release cycle completed with no critical migration regressions.
