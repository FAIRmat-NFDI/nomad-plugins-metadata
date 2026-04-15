# Architecture and Rationale

## Design choices

### 1. Canonical NOMAD schema + LinkML export

NOMAD metainfo classes are the active source of truth for runtime integration, searchability, and archive persistence.
LinkML is exported automatically from this NOMAD schema for interoperability, validation, and docs.

This keeps semantic ownership with the active runtime model while preserving compatibility with DataTractor-style contracts.

### 2. Plugin-owned extraction

Metadata generation is intended to run in each plugin repository CI and/or local development workflow.

Why:

- plugin maintainers can add plugin-specific extraction hooks,
- extraction behavior is versioned with plugin code.

The reusable workflow installs the target plugin repository in editable mode before extraction.
This allows the extractor to load installed `nomad.plugin` entry-point objects and harvest
technical metadata (especially parser matcher details) directly from entry-point configuration.

### 3. Three-file merge model

Automation writes machine-owned `auto` and `effective` files and never overwrites the manual template file.

- auto: `.metadata/nomad_plugin_metadata.auto.yaml`
- manual: `.metadata/nomad_plugin_metadata.manual.yaml`
- effective: `nomad_plugin_metadata.yaml`

Effective metadata is produced by deterministic deep-merge with manual precedence,
ignoring empty values from the manual template.

### Field-source precedence (quick view)

- `authors`: `CITATION.cff` authors > `pyproject` authors.
- `maintainers`: `pyproject` maintainers.
- `upstream_repository`: `pyproject.urls.Repository` > `CITATION.cff` `repository-code`.
- `documentation`: `pyproject.urls.Documentation` > GitHub Pages probe.
- `homepage`: `pyproject.urls.Homepage` > `CITATION.cff` `url` > resolved repository URL.
- `stars`, `owner`, `owner_type`, `created`, `last_updated`, `archived`: GitHub repository API (best-effort).
- Manual metadata still has final precedence in effective output.

### 4. Override reporting

When manual values override generated values, the pipeline records those blocked/generated conflicts in:

- `.metadata/plugin-metadata.override-report.yaml`

This gives maintainers visibility into stale generated signals without blocking CI by default.

### 5. Release-driven PR workflow

On release publication, the reusable workflow can regenerate metadata and open/update a rolling PR.
This keeps metadata updates reviewable, links metadata snapshots to release tag + commit SHA, and avoids direct writes to `main`.

## Scope

This package defines the metadata schema, extraction, merge behavior, and generated interoperability artifacts.
Integration details in other repositories are intentionally out of scope here.

For field-by-field intent, see `explanation/field_semantics.md`.
