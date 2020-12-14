import datetime
import logging
import requests
import json
import pysnooper

from base64 import b64encode

from .config import Config

config = Config()
config.config_init()
log_name = config.log_config['log-name']
log = logging.getLogger(log_name or __name__)


class ResourceBase():

    def __init__(self, *args, **kwargs):
        self.create_date = datetime.datetime.now()
        self.write_date = datetime.datetime.now()
        self.config = kwargs.get('config') #config if not kwargs.get('config') else config
        self.instruction_set = dict()
        self.instruction_set_response = dict()
        self.response = None
        self.timestamp = None
        self.status = bool()
        self.previous_label = str()

    # FETCHERS

    def fetch_resource_instruction_set(self):
        log.debug('ResourceBase')
        return self.instruction_set

    def fetch_resource_purge_map(self):
        log.debug('ResourceBase')
        return {
            'write_date': datetime.datetime.now(),
            'instruction_set_response': dict(),
            'response': None,
            'timestamp': None,
            'status': bool(),
            'previous_label': str(),
        }

    def fetch_resource_values(self):
        log.debug('ResourceBase')
        return {
            'create_date': self.create_date,
            'write_date': self.write_date,
            'instruction_set': self.instruction_set,
            'instruction_set_response': self.instruction_set_response,
            'response': self.response,
            'timestamp': self.timestamp,
            'status': self.status,
            'previous_label': self.previous_label,
        }

    def fetch_instruction_set(self):
        log.debug('ResourceBase')
        instruction_set = self.instruction_set
        if not isinstance(instruction_set, dict):
            return self.error_instruction_set_parameter_not_properly_set(
                instruction_set
            )
        elif not instruction_set:
            return self.warning_unpopulated_instruction_set(instruction_set)
        return instruction_set

    def fetch_supported_http_request_methods(self):
        log.debug('ResourceBase')
        return ['POST', 'GET']

#   @pysnooper.snoop()
    def fetch_action_instruction_set_target_url(self):
        log.debug('ResourceBase')
        return self.config.cloud_config['ewsc-url']

    # FORMATTERS

    def format_master_account_credentials_for_basic_auth(self, login, sequence):
        log.debug('ResourceBase')
        if not isinstance(login, str) or not isinstance(sequence, str):
            return self.error_invalid_basic_http_authorization_credentials(login, sequence)
        master_creds = '{}:{}'.format(login, sequence)
        encoded_creds = master_creds.encode('UTF-8')
        basic_auth_creds = b64encode(encoded_creds).decode('ascii')
        return basic_auth_creds or False

    def format_data_set_for_api_call(self, values):
        log.debug('ResourceBase')
        master_creds = self.format_master_account_credentials_for_basic_auth(
            self.config._fetch_ewsc_master_login(),
            self.config._fetch_ewsc_master_sequence()
        )
        if not master_creds or not isinstance(master_creds, str):
            return self.error_could_not_format_master_account_credentials_for_authorization(
               master_creds
            )
        formatted_values = {
            'Header': {
                'Authorization': 'Basic ' + master_creds,
                'Content-Type': 'application/json',
            },
            'Body': values,
        }
        return formatted_values

    # UPDATERS

    def update_last_executed_instruction_set(self, instruction_set):
        log.debug('ResourceBase')
        try:
            self.instruction_set = instruction_set
        except:
            self.error_could_not_update_last_executed_instruction_set(instruction_set)
            return False
        return True

    def update_last_write_date(self):
        log.debug('ResourceBase')
        try:
            self.write_date = datetime.datetime.now()
        except:
            self.error_could_not_update_last_resource_write_date()
            return False
        return True

    def update_last_ewsc_response_raw(self, response):
        log.debug('ResourceBase')
        try:
            self.response = response
        except:
            self.error_could_not_update_last_ewsc_response_raw(response)
            return False
        return True

    def update_last_ewsc_instruction_set_response(self, response):
        log.debug('ResourceBase')
        try:
            self.instruction_set_response = self.json_to_dictionary_convertor(response.text)
        except:
            self.error_could_not_update_last_ewsc_instruction_set_response(response)
            return False
        return True

    def update_last_ewsc_response_status(self, instruction_set_response):
        log.debug('ResourceBase')
        try:
            self.status = False if instruction_set_response.get('failed') \
                else True
        except:
            self.error_could_not_update_last_ewsc_response_status(
                instruction_set_response
            )
            return False
        return True

    def update_last_instruction_set_execution_timestamp(self):
        log.debug('ResourceBase')
        try:
            self.timestamp = datetime.datetime.now()
        except:
            self.error_could_not_update_last_instruction_set_execution_timestamp()
            return False
        return True

    def update_last_ewsc_response(self, instruction_set, response):
        log.debug('ResourceBase')
        updates = {
            'response': self.update_last_ewsc_response_raw(response),
            'instruction_set': self.update_last_executed_instruction_set(instruction_set),
            'instruction_set_response': self.update_last_ewsc_instruction_set_response(response),
            'status': self.update_last_ewsc_response_status(self.instruction_set_response),
            'timestamp': self.update_last_instruction_set_execution_timestamp(),
            'write_date': self.update_last_write_date()
        }
        return self.warning_could_not_update_last_ewsc_resource_response(response) \
            if False in list(updates.values()) else {
                'failed': False,
                'updates': updates,
            }

    # GENERAL

    def dictionary_to_json_convertor(self, target_dict):
        log.debug('ResourceBase')
        try:
            converted = json.dumps(target_dict)
        except:
            return self.error_could_not_convert_dictonary_to_json(target_dict)
        return converted

    def json_to_dictionary_convertor(self, target_json):
        log.debug('ResourceBase')
        try:
            converted = json.loads(target_json)
        except:
            return self.error_could_not_convert_json_to_dictionary(target_json)
        return converted

    # CLOUD

    def issue_api_call(self, method, target_url, data_set):
        log.debug('ResourceBase')
        supported_request_methods = self.fetch_supported_http_request_methods()
        if method not in supported_request_methods:
            return self.error_unsupported_http_request_method(
                method, target_url, data_set
            )
        try:
            json_payload = self.dictionary_to_json_convertor(data_set['Body'])
            api_call = requests.request(
                method, target_url, headers=data_set['Header'],
                data=json_payload
            )
        except:
            return self.error_could_not_issue_ewsc_api_call(
                method, target_url, data_set
            )
        return api_call

    def process_api_call(self, instruction_set, response):
        log.debug('ResourceBase')
        http_response = None if not response or isinstance(response, dict) and\
                response.get('failed') else response.status_code
        log.info(
            'EWSC - HTTP Response {} -'.format(http_response)
        )
        update = self.update_last_ewsc_response(instruction_set, response)
        return self.error_no_http_response_found(
            instruction_set, response, update
        ) if not http_response else \
            self.json_to_dictionary_convertor(response.text)

    # CORE

#   @pysnooper.snoop()
    def execute(self, *args, **kwargs):
        log.debug('ResourceBase')
        instruction_set = self.fetch_resource_instruction_set() \
            if not args or not isinstance(args[0], dict) else args[0]
        if 'instruction_set' in instruction_set \
                and isinstance(instruction_set['instruction_set'], dict):
            instruction = instruction_set['instruction_set']
            del instruction_set['instruction_set']
            instruction_set.update(instruction)
        target_url = self.fetch_action_instruction_set_target_url()
        formatted_data = self.format_data_set_for_api_call(instruction_set)
        api_call = self.issue_api_call('POST', target_url, formatted_data)
        return self.process_api_call(instruction_set, api_call)

    def previous(self):
        log.debug('ResourceBase')
        previous = self.fetch_instruction_set()
        if not previous or isinstance(previous, dict) and \
                previous.get('failed'):
            return previous
        previous.update({'failed': False})
        return previous

#   @pysnooper.snoop('logs/ewcc.log')
    def purge(self, *args, **kwargs):
        log.debug('ResourceBase')
        purge_map = self.fetch_resource_purge_map()
        if kwargs.get('purge_map'):
            purge_map.update(kwargs['purge_map'])
        purge_fields = kwargs.get('purge') or purge_map.keys()
        value_set = {} if not args or not isinstance(args[0], list) else args[0]
        for item in purge_fields:
            if item not in value_set:
                value_set.update({item: purge_map[item]})
        return self.set_values(value_set, resource=True)

#   @pysnooper.snoop('logs/ewcc.log')
    def set_instructions(self, value_set, *args, **kwargs):
        log.debug('ResourceBase')
        instruction_tags = {item: value_set[item] for item in value_set} \
            if 'instruction_set' not in value_set else {
                item: value_set['instruction_set'][item]
                for item in values['instruction_set']
            }
        instructions = []
        for field in instruction_tags:
            try:
                self.instruction_set.update({field: instruction_tags[field]})
                instructions.append(field)
            except:
                self.warning_could_not_set_instruction(field)
        return {
            'failed': False if instructions else True,
            'updated': instructions,
            'instruction_set': self.instruction_set,
        }

#   @pysnooper.snoop('logs/ewcc.log')
    def set_values(self, value_set, *args, **kwargs):
        log.debug('ResourceBase')
        if not kwargs.get('resource'):
            return self.set_instructions(value_set, *args, **kwargs)
        fields_set = []
        for field in value_set:
            try:
                setattr(self, field, value_set[field])
                fields_set.append(field)
            except:
                self.warning_could_not_set_resource_attribute(field)
        return {
            'failed': False if fields_set else True,
            'updated': fields_set,
            'state': self.state(),
        }

    def last_response(self, raw=False):
        log.debug('ResourceBase')
        return self.instruction_set_response if not raw else self.response

#   @pysnooper.snoop()
    def state(self, **kwargs):
        log.debug('ResourceBase')
        state = kwargs.get('state') or {}
        state.update(self.fetch_resource_values())
        return state

    # WARNINGS

    def warning_could_not_update_last_ewsc_resource_response(self, response):
        core_response = {
            'failed': True,
            'warning': 'Something went wrong. '
                       'Could not update last EWSC resource response values. '
                       'Details: {}, {}'.format(
                           response,
                           None if not response or isinstance(response, dict) \
                           and response.get('failed') else response.text
                       )
        }
        log.warning(core_response['warning'])
        return core_response

    def warning_could_not_set_instruction(self, instruction_tag):
        core_response = {
            'failed': True,
            'warning': 'Something went wrong. '
                       'Could not set resource handler instruction set tag {}.'\
                       .format(instruction_tag),
        }
        log.warning(core_response['warning'])
        return core_response

    def warning_unpopulated_instruction_set(self, *args):
        core_response = {
            'failed': True,
            'warning': 'Unpopulated resource instruction set. Details: {}'\
                       .format(args)
        }
        log.error(core_response['warning'])
        return core_response

    # ERRORS

    def error_no_http_response_found(self, *args):
        core_response = {
            'failed': True,
            'error': 'No HTTP response found. '
                     'Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_last_instruction_set_execution_timestamp(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update last instruction set execution timestamp. '
                     'Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response

    def error_instruction_set_parameter_not_properly_set(self, *args):
        core_response = {
            'failed': True,
            'error': 'Instruction set parameter not properly set. '
                     'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_convert_dictionary_to_json(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not convert python dictionary to JSON. '
                     'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_convert_json_to_dictionary(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not convert JSON to python dictionary. '
                     'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_last_ewsc_response_status(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update last EWSC instruction set response status. '
                     'Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_last_executed_instruction_set(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update last executed instruction set. '
                     'Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_last_resource_write_date(self):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update resource write date. '
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_last_ewsc_response_raw(self, response):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update last EWSC raw resource response. '
                     'Details: {}'.format(response)
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_last_ewsc_instruction_set_response(self, response):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update last EWSC instruction set resource response. '
                     'Details: {}'.format(response),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_issue_ewsc_api_call(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not issue API call to EWSC remote machine. '
                     'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response

    def error_unsupported_http_request_method(self, *args):
        core_response = {
            'failed': True,
            'error': 'Unsupported HTTP request method. Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response

    def error_invalid_basic_http_authorization_credentials(self, *args):
        core_response = {
            'failed': True,
            'error': 'Invalid HTTP Basic Auth credentials. Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_format_master_account_credentials_for_authorization(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. Could not format master account '
                     'credentials for authorization. Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response


