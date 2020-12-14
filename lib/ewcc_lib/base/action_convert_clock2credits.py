import logging

from .config import Config
from .action_base import ActionBase

config = Config()
config.config_init()
log_name = config.log_config['log-name']
log = logging.getLogger(log_name or __name__)


class ConvertClockToCredits(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(ConvertClockToCredits, self).__init__(*args, **kwargs)
        default_values = self.fetch_resource_purge_map()
        self.instruction_set = default_values['instruction_set']
        return res

    # FETCHERS

    def fetch_resource_purge_map(self):
        log.debug('ConvertClockToCredits')
        return {
            'instruction_set': {
                "controller": "client",
                "ctype": "action",
                "action": "convert",
                "convert": "clock2credits",
            }
        }

    def fetch_resource_key_map(self):
        log.debug('ConvertClockToCredits')
        return {
            'instruction_set': '<instruction-set type-dict>',
            'client_id': '<client_id type-str>',
            'session_token': '<session_token type-str>',
            'minutes': '<number-of-minutes type-float>',
            'notes': '<conversion-notes type-str>',
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('ConvertClockToCredits')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(ConvertClockToCredits, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, *args, **kwargs):
        log.debug('ConvertClockToCredits')
        instruction_set = self.fetch_instruction_set() \
            if not args or not isinstance(args[0], dict) else args[0]
        return super(ConvertClockToCredits, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('ConvertClockToCredits')
        valid_keys = list(self.fetch_resource_key_map().keys())
        return super(ConvertClockToCredits, self).set_values(
            value_set, valid_keys=valid_keys, *args, **kwargs
        )
