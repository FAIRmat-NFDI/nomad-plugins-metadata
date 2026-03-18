# Schema Reference

Source of truth:
- `src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml`

## Root Fields (`PluginPackage`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `id` | `string` | `True` | `False` |  | Stable machine identifier. |
| `metadata_schema_version` | `string` | `True` | `False` |  | Version of this metadata schema used for this document. |
| `name` | `string` | `True` | `False` |  |  |
| `description` | `string` | `False` | `False` |  |  |
| `plugin_version` | `string` | `False` | `False` |  | Plugin package version. |
| `subject` | `string` | `False` | `True` |  | Domain subjects or topical keywords. |
| `license` | `string` | `False` | `False` |  |  |
| `upstream_repository` | `string` | `True` | `False` |  |  |
| `documentation` | `string` | `False` | `False` |  |  |
| `homepage` | `string` | `False` | `False` |  |  |
| `issue_tracker` | `string` | `False` | `False` |  |  |
| `owner` | `string` | `False` | `False` |  |  |
| `owner_type` | `string` | `False` | `False` |  |  |
| `stars` | `integer` | `False` | `False` |  |  |
| `created` | `datetime` | `False` | `False` |  |  |
| `last_updated` | `datetime` | `False` | `False` |  |  |
| `archived` | `boolean` | `False` | `False` |  |  |
| `maintainers` | `Maintainer` | `False` | `True` |  |  |
| `authors` | `Maintainer` | `False` | `True` |  |  |
| `repository_default_branch` | `string` | `False` | `False` |  |  |
| `entry_points` | `EntryPoint` | `False` | `True` |  |  |
| `supported_filetypes` | `string` | `False` | `True` |  | Datatractor-compatible list of supported filetype IDs. |
| `capabilities` | `PluginCapability` | `False` | `True` |  |  |
| `file_format_support` | `FileFormatSupport` | `False` | `True` |  |  |
| `schema_dependencies` | `SchemaDependency` | `False` | `True` |  |  |
| `suggested_usages` | `SuggestedUsage` | `False` | `True` |  |  |
| `deployment` | `DeploymentInfo` | `False` | `False` |  |  |
| `release_context` | `ReleaseContext` | `False` | `False` |  |  |
| `maturity` | `MaturityLevel` | `True` | `False` | alpha, beta, stable, archived |  |
| `metadata_provenance` | `MetadataProvenance` | `False` | `True` |  |  |

## Full Schema-Shaped YAML Template

Generated from the LinkML schema (all fields included), with per-field comments:

```yaml
# string; required; Stable machine identifier.
id: null
# string; required; Version of this metadata schema used for this document.
metadata_schema_version: null
# string; required
name: null
# string; optional
description: null
# string; optional; Plugin package version.
plugin_version: null
# list[string]; optional; Domain subjects or topical keywords.
subject: []
# string; optional
license: null
# string; required
upstream_repository: null
# string; optional
documentation: null
# string; optional
homepage: null
# string; optional
issue_tracker: null
# string; optional
owner: null
# string; optional
owner_type: null
# integer; optional
stars: null
# datetime; optional
created: null
# datetime; optional
last_updated: null
# boolean; optional
archived: null
# list[Maintainer]; optional
maintainers:
  -
    # string; required
    name: null
    # string; optional
    email: null
    # string; optional
    affiliation: null
    # string; optional
    role: null
# list[Maintainer]; optional
authors:
  -
    # string; required
    name: null
    # string; optional
    email: null
    # string; optional
    affiliation: null
    # string; optional
    role: null
# string; optional
repository_default_branch: null
# list[EntryPoint]; optional
entry_points:
  -
    # string; required; Stable machine identifier.
    id: null
    # string; required; Python entry point group name.
    entry_point_group: null
    # string; required; Entry point identifier within the group.
    entry_point_name: null
    # string; required; Import path for entry point object.
    python_object: null
    # CapabilityType; enum: parser, schema, app, normalizer, example_upload, api, north_tool, tool; required
    capability_type: null
# list[string]; optional; Datatractor-compatible list of supported filetype IDs.
supported_filetypes: []
# list[PluginCapability]; optional
capabilities:
  -
    # string; required; Stable machine identifier.
    id: null
    # CapabilityType; enum: parser, schema, app, normalizer, example_upload, api, north_tool, tool; required
    capability_type: null
    # string; required
    title: null
    # string; optional
    summary: null
    # ParserCapabilityDetails; optional
    parser_details:
      # string; optional
      parser_name: null
      # integer; optional
      parser_level: null
      # list[string]; optional
      parser_aliases: []
      # string; optional
      mainfile_name_re: null
      # string; optional
      mainfile_contents_re: null
      # string; optional
      mainfile_contents_dict: null
      # string; optional
      mainfile_mime_re: null
      # string; optional
      mainfile_binary_header: null
      # string; optional
      mainfile_binary_header_re: null
      # boolean; optional
      mainfile_alternative: null
      # list[CompressionType]; enum: gz, bz2, xz, zip, tar; optional
      compression_support: []
      # list[string]; optional
      auxiliary_file_patterns: []
# list[FileFormatSupport]; optional
file_format_support:
  -
    # string; required; Stable machine identifier.
    id: null
    # string; required
    label: null
    # list[string]; optional
    extensions: []
    # list[string]; optional
    mime_types: []
    # string; optional
    standard: null
    # string; optional
    instrument_context: null
    # string; optional
    notes: null
# list[SchemaDependency]; optional
schema_dependencies:
  -
    # DependencyType; enum: nomad_plugin, python_package; required
    dependency_type: null
    # string; required
    package_name: null
    # string; optional
    version_range: null
    # boolean; optional
    optional: null
    # string; optional
    purpose: null
# list[SuggestedUsage]; optional
suggested_usages:
  -
    # string; required; Stable machine identifier.
    id: null
    # string; required
    title: null
    # string; required
    user_intent: null
    # DomainCategory; enum: simulations, measurements, synthesis, cross-domain, workflow, infrastructure; required
    domain_category: null
    # string; optional
    technique: null
    # string; optional
    audience: null
    # MaturityLevel; enum: alpha, beta, stable, archived; required
    maturity: null
    # list[string]; optional
    tags: []
# DeploymentInfo; optional
deployment:
  # boolean; optional
  on_central: null
  # boolean; optional
  on_example_oasis: null
  # boolean; optional
  on_pypi: null
  # string; optional
  pypi_package: null
# ReleaseContext; optional
release_context:
  # string; optional
  release_tag: null
  # string; optional
  release_commit_sha: null
# MaturityLevel; enum: alpha, beta, stable, archived; required
maturity: null
# list[MetadataProvenance]; optional
metadata_provenance:
  -
    # MetadataSource; enum: manual_override, plugin_entry_points, pyproject, citation_cff, repository_api, crawler_fallback; required
    source: null
    # ExtractionMethod; enum: deterministic, heuristic, manual; required
    extraction_method: null
    # datetime; required
    generated_at: null
    # string; optional
    generator_version: null
```

## Enums

- `CapabilityType`: parser, schema, app, normalizer, example_upload, api, north_tool, tool
- `DomainCategory`: simulations, measurements, synthesis, cross-domain, workflow, infrastructure
- `MaturityLevel`: alpha, beta, stable, archived
- `DependencyType`: nomad_plugin, python_package
- `MetadataSource`: manual_override, plugin_entry_points, pyproject, citation_cff, repository_api, crawler_fallback
- `ExtractionMethod`: deterministic, heuristic, manual
- `CompressionType`: gz, bz2, xz, zip, tar
