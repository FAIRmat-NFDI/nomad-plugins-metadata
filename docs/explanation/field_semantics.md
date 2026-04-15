# Field Semantics

This page explains the intention behind metadata quantity groups in the canonical
`PluginPackage` model and how to interpret generated vs manual values.

## Identity and versioning

- `id`, `name`: stable plugin identity and human-readable label.
- `metadata_schema_version`: schema contract version used by this metadata document.
- `plugin_version`, `maturity`: plugin release maturity state for consumers.

Typical source:
- auto extraction from `pyproject.toml`, repository signals.
- manual overrides when maintainers need stricter curation.

## Repository and distribution status

- `upstream_repository`, `homepage`, `documentation`, `issue_tracker`
- `owner`, `owner_type`, `stars`, `created`, `last_updated`, `archived`
- `deployment.on_central`, `deployment.on_example_oasis`, `deployment.on_pypi`, `deployment.pypi_package`

Purpose:
- discovery and trust signals for users.
- deployment availability checks for registry and ingestion tooling.

Typical source:
- deterministic extraction from project URLs and repository APIs.
- fallback heuristics for deployment/PyPI checks when necessary.

## People and ownership

- `authors[]`, `maintainers[]` with `name`, `email`, `affiliation`, `role`.

Purpose:
- credit attribution (`authors`) and operational contact (`maintainers`).

Typical source:
- `CITATION.cff` prioritized for author credits.
- `pyproject.toml` for maintainers and fallback author data.

## Capabilities and file formats

- `entry_points[]`: declared NOMAD plugin entry points.
- `capabilities[]`: normalized capability model (parser/schema/app/etc.).
- `capabilities[].parser_details.*`: parser matcher and parsing metadata.
- `supported_filetypes[]`, `file_format_support[]`: discovery and compatibility metadata.

Purpose:
- explain what a plugin can do and which data/files it supports.

Typical source:
- entry-point declarations and loaded plugin objects (when available).
- best-effort static extraction from parser matcher configuration.

## Dependencies and compatibility

- `schema_dependencies[]` with `dependency_type`, `package_name`, `location`, `version_range`, `optional`, `purpose`.

Purpose:
- runtime interoperability and compatibility tracking.
- machine-linkable dependency location via `location`.

Typical source:
- dependency parsing from `pyproject.toml`.
- optional index-based location enrichment and fallback resolution.

## Suggested usages and discovery guidance

- `suggested_usages[]` (`id`, `title`, `user_intent`, `domain_category`, `technique`, `audience`, `maturity`, `tags`).

Purpose:
- registry-facing guidance for filtering and user onboarding.
- maintainers can encode how the plugin should be discovered and applied.

Typical source:
- primarily manual curation.

## Provenance and release linkage

- `metadata_provenance[]` (`source`, `extraction_method`, `generated_at`, `generator_version`)
- `release_context` (`release_tag`, `release_commit_sha`)

Purpose:
- auditability and reproducibility of generated metadata.
- clear traceability from metadata snapshots to source release state.

Typical source:
- auto extraction pipeline and CI context.

## Manual vs auto ownership

- machine-generated baseline: `.metadata/nomad_plugin_metadata.auto.yaml`
- maintainer-curated overrides/additions: `.metadata/nomad_plugin_metadata.manual.yaml`
- effective consumer-facing output: `nomad_plugin_metadata.yaml`

Merge rule:
- non-empty manual values override generated values.
