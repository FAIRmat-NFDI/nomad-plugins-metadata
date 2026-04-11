from nomad_plugins_metadata.schema_packages.schema_validation import load_schema


def _required_in_plugin_package(schema: dict, slot_name: str) -> bool:
    slot_required = bool(schema['slots'][slot_name].get('required', False))
    usage_required = bool(
        schema['classes']['PluginPackage']
        .get('slot_usage', {})
        .get(slot_name, {})
        .get('required', False)
    )
    return slot_required or usage_required


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


def test_datatractor_direct_field_contract():
    schema = load_schema()
    field_contract = {
        'id': {
            'required': True,
            'multivalued': False,
            'range': 'string',
            'slot_uri': 'schema_org:identifier',
        },
        'name': {
            'required': True,
            'multivalued': False,
            'range': 'string',
            'slot_uri': 'schema_org:name',
        },
        'description': {
            'required': False,
            'multivalued': False,
            'range': 'string',
            'slot_uri': 'schema_org:description',
        },
        'subject': {
            'required': False,
            'multivalued': True,
            'range': 'string',
            'slot_uri': 'dc_terms:subject',
        },
        'license': {
            'required': False,
            'multivalued': False,
            'range': 'string',
            'slot_uri': 'schema_org:license',
        },
        'upstream_repository': {
            'required': True,
            'multivalued': False,
            'range': 'string',
            'slot_uri': 'schema_org:codeRepository',
        },
        'documentation': {
            'required': False,
            'multivalued': False,
            'range': 'string',
            'slot_uri': 'schema_org:url',
        },
        'supported_filetypes': {
            'required': False,
            'multivalued': True,
            'range': 'string',
        },
    }

    for field_name, expected in field_contract.items():
        field = schema['slots'][field_name]
        assert _required_in_plugin_package(schema, field_name) is expected['required']
        assert bool(field.get('multivalued', False)) is expected['multivalued']
        assert field.get('range', 'string') == expected['range']
        if 'slot_uri' in expected:
            assert field.get('slot_uri') == expected['slot_uri']


def test_datatractor_required_enum_members_present():
    schema = load_schema()
    required_members = {
        'CapabilityType': {'parser'},
        'MaturityLevel': {'alpha', 'beta', 'stable', 'archived'},
        'DomainCategory': {
            'simulations',
            'measurements',
            'synthesis',
            'cross-domain',
            'workflow',
            'infrastructure',
        },
    }

    for enum_name, required_values in required_members.items():
        enum_values = set(schema['enums'][enum_name]['permissible_values'].keys())
        assert required_values.issubset(enum_values)
