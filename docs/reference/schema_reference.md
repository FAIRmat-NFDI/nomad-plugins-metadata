# Schema Reference

Source of truth (runtime schema):
- `src/nomad_plugins_metadata/schema_packages/schema_package.py`

Generated interoperability export (used below):
- `src/nomad_plugins_metadata/schema_packages/nomad_plugin_metadata.yaml`

This page is generated from the exported LinkML schema and should not be edited manually.

## Root Fields (`PluginPackage`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `id` | `string` | `True` | `False` |  | Stable identifier for this metadata object or subsection instance. |
| `metadata_schema_version` | `string` | `True` | `False` |  | Version of this metadata schema used for this document. |
| `name` | `string` | `True` | `False` |  | Human-readable name of the plugin package or person. |
| `description` | `string` | `False` | `False` |  | Short summary description of the plugin package. |
| `plugin_version` | `string` | `False` | `False` |  | Plugin package version. |
| `subject` | `string` | `False` | `True` |  | Domain subjects or topical keywords. |
| `license` | `string` | `False` | `False` |  | Declared software license for the plugin package. |
| `upstream_repository` | `string` | `True` | `False` |  | Canonical source repository URL for the plugin package. |
| `documentation` | `string` | `False` | `False` |  | Primary user/developer documentation URL for the plugin package. |
| `homepage` | `string` | `False` | `False` |  | Homepage URL for the plugin package or project. |
| `issue_tracker` | `string` | `False` | `False` |  | Issue tracker URL for reporting bugs and feature requests. |
| `owner` | `string` | `False` | `False` |  | Repository owner or organization name. |
| `owner_type` | `string` | `False` | `False` |  | Owner classification, e.g. Organization or User. |
| `stars` | `integer` | `False` | `False` |  | GitHub star count at extraction time. |
| `created` | `datetime` | `False` | `False` |  | Repository creation timestamp. |
| `last_updated` | `datetime` | `False` | `False` |  | Last repository update timestamp. |
| `archived` | `boolean` | `False` | `False` |  | Whether the upstream repository is archived. |
| `repository_default_branch` | `string` | `False` | `False` |  | Default branch name used by the source repository. |
| `supported_filetypes` | `string` | `False` | `True` |  | Datatractor-compatible list of supported filetype IDs. |
| `maturity` | `MaturityLevel` | `True` | `False` | alpha, beta, stable, archived | Overall maturity classification of the plugin package. |
| `maintainers` | `Maintainer` | `False` | `True` |  | Maintainer contacts responsible for plugin operation and support. |
| `authors` | `Maintainer` | `False` | `True` |  | Author credits for the plugin package. |
| `entry_points` | `EntryPoint` | `False` | `True` |  | Registered NOMAD entry points exposed by the plugin package. |
| `capabilities` | `PluginCapability` | `False` | `True` |  | High-level capabilities implemented by this plugin package. |
| `file_format_support` | `FileFormatSupport` | `False` | `True` |  | Detailed file-format compatibility records for this plugin. |
| `schema_dependencies` | `SchemaDependency` | `False` | `True` |  | Dependencies required by the plugin package or schema behavior. |
| `suggested_usages` | `SuggestedUsage` | `False` | `True` |  | Curated suggested usage records for discovery and filtering. |
| `deployment` | `DeploymentInfo` | `False` | `False` |  | Deployment and distribution status for this plugin package. |
| `release_context` | `ReleaseContext` | `False` | `False` |  | Release linkage metadata for this generated snapshot. |
| `metadata_provenance` | `MetadataProvenance` | `False` | `True` |  | Provenance records describing how metadata values were produced. |

## Maintainer Fields (`Maintainer`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `name` | `string` | `False` | `False` |  | Human-readable name of the plugin package or person. |
| `email` | `string` | `False` | `False` |  | Email address for a maintainer/author contact. |
| `affiliation` | `string` | `False` | `False` |  | Organization or affiliation for a maintainer/author. |
| `role` | `string` | `False` | `False` |  | Role label for a maintainer/author in plugin lifecycle. |

## Entry Point Fields (`EntryPoint`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `id` | `string` | `True` | `False` |  | Stable identifier for this metadata object or subsection instance. |
| `entry_point_group` | `string` | `True` | `False` |  | Python entry point group name. |
| `entry_point_name` | `string` | `True` | `False` |  | Entry point identifier within the group. |
| `python_object` | `string` | `True` | `False` |  | Import path for entry point object. |
| `capability_type` | `CapabilityType` | `True` | `False` | parser, schema, app, normalizer, example_upload, api, north_tool, tool | Capability category for an entry point or capability record. |

## Capability Fields (`PluginCapability`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `id` | `string` | `True` | `False` |  | Stable identifier for this metadata object or subsection instance. |
| `capability_type` | `CapabilityType` | `True` | `False` | parser, schema, app, normalizer, example_upload, api, north_tool, tool | Capability category for an entry point or capability record. |
| `title` | `string` | `True` | `False` |  | Display title for a capability or suggested usage. |
| `summary` | `string` | `False` | `False` |  | Optional short summary for a capability. |
| `parser_details` | `ParserCapabilityDetails` | `False` | `False` |  | Structured parser matcher details for parser capabilities. |

## Parser Capability Details Fields (`ParserCapabilityDetails`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `parser_name` | `string` | `False` | `False` |  | Canonical parser name used in NOMAD parser registration. |
| `parser_level` | `integer` | `False` | `False` |  | Parser priority/level used in parser dispatch ordering. |
| `parser_aliases` | `string` | `False` | `True` |  | Alternative parser aliases accepted by NOMAD. |
| `mainfile_name_re` | `string` | `False` | `False` |  | Regex matching candidate mainfile names. |
| `mainfile_contents_re` | `string` | `False` | `False` |  | Regex matching candidate mainfile text contents. |
| `mainfile_contents_dict` | `string` | `False` | `False` |  | Serialized dictionary matcher for structured mainfile content checks. |
| `mainfile_mime_re` | `string` | `False` | `False` |  | Regex matching MIME types for candidate mainfiles. |
| `mainfile_binary_header` | `string` | `False` | `False` |  | Binary header signature used to identify mainfiles. |
| `mainfile_binary_header_re` | `string` | `False` | `False` |  | Regex-style binary header matcher used to identify mainfiles. |
| `mainfile_alternative` | `boolean` | `False` | `False` |  | Whether this parser matcher is marked as an alternative matcher. |
| `compression_support` | `CompressionType` | `False` | `True` | gz, bz2, xz, zip, tar | Supported compressed container formats for parser input files. |
| `auxiliary_file_patterns` | `string` | `False` | `True` |  | Auxiliary file name patterns expected by this parser. |

## File Format Support Fields (`FileFormatSupport`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `id` | `string` | `True` | `False` |  | Stable identifier for this metadata object or subsection instance. |
| `label` | `string` | `True` | `False` |  | Human-readable label for a file format or subsection record. |
| `capability_id` | `string` | `False` | `False` |  | Capability identifier that provides this format support. |
| `producer` | `string` | `False` | `False` |  | General producer/code family for ambiguous formats (e.g. .out). |
| `extensions` | `string` | `False` | `True` |  | Known filename extensions for this file format. |
| `mime_types` | `string` | `False` | `True` |  | Known MIME types associated with this file format. |
| `standard` | `string` | `False` | `False` |  | Named file/data standard represented by this format. |
| `instrument_context` | `string` | `False` | `False` |  | Instrument or workflow context where the format is used. |
| `notes` | `string` | `False` | `False` |  | Free-text notes about caveats, scope, or interpretation. |

## Schema Dependency Fields (`SchemaDependency`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `dependency_type` | `DependencyType` | `True` | `False` | nomad_plugin, python_package | Dependency classification (NOMAD plugin vs generic Python package). |
| `package_name` | `string` | `True` | `False` |  | Dependency package name. |
| `location` | `string` | `False` | `False` |  | Canonical dependency location URL (repository, package index, or direct URL). |
| `version_range` | `string` | `False` | `False` |  | Version constraint specifier for the dependency. |
| `optional` | `boolean` | `False` | `False` |  | Whether this dependency is optional. |
| `purpose` | `string` | `False` | `False` |  | Intended dependency purpose, e.g. runtime or optional feature. |

## Suggested Usage Fields (`SuggestedUsage`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `id` | `string` | `True` | `False` |  | Stable identifier for this metadata object or subsection instance. |
| `title` | `string` | `True` | `False` |  | Display title for a capability or suggested usage. |
| `user_intent` | `string` | `True` | `False` |  | User goal addressed by the suggested usage. |
| `domain_category` | `DomainCategory` | `True` | `False` | simulations, measurements, synthesis, cross-domain, workflow, infrastructure | Domain classification used for usage-level discovery filters. |
| `technique` | `string` | `False` | `False` |  | Technique or method keyword associated with this usage. |
| `audience` | `string` | `False` | `False` |  | Target audience level for this suggested usage. |
| `maturity` | `MaturityLevel` | `True` | `False` | alpha, beta, stable, archived | Overall maturity classification of the plugin package. |
| `tags` | `string` | `False` | `True` |  | Additional search/filter tags for the suggested usage. |

## Deployment Fields (`DeploymentInfo`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `on_central` | `boolean` | `False` | `False` |  | Whether plugin is available on central NOMAD deployment. |
| `on_example_oasis` | `boolean` | `False` | `False` |  | Whether plugin is available on NOMAD example oasis deployment. |
| `on_pypi` | `boolean` | `False` | `False` |  | Whether plugin package is published on PyPI. |
| `pypi_package` | `string` | `False` | `False` |  | Published PyPI package name, if available. |

## Release Context Fields (`ReleaseContext`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `release_tag` | `string` | `False` | `False` |  | Release tag associated with this metadata snapshot. |
| `release_commit_sha` | `string` | `False` | `False` |  | Commit SHA associated with this metadata snapshot. |

## Metadata Provenance Fields (`MetadataProvenance`)

| Field | Range | Required | Multi | Enum Values | Description |
|---|---|---|---|---|---|
| `source` | `MetadataSource` | `True` | `False` | manual_override, plugin_entry_points, pyproject, citation_cff, repository_api, extraction_fallback | Declared metadata source for this provenance record. |
| `extraction_method` | `ExtractionMethod` | `True` | `False` | deterministic, heuristic, manual | Extraction strategy used for this provenance record. |
| `generated_at` | `datetime` | `True` | `False` |  | Timestamp when this provenance record was generated. |
| `generator_version` | `string` | `False` | `False` |  | Version of the extractor/generator that produced this record. |


## Full Schema-Shaped YAML Template

Generated from the exported LinkML schema (all fields included), with per-field comments:

```yaml
# string; required; Stable identifier for this metadata object or subsection instance.
id: null
# string; required; Version of this metadata schema used for this document.
metadata_schema_version: null
# string; optional; Human-readable name of the plugin package or person.
name: null
# string; optional; Short summary description of the plugin package.
description: null
# string; optional; Plugin package version.
plugin_version: null
# list[string]; optional; Domain subjects or topical keywords.
subject: []
# string; optional; Declared software license for the plugin package.
license: null
# string; required; Canonical source repository URL for the plugin package.
upstream_repository: null
# string; optional; Primary user/developer documentation URL for the plugin package.
documentation: null
# string; optional; Homepage URL for the plugin package or project.
homepage: null
# string; optional; Issue tracker URL for reporting bugs and feature requests.
issue_tracker: null
# string; optional; Repository owner or organization name.
owner: null
# string; optional; Owner classification, e.g. Organization or User.
owner_type: null
# integer; optional; GitHub star count at extraction time.
stars: null
# datetime; optional; Repository creation timestamp.
created: null
# datetime; optional; Last repository update timestamp.
last_updated: null
# boolean; optional; Whether the upstream repository is archived.
archived: null
# string; optional; Default branch name used by the source repository.
repository_default_branch: null
# list[string]; optional; Datatractor-compatible list of supported filetype IDs.
supported_filetypes: []
# MaturityLevel; enum: alpha, beta, stable, archived; required; Overall maturity classification of the plugin package.
maturity: null
# list[Maintainer]; optional; Maintainer contacts responsible for plugin operation and support.
maintainers:
  -
    # string; optional; Human-readable name of the plugin package or person.
    name: null
    # string; optional; Email address for a maintainer/author contact.
    email: null
    # string; optional; Organization or affiliation for a maintainer/author.
    affiliation: null
    # string; optional; Role label for a maintainer/author in plugin lifecycle.
    role: null
# list[Maintainer]; optional; Author credits for the plugin package.
authors:
  -
    # string; optional; Human-readable name of the plugin package or person.
    name: null
    # string; optional; Email address for a maintainer/author contact.
    email: null
    # string; optional; Organization or affiliation for a maintainer/author.
    affiliation: null
    # string; optional; Role label for a maintainer/author in plugin lifecycle.
    role: null
# list[EntryPoint]; optional; Registered NOMAD entry points exposed by the plugin package.
entry_points:
  -
    # string; required; Stable identifier for this metadata object or subsection instance.
    id: null
    # string; required; Python entry point group name.
    entry_point_group: null
    # string; required; Entry point identifier within the group.
    entry_point_name: null
    # string; required; Import path for entry point object.
    python_object: null
    # CapabilityType; enum: parser, schema, app, normalizer, example_upload, api, north_tool, tool; required; Capability category for an entry point or capability record.
    capability_type: null
# list[PluginCapability]; optional; High-level capabilities implemented by this plugin package.
capabilities:
  -
    # string; required; Stable identifier for this metadata object or subsection instance.
    id: null
    # CapabilityType; enum: parser, schema, app, normalizer, example_upload, api, north_tool, tool; required; Capability category for an entry point or capability record.
    capability_type: null
    # string; required; Display title for a capability or suggested usage.
    title: null
    # string; optional; Optional short summary for a capability.
    summary: null
    # ParserCapabilityDetails; optional; Structured parser matcher details for parser capabilities.
    parser_details:
      # string; optional; Canonical parser name used in NOMAD parser registration.
      parser_name: null
      # integer; optional; Parser priority/level used in parser dispatch ordering.
      parser_level: null
      # list[string]; optional; Alternative parser aliases accepted by NOMAD.
      parser_aliases: []
      # string; optional; Regex matching candidate mainfile names.
      mainfile_name_re: null
      # string; optional; Regex matching candidate mainfile text contents.
      mainfile_contents_re: null
      # string; optional; Serialized dictionary matcher for structured mainfile content checks.
      mainfile_contents_dict: null
      # string; optional; Regex matching MIME types for candidate mainfiles.
      mainfile_mime_re: null
      # string; optional; Binary header signature used to identify mainfiles.
      mainfile_binary_header: null
      # string; optional; Regex-style binary header matcher used to identify mainfiles.
      mainfile_binary_header_re: null
      # boolean; optional; Whether this parser matcher is marked as an alternative matcher.
      mainfile_alternative: null
      # list[CompressionType]; enum: gz, bz2, xz, zip, tar; optional; Supported compressed container formats for parser input files.
      compression_support: []
      # list[string]; optional; Auxiliary file name patterns expected by this parser.
      auxiliary_file_patterns: []
# list[FileFormatSupport]; optional; Detailed file-format compatibility records for this plugin.
file_format_support:
  -
    # string; required; Stable identifier for this metadata object or subsection instance.
    id: null
    # string; required; Human-readable label for a file format or subsection record.
    label: null
    # string; optional; Capability identifier that provides this format support.
    capability_id: null
    # string; optional; General producer/code family for ambiguous formats (e.g. .out).
    producer: null
    # list[string]; optional; Known filename extensions for this file format.
    extensions: []
    # list[string]; optional; Known MIME types associated with this file format.
    mime_types: []
    # string; optional; Named file/data standard represented by this format.
    standard: null
    # string; optional; Instrument or workflow context where the format is used.
    instrument_context: null
    # string; optional; Free-text notes about caveats, scope, or interpretation.
    notes: null
# list[SchemaDependency]; optional; Dependencies required by the plugin package or schema behavior.
schema_dependencies:
  -
    # DependencyType; enum: nomad_plugin, python_package; required; Dependency classification (NOMAD plugin vs generic Python package).
    dependency_type: null
    # string; required; Dependency package name.
    package_name: null
    # string; optional; Canonical dependency location URL (repository, package index, or direct URL).
    location: null
    # string; optional; Version constraint specifier for the dependency.
    version_range: null
    # boolean; optional; Whether this dependency is optional.
    optional: null
    # string; optional; Intended dependency purpose, e.g. runtime or optional feature.
    purpose: null
# list[SuggestedUsage]; optional; Curated suggested usage records for discovery and filtering.
suggested_usages:
  -
    # string; required; Stable identifier for this metadata object or subsection instance.
    id: null
    # string; required; Display title for a capability or suggested usage.
    title: null
    # string; required; User goal addressed by the suggested usage.
    user_intent: null
    # DomainCategory; enum: simulations, measurements, synthesis, cross-domain, workflow, infrastructure; required; Domain classification used for usage-level discovery filters.
    domain_category: null
    # string; optional; Technique or method keyword associated with this usage.
    technique: null
    # string; optional; Target audience level for this suggested usage.
    audience: null
    # MaturityLevel; enum: alpha, beta, stable, archived; required; Overall maturity classification of the plugin package.
    maturity: null
    # list[string]; optional; Additional search/filter tags for the suggested usage.
    tags: []
# DeploymentInfo; optional; Deployment and distribution status for this plugin package.
deployment:
  # boolean; optional; Whether plugin is available on central NOMAD deployment.
  on_central: null
  # boolean; optional; Whether plugin is available on NOMAD example oasis deployment.
  on_example_oasis: null
  # boolean; optional; Whether plugin package is published on PyPI.
  on_pypi: null
  # string; optional; Published PyPI package name, if available.
  pypi_package: null
# ReleaseContext; optional; Release linkage metadata for this generated snapshot.
release_context:
  # string; optional; Release tag associated with this metadata snapshot.
  release_tag: null
  # string; optional; Commit SHA associated with this metadata snapshot.
  release_commit_sha: null
# list[MetadataProvenance]; optional; Provenance records describing how metadata values were produced.
metadata_provenance:
  -
    # MetadataSource; enum: manual_override, plugin_entry_points, pyproject, citation_cff, repository_api, extraction_fallback; required; Declared metadata source for this provenance record.
    source: null
    # ExtractionMethod; enum: deterministic, heuristic, manual; required; Extraction strategy used for this provenance record.
    extraction_method: null
    # datetime; required; Timestamp when this provenance record was generated.
    generated_at: null
    # string; optional; Version of the extractor/generator that produced this record.
    generator_version: null
```

## Enums

- `CapabilityType`: parser, schema, app, normalizer, example_upload, api, north_tool, tool
- `DomainCategory`: simulations, measurements, synthesis, cross-domain, workflow, infrastructure
- `MaturityLevel`: alpha, beta, stable, archived
- `DependencyType`: nomad_plugin, python_package
- `MetadataSource`: manual_override, plugin_entry_points, pyproject, citation_cff, repository_api, extraction_fallback
- `ExtractionMethod`: deterministic, heuristic, manual
- `CompressionType`: gz, bz2, xz, zip, tar
