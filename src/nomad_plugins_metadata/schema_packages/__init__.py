from nomad.config.models.plugins import SchemaPackageEntryPoint


class PluginMetadataSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_plugins_metadata.schema_packages.schema_package import m_package

        return m_package


schema_package_entry_point = PluginMetadataSchemaPackageEntryPoint(
    name='PluginMetadata',
    description='Schema package for canonical NOMAD plugin metadata.',
)
