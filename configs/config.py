import os
from simpleconfigparser import simpleconfigparser

__AUTHOR__ = "RAMESH KUMAR"


def init():
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    configs = simpleconfigparser()
    configs.read(APP_ROOT + '/config.ini')
    global config_dict
    config_dict = {s: dict(configs.items(s)) for s in configs.sections()}
    env_path_name = "DATA_CONFIGS"
    if env_path_name in os.environ and os.environ[env_path_name]:
        custom_config_path = os.environ[env_path_name]
        sconfigs = simpleconfigparser()
        sconfigs.read(custom_config_path)
        local_config_dict = {
            s: dict(sconfigs.items(s))
            for s in sconfigs.sections()
        }
        for key, val in local_config_dict.iteritems():
            if key not in config_dict:
                config_dict[key] = val
            else:
                config_dict[key].update(val)


if 'config_dict' not in globals():
    init()
