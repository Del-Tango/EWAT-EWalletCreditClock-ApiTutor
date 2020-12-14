import datetime
import logging

from .config import Config
from .action_base import ActionBase

config = Config()
config.config_init()
log_name = config.log_config['log-name']
log = logging.getLogger(log_name or __name__)


class RequestClientID(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(RequestClientID, self).__init__(*args, **kwargs)
        self.instruction_set = {
            'controller': 'client',
            'ctype': 'action',
            'action': 'request',
            'request': 'client_id',
        }
        return res

    # FETCHERS

    def fetch_resource_purge_map(self):
        log.debug('RequestClientID')
        value_set = {
            'instruction_set': {
                'controller': 'client',
                'ctype': 'action',
                'action': 'request',
                'request': 'client_id',
            },
        }
        return value_set

    def fetch_resource_key_map(self):
        log.debug('RequestClientID')
        return {
            'instruction_set': '<instruction-set type-dict>',
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('RequestClientID')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(RequestClientID, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, *args, **kwargs):
        log.debug('RequestClientID')
        instruction_set = self.fetch_instruction_set()
        return super(RequestClientID, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('RequestClientID')
        valid_keys = list(self.fetch_resource_key_map().keys())
        return super(RequestClientID, self).set_values(
            value_set, valid_keys=valid_keys, *args, **kwargs
        )

