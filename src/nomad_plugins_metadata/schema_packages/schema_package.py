from typing import TYPE_CHECKING

from nomad.datamodel.data import ArchiveSection, Schema
from nomad.metainfo import Datetime, MEnum, Quantity, SchemaPackage, SubSection

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

m_package = SchemaPackage()

CAPABILITY_TYPES = (
    'parser',
    'schema',
    'app',
    'normalizer',
    'example_upload',
    'api',
    'north_tool',
    'tool',
)
DOMAIN_CATEGORIES = (
    'simulations',
    'measurements',
    'synthesis',
    'cross-domain',
    'workflow',
    'infrastructure',
)
MATURITY_LEVELS = ('alpha', 'beta', 'stable', 'archived')
DEPENDENCY_TYPES = ('nomad_plugin', 'python_package')
METADATA_SOURCES = (
    'manual_override',
    'plugin_entry_points',
    'pyproject',
    'citation_cff',
    'repository_api',
    'crawler_fallback',
)
EXTRACTION_METHODS = ('deterministic', 'heuristic', 'manual')
COMPRESSION_TYPES = ('gz', 'bz2', 'xz', 'zip', 'tar')


class Maintainer(ArchiveSection):
    name = Quantity(type=str)
    email = Quantity(type=str)
    affiliation = Quantity(type=str)
    role = Quantity(type=str)


class EntryPoint(ArchiveSection):
    id = Quantity(type=str)
    entry_point_group = Quantity(type=str)
    entry_point_name = Quantity(type=str)
    python_object = Quantity(type=str)
    capability_type = Quantity(type=MEnum(*CAPABILITY_TYPES))


class ParserCapabilityDetails(ArchiveSection):
    parser_name = Quantity(type=str)
    mainfile_name_re = Quantity(type=str)
    mainfile_contents_re = Quantity(type=str)
    mainfile_mime_re = Quantity(type=str)
    mainfile_binary_header = Quantity(type=str)
    compression_support = Quantity(type=MEnum(*COMPRESSION_TYPES), shape=['*'])
    auxiliary_file_patterns = Quantity(type=str, shape=['*'])


class PluginCapability(ArchiveSection):
    id = Quantity(type=str)
    capability_type = Quantity(type=MEnum(*CAPABILITY_TYPES))
    title = Quantity(type=str)
    summary = Quantity(type=str)
    parser_details = SubSection(section=ParserCapabilityDetails)


class FileFormatSupport(ArchiveSection):
    id = Quantity(type=str)
    label = Quantity(type=str)
    extensions = Quantity(type=str, shape=['*'])
    mime_types = Quantity(type=str, shape=['*'])
    standard = Quantity(type=str)
    instrument_context = Quantity(type=str)
    notes = Quantity(type=str)


class SchemaDependency(ArchiveSection):
    dependency_type = Quantity(type=MEnum(*DEPENDENCY_TYPES))
    package_name = Quantity(type=str)
    version_range = Quantity(type=str)
    optional = Quantity(type=bool)
    purpose = Quantity(type=str)


class SuggestedUsage(ArchiveSection):
    id = Quantity(type=str)
    title = Quantity(type=str)
    user_intent = Quantity(type=str)
    domain_category = Quantity(type=MEnum(*DOMAIN_CATEGORIES))
    technique = Quantity(type=str)
    audience = Quantity(type=str)
    maturity = Quantity(type=MEnum(*MATURITY_LEVELS))
    tags = Quantity(type=str, shape=['*'])


class DeploymentInfo(ArchiveSection):
    on_central = Quantity(type=bool)
    on_example_oasis = Quantity(type=bool)
    on_pypi = Quantity(type=bool)
    pypi_package = Quantity(type=str)


class ReleaseContext(ArchiveSection):
    release_tag = Quantity(type=str)
    release_commit_sha = Quantity(type=str)


class MetadataProvenance(ArchiveSection):
    source = Quantity(type=MEnum(*METADATA_SOURCES))
    extraction_method = Quantity(type=MEnum(*EXTRACTION_METHODS))
    generated_at = Quantity(type=Datetime)
    generator_version = Quantity(type=str)


class PluginMetadata(Schema):
    id = Quantity(type=str)
    metadata_schema_version = Quantity(type=str)
    name = Quantity(type=str)
    description = Quantity(type=str)
    plugin_version = Quantity(type=str)
    subject = Quantity(type=str, shape=['*'])
    license = Quantity(type=str)
    upstream_repository = Quantity(type=str)
    documentation = Quantity(type=str)
    homepage = Quantity(type=str)
    issue_tracker = Quantity(type=str)
    owner = Quantity(type=str)
    owner_type = Quantity(type=str)
    stars = Quantity(type=int)
    created = Quantity(type=Datetime)
    last_updated = Quantity(type=Datetime)
    archived = Quantity(type=bool)
    repository_default_branch = Quantity(type=str)
    supported_filetypes = Quantity(type=str, shape=['*'])
    maturity = Quantity(type=MEnum(*MATURITY_LEVELS))

    maintainers = SubSection(section=Maintainer, repeats=True)
    authors = SubSection(section=Maintainer, repeats=True)
    entry_points = SubSection(section=EntryPoint, repeats=True)
    capabilities = SubSection(section=PluginCapability, repeats=True)
    file_format_support = SubSection(section=FileFormatSupport, repeats=True)
    schema_dependencies = SubSection(section=SchemaDependency, repeats=True)
    suggested_usages = SubSection(section=SuggestedUsage, repeats=True)
    deployment = SubSection(section=DeploymentInfo)
    release_context = SubSection(section=ReleaseContext)
    metadata_provenance = SubSection(section=MetadataProvenance, repeats=True)

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)
        logger.info('PluginMetadata.normalize', plugin=self.name, plugin_id=self.id)


m_package.__init_metainfo__()
