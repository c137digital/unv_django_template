from unv.app.settings import ComponentSettings


class ExampleSettings(ComponentSettings):
    KEY = 'example'
    SCHEMA = {
        "somevar": {
            "type": "string",
            "required": False
        }
    }
    DEFAULT = {
        'somevar': 'undefined',
    }


SETTINGS = ExampleSettings()
