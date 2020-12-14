import datetime
import logging

from .config import Config
from .resource_base import ResourceBase

config = Config()
config.config_init()
log_name = config.log_config['log-name']
log = logging.getLogger(log_name or __name__)


class ActionBase(ResourceBase):

    def __init__(self, *args, **kwargs):
        log.debug('ActionBase')
        return super(ActionBase, self).__init__(*args, **kwargs)

    def check_for_illegal_instruction_set_keys(self, instruction_keys, valid_key_set):
        log.debug('ActionBase')
        valid_keys, invalid_keys = [], []
        for key in instruction_keys:
            if key not in valid_key_set:
                self.warning_illegal_instruction_set_key_for_resource(
                    instruction_keys, valid_key_set
                )
                invalid_keys.append(key)
                continue
            valid_keys.append(key)
        return {
            'failed': False,
            'valid_keys': valid_keys,
            'invalid_keys': invalid_keys,
        }

    def execute(self, *args, **kwargs):
        log.debug('ActionBase')
        return super(ActionBase, self).execute(*args, **kwargs)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('ActionBase')
        if not kwargs.get('valid_keys') and \
                not isinstance(kwargs.get('valid_keys'), list):
            return self.error_no_valid_instruction_keys_found_for_resource(
                value_set, args, kwargs
            )
        check_illegal_keys = self.check_for_illegal_instruction_set_keys(
            value_set, kwargs['valid_keys']
        )
        if isinstance(check_illegal_keys, dict) and \
                (check_illegal_keys.get('failed') or \
                check_illegal_keys.get('invalid_keys')):
            return self.error_illegal_instruction_set_keys_found(
                value_set, args, kwargs, check_illegal_keys
            )
        return super(ActionBase, self).set_values(value_set, *args, **kwargs)

    # WARNINGS
    '''
    [ TODO ]: Fetch all warning messages from message file by key codes.
    '''

    def warning_illegal_instruction_set_key_for_resource(self, *args):
        core_response = {
            'failed': True,
            'level': 'action-base',
            'warning': 'Illegal instruction set key found '
                       'for user action handler. '
                       'Details: {}'.format(args)
        }
        log.warning(core_response['warning'])
        return core_response

    # ERRORS
    '''
    [ TODO ]: Fetch all error messages from message file by key codes.
    '''

    def error_no_valid_instruction_keys_found_for_resource(self, *args):
        core_response = {
            'failed': True,
            'level': 'action-base',
            'error': 'Something went wrong. '
                     'No valid resource instruction set keys found. '
                     'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response

    def error_illegal_instruction_set_keys_found(self, *args):
        core_response = {
            'failed': True,
            'level': 'action-base',
            'error': 'Illegal instruction set keys found for '
                     'user action handler. '
                     'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response

# CODE DUMP

