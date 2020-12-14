import requests
import json
import pysnooper
import sys
import logging
import time

from itertools import islice

from base.config import Config
from base.user_actions import UserActions
from lib.ewcc_lib import ewallet_client

config = Config()

def log_init():
    log_config = config.log_config
    log = logging.getLogger(log_config['log-name'])
    log.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_config['log-path'], 'a')
    formatter = logging.Formatter(
        log_config['log-record-format'],
        log_config['log-date-format']
    )
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    return log


log = log_init()


class EWalletCreditClockApiTutor():

    def __init__(self, *args, **kwargs):
        self.config = kwargs.get('config') or config
        self.client_core = ewallet_client.EWalletClientCore()
        self.client_core.setup_handlers(handlers=['action'])
        self.user_actions = UserActions(client_core=self.client_core)

    # FETCHERS

    def fetch_remote_instruction_set_url(self):
        log.debug('')
        return self.config.remote_machine_details['target-url']

    def fetch_remote_server_base_address(self):
        log.debug('')
        return self.config.remote_machine_details['server-address']

    def fetch_remote_server_port(self):
        log.debug('')
        return self.config.remote_machine_details['server-port']

    def fetch_remote_server_ewallet_path(self):
        log.debug('')
        return self.config.remote_machine_details['ewallet-path']

    def fetch_ewallet_credit_clock_banner(self):
        log.debug('')
        target_url = self.fetch_remote_server_base_address() + ':' \
            + str(self.fetch_remote_server_port()) \
            + self.fetch_remote_server_ewallet_path()
        formatted_data = self.format_data_for_ewallet_credit_clock_banner_request()
        return self.issue_rest_api_call_to_remote_machine(
            'GET', target_url, formatted_data
        )

#   @pysnooper.snoop()
    def fetch_ewallet_credit_clock_available_actions(self):
        log.debug('')
        target_url = self.fetch_remote_instruction_set_url()
        formatted_data = self.format_data_for_ewallet_credit_clock_available_options_request()
        http_request = self.issue_rest_api_call_to_remote_machine(
            'GET', target_url, formatted_data
        )
        return json.loads(http_request.text).get('available_actions')

    def display_ewallet_tutor_banner(self):
        log.debug('')
        remote_banner = self.fetch_ewallet_credit_clock_banner()
        if not remote_banner or not remote_banner.text:
            return False
        print('\n   ' + json.loads(remote_banner.text).get('message') + '\n')
        return remote_banner

    # FORMATTERS

    def format_data_for_ewallet_credit_clock_available_options_request(self):
        log.debug('')
        return {
            'Headers': {
                'Content-Type': 'application/json',
            },
            'Body': {},
        }

    def format_data_for_ewallet_credit_clock_action_detail_request(self, instruction_set):
        log.debug('')
        return {
            'Headers': {
                'Content-Type': 'application/json',
            },
            'Body': instruction_set,
        }

    def format_data_for_ewallet_credit_clock_banner_request(self):
        log.debug('')
        return {
            'Headers': {
                'Content-Type': 'application/json',
            },
            'Body': {},
        }

    # API REQUEST HANDLING

#   @pysnooper.snoop()
    def issue_rest_api_call_to_remote_machine_get(self, url, formatted_data):
        log.debug('')
        formatted_data = formatted_data or \
            self.format_data_for_ewallet_credit_clock_banner_request()
        try:
            reqst = requests.get(
                url, headers=formatted_data['Headers'],
                data=json.dumps(formatted_data['Body']),
            )
        except:
            return self.error_could_not_issue_get_api_call_to_remote_machine(url, formatted_data)
        return reqst

    def issue_rest_api_call_to_remote_machine_post(self, url, formatted_data):
        log.debug('')
        return requests.post(
            url, headers=formatted_data['Headers'],
            data=json.dumps(formatted_data['Body'])
        )

    def issue_rest_api_call_to_remote_machine(self, method, url, formatted_data):
        log.debug('')
        handlers = {
            'GET': self.issue_rest_api_call_to_remote_machine_get,
            'POST': self.issue_rest_api_call_to_remote_machine_post,
        }
        return handlers[method](url, formatted_data)

    # GENERAL

    def exit_tutor(self):
        log.debug('')
#       self.display_ewallet_tutor_banner()
        print('Terminating API Tutor.\n')
        sys.exit()

    # HANDLERS

    def handle_live_ewallet_action_session(self):
        log.debug('')
        target_url = self.fetch_remote_instruction_set_url()
        user_actions = self.fetch_ewallet_credit_clock_available_actions()
        # [ NOTE ]: Creates {<action-id> : <action-label>} map dynamicaly.
        options = {
            str(item): user_actions[item-1] for item in range(1, len(user_actions)+1)
        }
        while True:
            for item in options:
                print(str(item) + ') ' + options[item])
            selected_option = input('\nEWalletAction> ')
            if selected_option not in options.keys():
                self.warning_invalid_ewallet_tutor_option(selected_option)
                continue
            user_action_map = self.user_actions.user_action_map
            if options[selected_option] not in user_action_map.keys():
                self.warning_user_action_not_supported(selected_option)
                continue
            user_action = user_action_map[options[selected_option]](
                self.format_data_for_ewallet_credit_clock_action_detail_request,
                self.issue_rest_api_call_to_remote_machine,
            )
            if not user_action:
                return False
            print('\nInstruction Set Response: ' + str(
                    json.dumps(user_action, indent=4)
                ) + '\n'
            )
            return True
        return False

    # TODO
    def handle_live_ewallet_event_session(self):
        log.debug('TODO')
        print('\n[ WARNING ]: User events not yet supported.\n')
        return False

    # TODO
    def handle_view_user_event(self):
        log.debug('TODO')
        print('\n[ WARNING ]: User events not yet supported.\n')
        return False

    def handle_view_user_action(self):
        log.debug('')
        target_url = self.fetch_remote_instruction_set_url()
        user_actions = self.fetch_ewallet_credit_clock_available_actions()
        options = {
            str(item): user_actions[item-1] for item in range(1, len(user_actions)+1)
        }
        while True:
            for item in options:
                print(str(item) + ') ' + options[item])
            selected_option = input('\nEWalletAction> ')
            if selected_option not in options.keys():
                self.warning_invalid_ewallet_tutor_option(selected_option)
                continue
            instruction_set = {
                'option': 'action',
                'action': options[selected_option],
            }
            formatted_data = self.format_data_for_ewallet_credit_clock_action_detail_request(
                instruction_set
            )
            http_request = self.issue_rest_api_call_to_remote_machine(
                'GET', target_url, formatted_data
            )
            if not http_request or not http_request.text:
                return self.error_could_not_fetch_values_from_remote_server(
                    http_request
                )
            print('\n' + str(
                    json.dumps(json.loads(http_request.text), indent=4)
                ) + '\n'
            )
            return True
        return False

    # MENUS

    def main_menu(self):
        log.debug('')
        options = {
            'menu': {
                '1': 'Inspect User Action',
                '2': 'Inspect User Event',
                '3': 'Live EWallet Action Session',
                '4': 'Live EWallet Event Session',
                '5': 'Exit Tutor',
            },
            'handler': {
                '1': self.handle_view_user_action,
                '2': self.handle_view_user_event,
                '3': self.handle_live_ewallet_action_session,
                '4': self.handle_live_ewallet_event_session,
                '5': self.exit_tutor,
            }
        }
        while True:
            for item in options['menu']:
                print(str(item) + ') ' + options['menu'][item])
            selected_option = input('\nEWalletTutor> ')
            if selected_option not in options['menu'].keys() and selected_option \
                    not in options['menu'].values():
                self.warning_invalid_ewallet_tutor_option(selected_option)
                continue
            elif len(selected_option) > 1:
                self.warning_option_label_found()
                continue
            return options['handler'][selected_option]()
        return False

    def init(self):
        log.debug('')
        self.display_ewallet_tutor_banner()
        while True:
            self.main_menu()
        return True

    # WARNINGS

    def warning_user_action_not_supported(self, selected_option):
        warning = 'User action not supported. '\
                  'You may have an outdated EWallet API Tutor version.'
        log.warning(warning)
        print('\n[ WARNING ]: {}\n'.format(warning))
        time.sleep(1)
        return False

    def warning_option_label_found(self):
        warning = 'Please input menu number not menu label.'
        log.warning(warning)
        print('\n[ WARNING ]: {}\n'.format(warning))
        return False

    def warning_invalid_ewallet_tutor_option(self, tutor_option):
        warning = 'Invalid EWallet Tutor option {}.'.format(tutor_option)
        log.warning(warning)
        print('\n[ WARNING ]: {}\n'.format(warning))
        return False

    # ERRORS

    def error_could_not_issue_get_api_call_to_remote_machine(self, url, formatted_data):
        error = 'Something went wrong. Could not issue GET api call to remote machine.'
        log.error(error + 'Details : {}, {}'.format(url, formatted_data))
        print('[ ERROR ]: {}'.format(error))
        return False

    def error_could_not_fetch_values_from_remote_server(self, http_request):
        error = 'Something went wrong. Could not fetch values from remote server.'
        log.error(error + 'Details : {}'.format(http_request))
        print('\n[ ERROR ]: {}\n'.format(error))
        return False


if __name__ == '__main__':
    tutor = EWalletCreditClockApiTutor(config=Config())
    tutor.init()

# CODE DUMP

