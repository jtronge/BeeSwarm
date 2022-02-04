import beeswarm


def test_config_0():
    conf = beeswarm.Config(
        {
            'name': '$name',
            'inner_key': {
                'value': '$value',
                'some_value': 88,
            },
        },
        {
            'name': 'some name',
            'value': 'some value',
        },
    )

    assert conf['name'] == 'some name'
    assert conf['inner_key']['value'] == 'some value'
    assert conf['inner_key']['some_value'] == 88
    assert conf.resolve_key('name') == 'some name'
    assert conf.resolve_key('inner_key.value') == 'some value'
    assert conf.resolve_key('inner_key.some_value') == 88
