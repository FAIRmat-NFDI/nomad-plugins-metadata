# Datatractor Compatibility Mapping

This document defines how `nomad_plugin_metadata` aligns with the datatractor extractor model.

## Goal
Preserve compatibility for shared discovery fields while extending metadata for NOMAD-specific plugin behavior.

## Direct field mappings
| datatractor field | canonical field (`PluginPackage`) | Notes |
|---|---|---|
| `id` | `id` | Same semantics: stable identifier. |
| `name` | `name` | Same semantics. |
| `description` | `description` | Same semantics. |
| `subject` | `subject[]` | Same semantics as domain/topic tags. |
| `license` | `license` | Same semantics. |
| `upstream_repository` | `upstream_repository` | Same semantics. |
| `documentation` | `documentation` | Same semantics. |
| `supported_filetypes` | `supported_filetypes[]` | Preserved as datatractor filetype IDs. |

## Structured extension mappings
| New canonical field | datatractor analog | Notes |
|---|---|---|
| `capabilities[]` | partial | datatractor models extractor behavior; this generalizes to parser/schema/app/etc. |
| `capabilities[].parser_details.*` | extractor matching metadata | Includes `mainfile_*` patterns and aux files. |
| `file_format_support[]` | `FileType` metadata | Adds mime/extensions/standards in plugin-centric shape. |
| `schema_dependencies[]` | none | New dependency model for plugin interoperability. |
| `suggested_usages[]` | usage instructions (conceptual) | Registry-facing guidance and filtering hints. |
| `deployment.*` | none | NOMAD deployment/publishing state. |
| `metadata_provenance[]` | none | Extraction traceability. |

## Compatibility rules
1. Keep datatractor-compatible fields stable and optionality conservative.
2. Never overload datatractor fields with NOMAD-only semantics.
3. Put NOMAD-specific additions into dedicated extension fields.
4. If a field cannot be inferred, leave it missing and use `nomad_plugin_metadata.manual.yaml` override.

## Known gaps (Phase 1)
1. No strict one-to-one mapping yet for executable `usage` command templates.
2. Controlled vocabulary crosswalk (`subject` values) is intentionally left open.
3. Canonical schema supports multiple capability types; datatractor extractor model is parser/extractor-centric.
