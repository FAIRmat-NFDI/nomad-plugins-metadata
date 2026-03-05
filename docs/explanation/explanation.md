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

### 3. Two-file merge model

Automation writes a machine-owned generated file and never overwrites the manual metadata file.

- generated: `.nomad/plugin-metadata.generated.yaml`
- manual: `nomad_plugin_metadata.yaml`

Effective metadata is produced by deterministic deep-merge with manual precedence.

### 4. Override reporting

When manual values override generated values, the pipeline records those blocked/generated conflicts in:

- `.nomad/plugin-metadata.override-report.yaml`

This gives maintainers visibility into stale generated signals without blocking CI by default.

## Migration strategy

`nomad-plugins` internal schema is treated as a transitional adapter.
The target state is canonical metadata-first ingestion and eventual adapter phase-out after compatibility gates are met.
