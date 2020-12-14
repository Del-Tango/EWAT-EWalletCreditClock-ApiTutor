import datetime
import logging

from .config import Config
from .action_base import ActionBase

config = Config()
config.config_init()
log_name = config.log_config['log-name']
log = logging.getLogger(log_name or __name__)


class CheckCTokenSession(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(CheckCTokenSession, self).__init__(*args, **kwargs)
        self.instruction_set = {
            'controller': 'client',
            'ctype': 'action',
            'action': 'verify',
            'verify': 'ctoken',
            'ctoken': 'session',
        }
        return res

    # FETCHERS

    def fetch_resource_purge_map(self):
        log.debug('CheckCTokenSession')
        return {
            'instruction_set': {
                'controller': 'client',
                'ctype': 'action',
                'action': 'verify',
                'verify': 'ctoken',
                'ctoken': 'session',
            }
        }

    def fetch_resource_key_map(self):
        log.debug('CheckCTokenSession')
        return {
            'instruction_set': '<instruction-set type-dict>',
            'client_id': 'client-id type-str>',
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('CheckCTokenSession')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(CheckCTokenSession, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, **kwargs):
        log.debug('CheckCTokenSession')
        instruction_set = self.fetch_instruction_set()
        return super(CheckCTokenSession, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('CheckCTokenSession')
        valid_keys = list(self.fetch_resource_key_map().keys())
        return super(CheckCTokenSession, self).set_values(
            value_set, valid_keys=valid_keys, *args, **kwargs
        )

