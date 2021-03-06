import logging

from .config import Config
from .action_base import ActionBase

config = Config()
config.config_init()
log_name = config.log_config['log-name']
log = logging.getLogger(log_name or __name__)


class AcquireMaster(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(AcquireMaster, self).__init__(*args, **kwargs)
        default_values = self.fetch_resource_purge_map()
        self.instruction_set = default_values['instruction_set']
        return res

    # FETCHERS

    def fetch_resource_purge_map(self):
        log.debug('AcquireMaster')
        return {
            'instruction_set': {
                "controller": "client",
                "ctype": "action",
                "action": "acquire",
                "acquire": "master",
            }
        }

    def fetch_resource_key_map(self):
        log.debug('AcquireMaster')
        return {
            'instruction_set': '<instruction-set type-dict>',
            'client_id': '<client-id type-str>',
            'session_token': '<session-token type-str>',
            'master': '<email-address type-str>',
            'key': '<master-key-code type-str>',
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('AcquireMaster')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(AcquireMaster, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, *args, **kwargs):
        log.debug('AcquireMaster')
        instruction_set = self.fetch_instruction_set() \
            if not args or not isinstance(args[0], dict) else args[0]
        return super(AcquireMaster, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('AcquireMaster')
        valid_keys = list(self.fetch_resource_key_map().keys())
        return super(AcquireMaster, self).set_values(
            value_set, valid_keys=valid_keys, *args, **kwargs
        )
