from __future__ import annotations

from pathlib import Path

import yaml
from nomad.metainfo import MEnum, Quantity, SubSection

from nomad_plugins_metadata.schema_packages import schema_package as sp

SCHEMA_PATH = Path(__file__).resolve().parent / 'nomad_plugin_metadata.yaml'

SCHEMA_VERSION = '1.0.0'
ROOT_CLASS_NAME = 'PluginPackage'
ROOT_NOMAD_CLASS_NAME = 'PluginMetadata'

CLASS_ORDER = [
    'PluginMetadata',
    'Maintainer',
    'EntryPoint',
    'PluginCapability',
    'ParserCapabilityDetails',
    'FileFormatSupport',
    'SchemaDependency',
    'SuggestedUsage',
    'DeploymentInfo',
    'ReleaseContext',
    'MetadataProvenance',
]

CLASS_DESCRIPTIONS = {
    'PluginPackage': 'Top-level metadata object for a single NOMAD plugin package.',
    'Maintainer': 'Maintainer or ownership contact for this plugin.',
    'EntryPoint': 'A registered NOMAD plugin entry point.',
    'PluginCapability': 'Declares one high-level capability implemented by the plugin.',
    'ParserCapabilityDetails': 'Structured parser metadata used for parser discoverability.',
    'FileFormatSupport': 'File format support details for a plugin capability.',
    'SchemaDependency': 'Declares dependency on plugin/schema packages.',
    'SuggestedUsage': 'Registry-facing usage suggestion for filtering and discovery.',
    'DeploymentInfo': 'Deployment and distribution status for this plugin.',
    'ReleaseContext': 'Release linkage for generated/effective metadata snapshots.',
    'MetadataProvenance': 'How metadata was produced.',
}

SLOT_DESCRIPTIONS = {
    'id': 'Stable identifier for this metadata object or subsection instance.',
    'metadata_schema_version': 'Version of this metadata schema used for this document.',
    'name': 'Human-readable name of the plugin package or person.',
    'description': 'Short summary description of the plugin package.',
    'plugin_version': 'Plugin package version.',
    'subject': 'Domain subjects or topical keywords.',
    'license': 'Declared software license for the plugin package.',
    'upstream_repository': 'Canonical source repository URL for the plugin package.',
    'documentation': 'Primary user/developer documentation URL for the plugin package.',
    'homepage': 'Homepage URL for the plugin package or project.',
    'issue_tracker': 'Issue tracker URL for reporting bugs and feature requests.',
    'owner': 'Repository owner or organization name.',
    'owner_type': 'Owner classification, e.g. Organization or User.',
    'stars': 'GitHub star count at extraction time.',
    'created': 'Repository creation timestamp.',
    'last_updated': 'Last repository update timestamp.',
    'archived': 'Whether the upstream repository is archived.',
    'repository_default_branch': 'Default branch name used by the source repository.',
    'maturity': 'Overall maturity classification of the plugin package.',
    'maintainers': 'Maintainer contacts responsible for plugin operation and support.',
    'authors': 'Author credits for the plugin package.',
    'entry_points': 'Registered NOMAD entry points exposed by the plugin package.',
    'capabilities': 'High-level capabilities implemented by this plugin package.',
    'entry_point_group': 'Python entry point group name.',
    'entry_point_name': 'Entry point identifier within the group.',
    'python_object': 'Import path for entry point object.',
    'capability_type': 'Capability category for an entry point or capability record.',
    'title': 'Display title for a capability or suggested usage.',
    'summary': 'Optional short summary for a capability.',
    'parser_details': 'Structured parser matcher details for parser capabilities.',
    'parser_name': 'Canonical parser name used in NOMAD parser registration.',
    'parser_level': 'Parser priority/level used in parser dispatch ordering.',
    'parser_aliases': 'Alternative parser aliases accepted by NOMAD.',
    'mainfile_name_re': 'Regex matching candidate mainfile names.',
    'mainfile_contents_re': 'Regex matching candidate mainfile text contents.',
    'mainfile_contents_dict': 'Serialized dictionary matcher for structured mainfile content checks.',
    'mainfile_mime_re': 'Regex matching MIME types for candidate mainfiles.',
    'mainfile_binary_header': 'Binary header signature used to identify mainfiles.',
    'mainfile_binary_header_re': 'Regex-style binary header matcher used to identify mainfiles.',
    'mainfile_alternative': 'Whether this parser matcher is marked as an alternative matcher.',
    'compression_support': 'Supported compressed container formats for parser input files.',
    'auxiliary_file_patterns': 'Auxiliary file name patterns expected by this parser.',
    'supported_filetypes': 'Datatractor-compatible list of supported filetype IDs.',
    'file_format_support': 'Detailed file-format compatibility records for this plugin.',
    'label': 'Human-readable label for a file format or subsection record.',
    'capability_id': 'Capability identifier that provides this format support.',
    'producer': 'General producer/code family for ambiguous formats (e.g. .out).',
    'extensions': 'Known filename extensions for this file format.',
    'mime_types': 'Known MIME types associated with this file format.',
    'standard': 'Named file/data standard represented by this format.',
    'instrument_context': 'Instrument or workflow context where the format is used.',
    'notes': 'Free-text notes about caveats, scope, or interpretation.',
    'schema_dependencies': 'Dependencies required by the plugin package or schema behavior.',
    'dependency_type': 'Dependency classification (NOMAD plugin vs generic Python package).',
    'package_name': 'Dependency package name.',
    'location': 'Canonical dependency location URL (repository, package index, or direct URL).',
    'version_range': 'Version constraint specifier for the dependency.',
    'optional': 'Whether this dependency is optional.',
    'purpose': 'Intended dependency purpose, e.g. runtime or optional feature.',
    'suggested_usages': 'Curated suggested usage records for discovery and filtering.',
    'user_intent': 'User goal addressed by the suggested usage.',
    'domain_category': 'Domain classification used for usage-level discovery filters.',
    'technique': 'Technique or method keyword associated with this usage.',
    'audience': 'Target audience level for this suggested usage.',
    'tags': 'Additional search/filter tags for the suggested usage.',
    'deployment': 'Deployment and distribution status for this plugin package.',
    'on_central': 'Whether plugin is available on central NOMAD deployment.',
    'on_example_oasis': 'Whether plugin is available on NOMAD example oasis deployment.',
    'on_pypi': 'Whether plugin package is published on PyPI.',
    'pypi_package': 'Published PyPI package name, if available.',
    'release_context': 'Release linkage metadata for this generated snapshot.',
    'release_tag': 'Release tag associated with this metadata snapshot.',
    'release_commit_sha': 'Commit SHA associated with this metadata snapshot.',
    'metadata_provenance': 'Provenance records describing how metadata values were produced.',
    'source': 'Declared metadata source for this provenance record.',
    'extraction_method': 'Extraction strategy used for this provenance record.',
    'generated_at': 'Timestamp when this provenance record was generated.',
    'generator_version': 'Version of the extractor/generator that produced this record.',
    'email': 'Email address for a maintainer/author contact.',
    'affiliation': 'Organization or affiliation for a maintainer/author.',
    'role': 'Role label for a maintainer/author in plugin lifecycle.',
}

SLOT_URIS = {
    'id': 'schema_org:identifier',
    'name': 'schema_org:name',
    'description': 'schema_org:description',
    'subject': 'dc_terms:subject',
    'license': 'schema_org:license',
    'upstream_repository': 'schema_org:codeRepository',
    'documentation': 'schema_org:url',
    'homepage': 'schema_org:url',
}

REQUIRED_SLOTS_BY_CLASS = {
    'PluginMetadata': {
        'id',
        'metadata_schema_version',
        'name',
        'upstream_repository',
        'maturity',
    },
    'EntryPoint': {
        'id',
        'entry_point_group',
        'entry_point_name',
        'python_object',
        'capability_type',
    },
    'PluginCapability': {'id', 'capability_type', 'title'},
    'FileFormatSupport': {'id', 'label'},
    'SchemaDependency': {'dependency_type', 'package_name'},
    'SuggestedUsage': {'id', 'title', 'user_intent', 'domain_category', 'maturity'},
    'MetadataProvenance': {'source', 'extraction_method', 'generated_at'},
}

ENUM_VALUES = {
    'CapabilityType': sp.CAPABILITY_TYPES,
    'DomainCategory': sp.DOMAIN_CATEGORIES,
    'MaturityLevel': sp.MATURITY_LEVELS,
    'DependencyType': sp.DEPENDENCY_TYPES,
    'MetadataSource': sp.METADATA_SOURCES,
    'ExtractionMethod': sp.EXTRACTION_METHODS,
    'CompressionType': sp.COMPRESSION_TYPES,
}

ENUM_BY_SLOT = {
    'capability_type': 'CapabilityType',
    'domain_category': 'DomainCategory',
    'maturity': 'MaturityLevel',
    'dependency_type': 'DependencyType',
    'source': 'MetadataSource',
    'extraction_method': 'ExtractionMethod',
    'compression_support': 'CompressionType',
}


def _linkml_class_name(nomad_class_name: str) -> str:
    if nomad_class_name == ROOT_NOMAD_CLASS_NAME:
        return ROOT_CLASS_NAME
    return nomad_class_name


def _is_list_quantity(quantity: Quantity) -> bool:
    shape = getattr(quantity, 'shape', None)
    return shape == ['*']


def _range_from_quantity(slot_name: str, quantity: Quantity) -> str:
    q_type = getattr(quantity, 'type', None)
    if slot_name in ENUM_BY_SLOT or isinstance(q_type, MEnum):
        range_name = ENUM_BY_SLOT.get(slot_name, 'string')
    elif q_type is str:
        range_name = 'string'
    elif q_type is int or str(q_type).startswith('m_int'):
        range_name = 'integer'
    elif q_type is bool or str(q_type).startswith('m_bool'):
        range_name = 'boolean'
    # NOMAD Datetime quantity type.
    elif 'Datetime' in str(q_type):
        range_name = 'datetime'
    else:
        range_name = 'string'
    return range_name


def _render_slot(
    slot_name: str, *, range_name: str, required: bool, multivalued: bool
) -> dict:
    slot: dict = {
        'required': bool(required),
    }
    if slot_name == 'id':
        slot['identifier'] = True
    if multivalued:
        slot['multivalued'] = True
    if range_name != 'string':
        slot['range'] = range_name
    if slot_name in SLOT_URIS:
        slot['slot_uri'] = SLOT_URIS[slot_name]
    if slot_name in SLOT_DESCRIPTIONS:
        slot['description'] = SLOT_DESCRIPTIONS[slot_name]
    return slot


def _record_slot_tracking(
    *,
    slot_name: str,
    linkml_class_name: str,
    required_in_class: bool,
    slot_to_classes: dict[str, set[str]],
    slot_required_by_class: dict[str, set[str]],
) -> None:
    slot_to_classes.setdefault(slot_name, set()).add(linkml_class_name)
    if required_in_class:
        slot_required_by_class.setdefault(slot_name, set()).add(linkml_class_name)


def _build_quantity_slot(
    *,
    class_name: str,
    attr_name: str,
    attr_value: Quantity,
) -> tuple[dict, bool]:
    required_in_class = attr_name in REQUIRED_SLOTS_BY_CLASS.get(class_name, set())
    slot = _render_slot(
        attr_name,
        range_name=_range_from_quantity(attr_name, attr_value),
        required=required_in_class,
        multivalued=_is_list_quantity(attr_value),
    )
    return slot, required_in_class


def _build_subsection_slot(
    *,
    class_name: str,
    attr_name: str,
    attr_value: SubSection,
) -> tuple[dict, bool]:
    section_cls = getattr(attr_value, 'section', None)
    section_name = (
        getattr(section_cls, '__name__', None)
        or getattr(section_cls, 'name', None)
        or 'string'
    )
    repeats = bool(getattr(attr_value, 'repeats', False))
    required_in_class = attr_name in REQUIRED_SLOTS_BY_CLASS.get(class_name, set())
    slot = _render_slot(
        attr_name,
        range_name=_linkml_class_name(section_name),
        required=required_in_class,
        multivalued=repeats,
    )
    if repeats:
        slot['inlined_as_list'] = True
    return slot, required_in_class


def _finalize_requiredness(
    *,
    classes: dict,
    slots: dict,
    slot_to_classes: dict[str, set[str]],
    slot_required_by_class: dict[str, set[str]],
) -> None:
    # Avoid over-constraining shared slots globally; put class-specific requiredness
    # into slot_usage when a slot is required only in a subset of classes.
    for slot_name, owner_classes in slot_to_classes.items():
        required_classes = slot_required_by_class.get(slot_name, set())
        globally_required = required_classes == owner_classes and bool(owner_classes)
        slots[slot_name]['required'] = globally_required
        if globally_required:
            continue
        for class_name in sorted(required_classes):
            class_payload = classes[class_name]
            slot_usage = class_payload.setdefault('slot_usage', {})
            slot_usage[slot_name] = {'required': True}


def generate_linkml_schema() -> dict:
    classes: dict = {}
    slots: dict = {}
    slot_to_classes: dict[str, set[str]] = {}
    slot_required_by_class: dict[str, set[str]] = {}

    for class_name in CLASS_ORDER:
        cls = getattr(sp, class_name)
        linkml_class_name = _linkml_class_name(class_name)
        class_slots: list[str] = []
        class_payload: dict = {}
        if linkml_class_name == ROOT_CLASS_NAME:
            class_payload['tree_root'] = True
            class_payload['close_mappings'] = ['schema_org:SoftwareApplication']
        if linkml_class_name in CLASS_DESCRIPTIONS:
            class_payload['description'] = CLASS_DESCRIPTIONS[linkml_class_name]

        for attr_name, attr_value in cls.__dict__.items():
            if attr_name.startswith('_'):
                continue

            if isinstance(attr_value, Quantity):
                class_slots.append(attr_name)
                slot, required_in_class = _build_quantity_slot(
                    class_name=class_name,
                    attr_name=attr_name,
                    attr_value=attr_value,
                )
                slots[attr_name] = slot
                _record_slot_tracking(
                    slot_name=attr_name,
                    linkml_class_name=linkml_class_name,
                    required_in_class=required_in_class,
                    slot_to_classes=slot_to_classes,
                    slot_required_by_class=slot_required_by_class,
                )
                continue

            if isinstance(attr_value, SubSection):
                class_slots.append(attr_name)
                slot, required_in_class = _build_subsection_slot(
                    class_name=class_name,
                    attr_name=attr_name,
                    attr_value=attr_value,
                )
                slots[attr_name] = slot
                _record_slot_tracking(
                    slot_name=attr_name,
                    linkml_class_name=linkml_class_name,
                    required_in_class=required_in_class,
                    slot_to_classes=slot_to_classes,
                    slot_required_by_class=slot_required_by_class,
                )

        class_payload['slots'] = class_slots
        classes[linkml_class_name] = class_payload

    _finalize_requiredness(
        classes=classes,
        slots=slots,
        slot_to_classes=slot_to_classes,
        slot_required_by_class=slot_required_by_class,
    )

    enums = {
        enum_name: {'permissible_values': {value: {} for value in values}}
        for enum_name, values in ENUM_VALUES.items()
    }

    schema = {
        'title': 'NOMAD Plugin Metadata Schema',
        'name': 'nomad_plugin_metadata',
        'version': SCHEMA_VERSION,
        'id': 'https://fairmat-nfdi.github.io/nomad-plugins-metadata/schema/nomad_plugin_metadata',
        'prefixes': {
            'linkml': 'https://w3id.org/linkml/',
            'schema_org': 'http://schema.org/',
            'dc_terms': 'http://purl.org/dc/terms/',
            'nomadpm': 'https://fairmat-nfdi.github.io/nomad-plugins-metadata/schema/',
        },
        'default_prefix': 'nomadpm',
        'emit_prefixes': ['nomadpm'],
        'imports': ['linkml:types'],
        'default_range': 'string',
        'description': (
            'Generated from NOMAD metainfo classes in schema_package.py. '
            'This LinkML export is the interoperability artifact for validation/docs.'
        ),
        'classes': classes,
        'slots': slots,
        'enums': enums,
    }
    return schema


def export_linkml_schema(path: Path = SCHEMA_PATH) -> None:
    payload = generate_linkml_schema()
    with path.open('w', encoding='utf-8') as f:
        f.write('# AUTO-GENERATED FROM schema_package.py. DO NOT EDIT DIRECTLY.\n')
        yaml.safe_dump(
            payload,
            f,
            sort_keys=False,
            allow_unicode=False,
            default_flow_style=False,
        )


def is_export_current(path: Path = SCHEMA_PATH) -> bool:
    if not path.exists():
        return False
    with path.open('r', encoding='utf-8') as f:
        existing = yaml.safe_load(f)
    return existing == generate_linkml_schema()
