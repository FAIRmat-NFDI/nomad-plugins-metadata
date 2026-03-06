# Explanation

## Design choices

### 1. Canonical schema + adapter split

The canonical plugin metadata contract is defined in LinkML.
NOMAD metainfo classes mirror this model for runtime integration, searchability, and archive persistence.

This keeps semantic ownership in one canonical schema while preserving compatibility with existing NOMAD infrastructure.

### 2. Plugin-owned extraction

Metadata extraction is executed in each plugin repository CI rather than centrally in crawler CI.

Why:

- no need to install every plugin in a central pipeline,
- plugin maintainers can add plugin-specific extraction hooks,
- extraction behavior is versioned with plugin code.

The reusable workflow installs the target plugin repository in editable mode before extraction.
This allows the extractor to load installed `nomad.plugin` entry-point objects and harvest
technical metadata (especially parser matcher details) directly from entry-point configuration.

### 3. Three-file merge model

Automation writes machine-owned `auto` and `effective` files and never overwrites the manual template file.

- auto: `nomad_plugin_metadata.auto.yaml`
- manual: `nomad_plugin_metadata.manual.yaml`
- effective: `nomad_plugin_metadata.yaml`

Effective metadata is produced by deterministic deep-merge with manual precedence,
ignoring empty values from the manual template.

### 4. Override reporting

When manual values override generated values, the pipeline records those blocked/generated conflicts in:

- `.metadata/plugin-metadata.override-report.yaml`

This gives maintainers visibility into stale generated signals without blocking CI by default.

### 5. Release-driven PR workflow

On release publication, the reusable workflow can regenerate metadata and open/update a rolling PR.
This keeps metadata updates reviewable, links metadata snapshots to release tag + commit SHA, and avoids direct writes to `main`.

## Migration strategy

`nomad-plugins` internal schema is treated as a transitional adapter.
The target state is canonical metadata-first ingestion and eventual adapter phase-out after compatibility gates are met.
