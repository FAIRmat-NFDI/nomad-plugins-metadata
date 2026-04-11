from nomad_plugins_metadata.schema_packages.schema_validation import load_schema


def test_datatractor_compatibility_fields_exist():
    schema = load_schema()
    plugin_package_slots = set(schema['classes']['PluginPackage']['slots'])
    expected_slots = {
        'id',
        'name',
        'description',
        'subject',
        'license',
        'upstream_repository',
        'documentation',
        'supported_filetypes',
    }
    assert expected_slots.issubset(plugin_package_slots)


def test_datatractor_filetype_shape_is_compatible():
    schema = load_schema()
    supported_filetypes = schema['slots']['supported_filetypes']
    assert supported_filetypes.get('range', 'string') == 'string'
    assert supported_filetypes.get('multivalued', False) is True
