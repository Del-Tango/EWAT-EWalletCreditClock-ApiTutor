import datetime
import logging

from .config import Config
from .action_base import ActionBase

config = Config()
config.config_init()
log_name = config.log_config['log-name']
log = logging.getLogger(log_name or __name__)


class CheckSTokenLinked(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(CheckSTokenLinked, self).__init__(*args, **kwargs)
        self.instruction_set = {
            'controller': 'client',
            'ctype': 'action',
            'action': 'verify',
            'verify': 'stoken',
            'stoken': 'linked',
        }
        return res

    # FETCHERS

    def fetch_resource_purge_map(self):
        log.debug('CheckSTokenLinked')
        return {
            'instruction_set': {
                'controller': 'client',
                'ctype': 'action',
                'action': 'verify',
                'verify': 'stoken',
                'stoken': 'linked',
            }
        }

    def fetch_resource_key_map(self):
        log.debug('CheckSTokenLinked')
        return {
            'instruction_set': '<instruction-set type-dict>',
            'session_token': '<session_token type-str>',
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('CheckSTokenLinked')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(CheckSTokenLinked, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, **kwargs):
        log.debug('CheckSTokenLinked')
        instruction_set = self.fetch_instruction_set()
        return super(CheckSTokenLinked, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('CheckSTokenLinked')
        valid_keys = list(self.fetch_resource_key_map().keys())
        return super(CheckSTokenLinked, self).set_values(
            value_set, valid_keys=valid_keys, *args, **kwargs
        )

