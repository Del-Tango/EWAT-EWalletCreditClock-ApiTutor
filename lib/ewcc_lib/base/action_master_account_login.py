import logging

from .config import Config
from .action_base import ActionBase

config = Config()
config.config_init()
log_name = config.log_config['log-name']
log = logging.getLogger(log_name or __name__)


class MasterAccountLogin(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(MasterAccountLogin, self).__init__(*args, **kwargs)
        default_values = self.fetch_resource_purge_map()
        self.instruction_set = default_values['instruction_set']
        return res

    # FETCHERS

    def fetch_resource_purge_map(self):
        log.debug('MasterAccountLogin')
        return {
            'instruction_set': {
                "controller": "master",
                "ctype": "action",
                "action": "login",
            }
        }

    def fetch_resource_key_map(self):
        log.debug('MasterAccountLogin')
        return {
            'instruction_set': '<instruction-set type-dict>',
            'client_id': '<client-id type-str>',
            'session_token': '<session-token type-str>',
            'user_email': '<email-address type-str>',
            'user_pass': '<password type-str>',
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('MasterAccountLogin')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(MasterAccountLogin, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, *args, **kwargs):
        log.debug('MasterAccountLogin')
        instruction_set = self.fetch_instruction_set() \
            if not args or not isinstance(args[0], dict) else args[0]
        return super(MasterAccountLogin, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('MasterAccountLogin')
        valid_keys = list(self.fetch_resource_key_map().keys())
        return super(MasterAccountLogin, self).set_values(
            value_set, valid_keys=valid_keys, *args, **kwargs
        )
