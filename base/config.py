import configparser

config = configparser.ConfigParser()
config._interpolation = configparser.ExtendedInterpolation()
config.read('conf/ewat.conf')


class Config():

    def __init__(self, *args, **kwargs):
        self.remote_machine_details = {
            'server-address': config['RemoteMachineDetails']['server_address'],
            'server-port': config['RemoteMachineDetails'].getint('server_port'),
            'ewallet-path': config['RemoteMachineDetails'].get('ewallet_path'),
            'instruction-set-path': config['RemoteMachineDetails'].get('instruction_set_path'),
            'target-url': config['RemoteMachineDetails'].get('target_url'),
        }
        self.log_config = {
            'log-name': config['LogDetails']['log_name'],
            'log-level':config['LogDetails']['log_level'],
            'log-file': config['LogDetails']['log_file'],
            'log-dir': config['LogDetails']['log_dir'],
            'log-path': config['LogDetails'].get('log_path'),
            'log-record-format': "[ %(asctime)s ] %(name)s [ %(levelname)s ] - %(filename)s - %(lineno)d: %(funcName)s - %(message)s",
            'log-date-format': "%Y-%m-%d %H:%M:%S",
        }
