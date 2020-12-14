import logging

from .config import Config
from .action_base import ActionBase

config = Config()
config.config_init()
log_name = config.log_config['log-name']
log = logging.getLogger(log_name or __name__)


class TransferCredits(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(TransferCredits, self).__init__(*args, **kwargs)
        default_values = self.fetch_resource_purge_map()
        self.instruction_set = default_values['instruction_set']
        return res

    # FETCHERS

    def fetch_resource_purge_map(self):
        log.debug('TransferCredits')
        return {
            'instruction_set': {
                "controller": "client",
                "ctype": "action",
                "action": "transfer",
                "transfer": "credits",
            }
        }

    def fetch_resource_key_map(self):
        log.debug('TransferCredits')
        return {
            'instruction_set': '<instruction-set type-dict>',
            'client_id': '<client_id type-str>',
            'session_token': '<session_token type-str>',
            'credits': '<number-of-credits type-int>',
            'transfer_to': '<email-address type-str>',
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('TransferCredits')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(TransferCredits, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, *args, **kwargs):
        log.debug('TransferCredits')
        instruction_set = self.fetch_instruction_set() \
            if not args or not isinstance(args[0], dict) else args[0]
        return super(TransferCredits, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('TransferCredits')
        valid_keys = list(self.fetch_resource_key_map().keys())
        return super(TransferCredits, self).set_values(
            value_set, valid_keys=valid_keys, *args, **kwargs
        )
