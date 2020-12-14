'''
    Hello there, CyberSpace Walker!

    If you're reading this, I can only asume you're wondering around checking
    the code of libraries you're using, in which case... Thats ma boi! Always
    read before executing. You my friend, just got the props of the EWCC core
    developer, so congrats on that.

    Now let's get back to business.

    EWCC-lib (also known as the EWallet Python Client Core) has as its main
    goal to make the developers' job easier (I can only asume that means you).
    What job is that you may ask? Well using the most amazing virtual payment
    system ever, obviously. That would be the EWalletCreditClock VPS-Suit.

    Think of this library as a wrapper around the EWSC REST API. All actions
    and events have their own handlers that do a number of things for you, from
    creating the instruction set to recording history. And then there's also
    that tiny bit of talking to the remote server thing, so yeah, everything is
    taken care of, I spoil you people.

    These handlers are managed by the EWalletClientCore entity that has the
    responsabilities of creating, destroying, and configuring the handlers,
    as well as recording history.

    If you have any other questions regarding the functionality of this thing
    and you're still too lazy to read the official documentation that some
    eastern european guy out there worked really hard on, feel free to execute:

        ~$ python3 -m unittest discover

    in the same directory as this file, and then realize you're not getting off
    that easy and you need to poke around the functional tests.
    You can find them in the ./tests/functional directory.

    P.S.[0] - To successfully run the functional test suit, you first need to
    configure the library and point it to either the EWCreditClock staging or
    production servers (which are awesome, if I may add).

    P.S.[1] - Find a way to make my -= STAGING =- server do weird things it's
    not supposed to be doing, and you get a beaverage of your choice from me
    personally. I would be very much interested in how you managed. Messing
    with the production server will instantly get you the bad boy card, bad
    things happen to whoever holds the bad boy card.


    Regards, S:Mx093pk01.
'''

import datetime
import time
import json
import requests
import logging
import pysnooper
import socket
import os

from .base.config import Config

config_prime = Config(
    client_config={'lib-dir': os.path.dirname(os.path.abspath(__file__))}
)
config_file = config_prime.client_config['lib-dir'] + '/conf/ewcc.conf'
file_path = os.path.dirname(os.path.abspath(__file__)) + '/conf/ewcc.conf' \
    if not config_file else config_file
config_prime.config_init(config_file=file_path)
log = config_prime.log_init()

from .base import *


class EWalletClientCore():

#   @pysnooper.snoop()
    def __init__(self, *args, **kwargs):
        self.create_date = datetime.datetime.now()
        self.write_date = datetime.datetime.now()
        self.actions = dict()
        self.events = dict()
        self.status = bool()
        self.instruction_set = dict()
        self.instruction_set_response = dict()
        self.response = None
        self.timestamp = None
        self.config_file = kwargs.get('config_file') or file_path
        config_prime.config_reload(self.config_file)
        self.config = config_prime
        self.execution_category = str()
        self.previous_label = str()
        self.previous_action = str()
        self.previous_event = str()

    # FETCHERS

    def fetch_last_core_execution_type(self):
        log.debug('EWalletClientCore')
        return self.execution_category

    def fetch_last_executed_resource(self):
        log.debug('EWalletClientCore')
        return self.previous_label

    def fetch_last_executed_action(self):
        log.debug('EWalletClientCore')
        return self.previous_action

    def fetch_last_executed_event(self):
        log.debug('EWalletClientCore')
        return self.previous_event

    def fetch_action_resource_handler_map(self):
        log.debug('EWalletClientCore')
        return self.actions

    def fetch_event_resource_handler_map(self):
        log.debug('EWalletClientCore')
        return self.events

    def fetch_ewallet_client_core_purge_map(self):
        log.debug('EWalletClientCore')
        return {
            'write_date': datetime.datetime.now(),
            'config_file': str(),
            'actions': dict(),
            'events': dict(),
            'status': bool(),
            'instruction_set': dict(),
            'instruction_set_response': dict(),
            'response': None,
            'timestamp': None,
            'execution_category': str(),
            'previous_label': str(),
            'previous_action': str(),
            'previous_event': str(),
        }

    def fetch_complete_resource_map(self):
        log.debug('EWalletClientCore')
        resource_map = self.actions.copy()
        resource_map.update(self.events)
        return resource_map

#   @pysnooper.snoop()
    def fetch_ewallet_client_core_values(self):
        log.debug('EWalletClientCore')
        value_set = {
            'create_date': self.create_date,
            'write_date': self.write_date,
            'actions': self.actions,
            'events': self.events,
            'status': self.status,
            'instruction_set': self.instruction_set,
            'instruction_set_response': self.instruction_set_response,
            'response': self.response,
            'timestamp': self.timestamp,
            'config_file': self.config_file,
            'config': self.config.fetch_settings(),
            'execution_category': self.execution_category,
            'previous_label': self.previous_label,
            'previous_action': self.previous_action,
            'previous_event': self.previous_event,
        }
        return value_set

    def fetch_action_label_map(self):
        log.debug('EWalletClientCore')
        labeled_actions = {
            'RequestClientID': action_request_clientid.RequestClientID,
            'RequestSessionToken': action_request_stoken.RequestSessionToken,
            'CreateMaster': action_create_master_account.CreateMaster,
            'AcquireMaster': action_acquire_master.AcquireMaster,
            'STokenKeepAlive': action_stoken_keep_alive.STokenKeepAlive,
            'CTokenKeepAlive': action_ctoken_keep_alive.CTokenKeepAlive,
            'IssueReport': action_issue_report.IssueReport,
            'ReleaseMaster': action_release_master.ReleaseMaster,
            'MasterAccountLogin': action_master_account_login.MasterAccountLogin,
            'MasterAccountLogout': action_master_account_logout.MasterAccountLogout,
            'MasterViewAccount': action_master_view_account.MasterViewAccount,
            'MasterEditAccount': action_master_edit_account.MasterEditAccount,
            'MasterUnlinkAccount': action_master_unlink_account.MasterUnlinkAccount,
            'MasterRecoverAccount': action_master_recover_account.MasterRecoverAccount,
            'InspectCTokens': action_master_inspect_ctokens.MasterInspectCTokens,
            'InspectCToken': action_master_inspect_ctoken.MasterInspectCToken,
            'InspectSubPool': action_master_inspect_subordonate_pool.MasterInspectSubPool,
            'InspectSubordonate': action_master_inspect_subordonate.MasterInspectSubordonate,
            'MasterViewLogin': action_master_view_login.MasterViewLoginRecords,
            'MasterViewLogout': action_master_view_logout.MasterViewLogoutRecords,
            'CheckCTokenValid': action_check_ctoken_valid.CheckCTokenValid,
            'CheckCTokenLinked': action_check_ctoken_linked.CheckCTokenLinked,
            'CheckCTokenSession': action_check_ctoken_session.CheckCTokenSession,
            'CheckCTokenStatus': action_check_ctoken_status.CheckCTokenStatus,
            'CheckSTokenValid': action_check_stoken_valid.CheckSTokenValid,
            'CheckSTokenLinked': action_check_stoken_linked.CheckSTokenLinked,
            'CheckSTokenSession': action_check_stoken_session.CheckSTokenSession,
            'CheckSTokenStatus': action_check_stoken_status.CheckSTokenStatus,
            'PauseClockTimer': action_pause_clock_timer.PauseClockTimer,
            'ResumeClockTimer': action_resume_clock_timer.ResumeClockTimer,
            'StartClockTimer': action_start_clock_timer.StartClockTimer,
            'StopClockTimer': action_stop_clock_timer.StopClockTimer,
            'AccountLogin': action_account_login.AccountLogin,
            'AccountLogout': action_account_logout.AccountLogout,
            'RecoverAccount': action_recover_account.RecoverAccount,
            'AddContactRecord': action_add_contact_record.AddContactRecord,
            'ConvertClockToCredits': action_convert_clock2credits.ConvertClockToCredits,
            'ConvertCreditsToClock': action_convert_credits2clock.ConvertCreditsToClock,
            'CreateAccount': action_create_new_account.CreateNewAccount,
            'CreateContactList': action_create_contact_list.CreateContactList,
            'CreateConversionSheet': action_create_conversion_sheet.CreateConversionSheet,
            'CreateCreditClock': action_create_credit_clock.CreateCreditClock,
            'CreateCreditEWallet': action_create_credit_ewallet.CreateCreditEWallet,
            'CreateInvoiceSheet': action_create_invoice_sheet.CreateInvoiceSheet,
            'CreateTimeSheet': action_create_time_sheet.CreateTimeSheet,
            'CreateTransferSheet': action_create_transfer_sheet.CreateTransferSheet,
            'EditAccount': action_edit_account.EditAccount,
            'PayCredits': action_pay_credits.PayCredits,
            'SupplyCredits': action_supply_credits.SupplyCredits,
            'SwitchAccount': action_switch_active_session_user.SwitchSessionUser,
            'SwitchContactList': action_switch_contact_list.SwitchContactList,
            'SwitchConversionSheet': action_switch_conversion_sheet.SwitchConversionSheet,
            'SwitchCreditClock': action_switch_credit_clock.SwitchCreditClock,
            'SwitchCreditEWallet': action_switch_credit_ewallet.SwitchCreditEWallet,
            'SwitchInvoiceSheet': action_switch_invoice_sheet.SwitchInvoiceSheet,
            'SwitchTimeSheet': action_switch_time_sheet.SwitchTimeSheet,
            'SwitchTransferSheet': action_switch_transfer_sheet.SwitchTransferSheet,
            'TransferCredits': action_transfer_credits.TransferCredits,
            'UnlinkAccount': action_unlink_account.UnlinkAccount,
            'UnlinkContactList': action_unlink_contact_list.UnlinkContactList,
            'UnlinkContactRecord': action_unlink_contact_record.UnlinkContactRecord,
            'UnlinkConversionRecord': action_unlink_conversion_record.UnlinkConversionRecord,
            'UnlinkConversionSheet': action_unlink_conversion_sheet.UnlinkConversionSheet,
            'UnlinkCreditClock': action_unlink_credit_clock.UnlinkCreditClock,
            'UnlinkCreditEWallet': action_unlink_credit_ewallet.UnlinkCreditEWallet,
            'UnlinkInvoiceRecord': action_unlink_invoice_record.UnlinkInvoiceRecord,
            'UnlinkInvoiceSheet': action_unlink_invoice_sheet.UnlinkInvoiceSheet,
            'UnlinkTimeRecord': action_unlink_time_record.UnlinkTimeRecord,
            'UnlinkTimeSheet': action_unlink_time_sheet.UnlinkTimeSheet,
            'UnlinkTransferRecord': action_unlink_transfer_record.UnlinkTransferRecord,
            'UnlinkTransferSheet': action_unlink_transfer_sheet.UnlinkTransferSheet,
            'ViewAccount': action_view_account.ViewAccount,
            'ViewContactList': action_view_contact_list.ViewContactList,
            'ViewContactRecord': action_view_contact_record.ViewContactRecord,
            'ViewConversionRecord': action_view_conversion_record.ViewConversionRecord,
            'ViewConversionSheet': action_view_conversion_sheet.ViewConversionSheet,
            'ViewCreditClock': action_view_credit_clock.ViewCreditClock,
            'ViewCreditEWallet': action_view_credit_ewallet.ViewCreditEWallet,
            'ViewInvoiceRecord': action_view_invoice_record.ViewInvoiceRecord,
            'ViewInvoiceSheet': action_view_invoice_sheet.ViewInvoiceSheet,
            'ViewLoginRecords': action_view_login_records.ViewLoginRecords,
            'ViewLogoutRecords': action_view_logout_records.ViewLogoutRecords,
            'ViewTimeRecord': action_view_time_record.ViewTimeRecord,
            'ViewTimeSheet': action_view_time_sheet.ViewTimeSheet,
            'ViewTransferRecord': action_view_transfer_record.ViewTransferRecord,
            'ViewTransferSheet': action_view_transfer_sheet.ViewTransferSheet,
        }
        return labeled_actions

    # TODO
    def fetch_event_label_map(self):
        log.debug('EWalletClientCore - TODO - Client events not yet supported.')
        event_labels = {}
        return event_labels

    # UPDATERS

    def update_core_state_from_resource(self, target_label, resource_map):
        log.debug('EWalletClientCore')
        resource_state = resource_map[target_label].state()
        resource_type = self.check_resource_type(target_label)
        if resource_type == 'action':
            resource_state.update({
                'execution_category': 'action',
                'previous_label': target_label,
                'previous_action': target_label,
            })
        elif resource_type == 'event':
            resource_state.update({
                'execution_category': 'event',
                'previous_label': target_label,
                'previous_event': target_label,
            })
        else:
            return self.error_invalid_resource_label(target_label)
        return self.set_client_core_values(resource_state)

    def update_write_date(self, **kwargs):
        log.debug('EWalletClientCore')
        try:
            self.write_date = kwargs.get('write_date') \
                or datetime.datetime.now()
        except:
            return self.error_could_not_update_write_date(kwargs)
        return True

    def update_event_handlers(self, extension):
        log.debug('EWalletClientCore')
        try:
            self.events.update(extension)
        except:
            return self.error_could_not_update_event_handler_set(extension)
        return True

    def update_action_handlers(self, extension):
        log.debug('EWalletClientCore')
        try:
            self.actions.update(extension)
        except:
            return self.error_could_not_update_action_handler_set(extension)
        return True

    # CHECKERS

    def check_resource_type(self, target_label):
        log.debug('EWalletClientCore')
        actions = self.fetch_action_label_map()
        events = self.fetch_event_label_map()
        if target_label in actions.keys():
            return 'action'
        elif target_label in events.keys():
            return 'event'
        self.error_invalid_resource_label(target_label)
        return False

    # COMPUTERS

    def compute_setup_event_handler(self, handler_map):
        log.debug('EWalletClientCore')
        self.update_event_handlers(handler_map)
        return True

    def compute_setup_action_handler(self, handler_map):
        log.debug('EWalletClientCore')
        self.update_action_handlers(handler_map)
        return True

    # GENERAL

    def log_warning(self, warning):
        log.warning(
            '{} - [ DETAILS ] - {}'.format(
                warning.get('warning'), warning.get('details')
            )
        )

    def log_error(self, error):
        log.error(
            '{} - [ DETAILS ] - {}'.format(
                error.get('error'), error.get('details')
            )
        )

    # FORMATTERS

    def format_warning_response(self, **kwargs):
        log.debug('EWalletClientCore')
        core_response = {
            'failed': kwargs.get('failed'),
            'warning': kwargs.get('warning'),
            'details': ''.join(map(str, [
                item for item in filter(
                    lambda ch: ch not in "\\(\')\"", str(kwargs.get('details'))
                )
            ]))
        }
        return core_response

    def format_error_response(self, **kwargs):
        log.debug('EWalletClientCore')
        core_response = {
            'failed': kwargs.get('failed'),
            'error': kwargs.get('error'),
            'details': ''.join(map(str, [
                item for item in filter(
                    lambda ch: ch not in "\\(\')\"", str(kwargs.get('details'))
                )
            ]))
        }
        return core_response

    # CORE

    # TODO
    def new_issue_report(self, *args, **kwargs):
        log.debug('TODO - Not yet implemented.')

    def config_reload(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        return self.config.config_reload(*args, **kwargs)

#   @pysnooper.snoop()
    def server_online(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            response = sock.connect_ex((
                self.config.cloud_config['ewsc-address']\
                    .strip('https://').strip('http://'),
                self.config.cloud_config['ewsc-port'],
            ))
            return {
                'failed': False,
                'server': 'online' if response == 0 else 'offline'
            }
        except:
            return self.error_server_online_check_failure(args, kwargs)
        finally:
            sock.close()

    def previous_action_execution(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        return {
            'failed': False,
            'action': self.fetch_last_executed_action(),
        }

    def previous_event_execution(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        return {
            'failed': False,
            'event': self.fetch_last_executed_event(),
        }

    def previous_execution(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        return {
            'failed': False,
            'execution': self.fetch_last_core_execution_type(),
            'previous': self.fetch_last_executed_resource(),
        }

#   @pysnooper.snoop()
    def previous(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        if not args:
            return self.previous_execution(**kwargs)
        if 'action' in args:
            return self.previous_action_execution(*args, **kwargs)
        elif 'event' in args:
            return self.previous_event_execution(*args, **kwargs)
        resource_map = self.fetch_complete_resource_map()
        if args[0] not in resource_map:
            return self.error_invalid_resource_label(args[0])
        try:
            return resource_map[args[0]].previous()
        except:
            return self.error_could_not_fetch_previous_execution(args, kwargs)

#   @pysnooper.snoop()
    def action_resource_purge(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        resource_map = self.fetch_action_resource_handler_map()
        try:
            purge_map = {
                item: resource_map[item].purge(*args, **kwargs)
                for item in resource_map
            }
        except:
            return self.error_could_not_purge_all_action_resource_handlers(args, kwargs)
        purge_map.update({'failed': False})
        return purge_map

    def event_resource_purge(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        resource_map = self.fetch_event_resource_handler_map()
        try:
            purge_map = {
                item: resource_map[item].purge(*args, **kwargs)
                for item in resource_map
            }
        except:
            return self.error_could_not_purge_all_action_resource_handlers(args, kwargs)
        purge_map.update({'failed': False})
        return purge_map

#   @pysnooper.snoop('logs/ewcc.log')
    def total_resource_purge(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        resource_map = self.fetch_complete_resource_map()
        try:
            purge_map = {
                item: resource_map[item].purge(*args, **kwargs)
                for item in resource_map
            }
        except:
            return self.error_could_not_purge_all_resources(resource_map)
        if not purge_map:
            return self.warning_no_resource_handlers_found_to_purge(args, kwargs)
        purge_map.update({'failed': False})
        return purge_map

#   @pysnooper.snoop('logs/ewcc.log')
    def resource_purge(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        if kwargs.get('actions'):
            return self.action_resource_purge(*args, **kwargs)
        elif kwargs.get('events'):
            return self.event_resource_purge(*args, **kwargs)
        return self.total_resource_purge(*args, **kwargs)

    def config_purge(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        return self.config.purge(*args, **kwargs)

    def core_purge(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        purge_map = self.fetch_ewallet_client_core_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        value_set = {item: purge_map[item] for item in purge_fields}
        return self.set_values('Core', **value_set)

    def total_purge(self):
        log.debug('EWalletClientCore')
        try:
            purge = {
                'core': self.core_purge(),
                'resource': self.resource_purge(),
            }
        except:
            return self.error_could_not_purge_core_and_resources()
        purge.update({'failed': False})
        return purge

    def purge(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        if not args and not kwargs:
            return self.total_purge()
        elif args and args[0] in ['Core', '']:
            return self.core_purge(*args, **kwargs)
        elif args and args[0] == 'Config':
            return self.config_purge(*args, **kwargs)
        elif args and args[0] == 'Resource':
            return self.resource_purge(*args, **kwargs)
        resource_map = self.fetch_complete_resource_map()
        if args and args[0] not in resource_map:
            return self.error_invalid_target_label(args[0])
        return resource_map[target_label].purge(*args, **kwargs)

#   @pysnooper.snoop()
    def set_values(self, target_label, **value_set):
        log.debug('EWalletClientCore')
        if not target_label or isinstance(target_label, str) and \
                target_label == 'Core':
            return self.set_client_core_values(value_set)
        if target_label == 'Config':
            return self.set_client_core_config_values(value_set)
        resource_map = self.fetch_complete_resource_map()
        if target_label not in resource_map:
            return self.error_invalid_target_label(target_label)
        return resource_map[target_label].set_values(value_set)

    def state(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        if not args or args[0] in ['Core', '']:
            return {
                'failed': False,
                'state': self.fetch_ewallet_client_core_values(),
            }
        resource_map = self.fetch_complete_resource_map()
        if args[0] not in resource_map:
            return self.error_invalid_resource_label(args[0])
        return resource_map[args[0]].state()

    def response_core(self):
        log.debug('EWalletClientCore')
        response = {
            'failed': False,
            'execute': self.execution_category,
            'response': self.response,
            'instruction_set_response': self.instruction_set_response,
        }
        if self.execution_category == 'action':
            response.update({'action': self.previous_action})
        elif self.execution_category == 'event':
            response.update({'event': self.previous_event})
        return response

#   @pysnooper.snoop()
    def last_response(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        if not args and not kwargs:
            return self.response_core()
        if not args:
            if kwargs.get('raw'):
                return self.response
            return self.instruction_set_response
        resource_map = self.fetch_complete_resource_map()
        if args[0] not in list(resource_map.keys()):
            return self.error_invalid_resource_label(args[0])
        return resource_map[args[0]].last_response(**kwargs)

#   @pysnooper.snoop()
    def execute(self, target_label, *args, **kwargs):
        log.debug('EWalletClientCore')
        resource_map = self.fetch_complete_resource_map()
        if target_label not in resource_map:
            return self.error_invalid_target_label(target_label)
        execute = resource_map[target_label].execute(*args, **kwargs)
        self.update_core_state_from_resource(target_label, resource_map)
        return execute

    def set_client_core_config_values(self, value_set):
        log.debug('EWalletClientCore')
        return self.config.set_values(value_set)

    def set_client_core_values(self, value_set):
        log.debug('EWalletClientCore')
        fields_set = []
        for field in value_set:
            try:
                setattr(self, field, value_set[field])
                fields_set.append(field)
            except:
                self.warning_could_not_set_client_core_attribute(field)
        return self.warning_no_client_core_fields_set(value_set) \
            if not fields_set else {
                'failed': False,
                'updated': fields_set,
                'state': self.fetch_ewallet_client_core_values(),
            }

    def new_handlers(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        return self.setup_handlers(*args, **kwargs)

    def new(self, new='handlers', *args, **kwargs):
        log.debug('EWalletClientCore')
        handlers = {
            'handlers': self.new_handlers,
            'issue-report': self.new_issue_report,
        }
        if new not in handlers:
            return self.error_invalid_target_for_action_new(new)
        return handlers[new](*args, **kwargs)

    def setup_event_handlers(self, events='all', **kwargs):
        log.debug('EWalletClientCore')
        event_map = self.fetch_event_label_map()
        setup_count = 0
        handler_set = events if isinstance(events, list) \
            else (list(event_map.keys()) if events == 'all' else [])
        for item in handler_set:
            if not item:
                continue
            compute = self.compute_setup_event_handler({
                item: event_map[item](config=self.config)
            })
            if not compute:
                self.warning_could_not_setup_event_handler(item)
                continue
            setup_count += 1
            log.info('Successfully set up event handler for {}.'.format(item))
        event_handlers = self.events.copy()
        if setup_count != len(handler_set):
            self.warning_not_all_specified_event_handlers_setup(event_handlers)
        elif not event_handlers:
            return self.warning_no_event_handlers_set_up(events, kwargs)
        event_handlers.update({'failed': False})
        return event_handlers

#   @pysnooper.snoop()
    def setup_action_handlers(self, actions='all', *args, **kwargs):
        log.debug('EWalletClientCore')
        action_map = self.fetch_action_label_map()
        setup_count = 0
        handler_set = actions if isinstance(actions, list) \
            else (list(action_map.keys()) if actions == 'all' else [])
        for item in handler_set:
            if not item:
                continue
            compute = self.compute_setup_action_handler({
                item: action_map[item](config=self.config)
            })
            if not compute:
                self.warning_could_not_setup_action_handler(item)
                continue
            setup_count += 1
            log.info('Successfully set up action handler for {}.'.format(item))
        action_handlers = self.actions.copy()
        if setup_count != len(handler_set):
            self.warning_not_all_specified_action_handlers_setup(action_handlers)
        elif not action_handlers:
            return self.warning_no_action_handlers_set_up(actions, args, kwargs)
        action_handlers.update({'failed': False})
        return action_handlers

    def setup_all_handlers(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        return {
            'failed': False,
            'actions': self.setup_action_handlers(actions='all'),
            'events': self.setup_event_handlers(events='all'),
        }

#   @pysnooper.snoop()
    def setup_handlers(self, *args, **kwargs):
        log.debug('EWalletClientCore')
        handlers, response = {
            'action': self.setup_action_handlers,
            'event': self.setup_event_handlers,
        }, {}
        if not kwargs.get('handlers'):
            return self.setup_all_handlers(*args, **kwargs)
        elif not isinstance(kwargs.get('handlers'), list):
            return self.error_invalid_handler_value_set(args, kwargs)
        for item in kwargs['handlers']:
            if item not in handlers:
                self.warning_invalid_handler(item)
                continue
            handle = handlers[item](*args, **kwargs)
            response.update({item + 's': handle})
        core_response = {'failed': False}
        core_response.update(response)
        return core_response

    # WARNINGS
    '''
    [ TODO ]: Fetch all warning messages from message file by key codes
    '''

    def warning_no_action_handlers_set_up(self, *args):
        core_response = self.format_warning_response(
            failed=True,
            warning='Something went wrong. '
                    'No Action handlers set up.',
            details=args,
        )
        self.log_warning(core_response)
        return core_response

    def warning_no_event_handlers_set_up(self, *args):
        core_response = self.format_warning_response(
            failed=True,
            warning='Something went wrong. '
                    'No event handlers set up.',
            details=args,
        )
        self.log_warning(core_response)
        return core_response

    def warning_no_resource_handlers_found_to_purge(self, *args):
        core_response = self.format_warning_response(
            failed=True,
            warning='No resource handlers found to purge.',
            details=args,
        )
        self.log_warning(core_response)
        return core_response

    def warning_could_not_set_client_core_attribute(self, *args):
        core_response = self.format_warning_response(
            failed=True,
            warning='Something went wrong. '
                    'Could not set client core attribute.',
            details=args,
        )
        self.log_warning(core_response)
        return core_response

    def warning_no_client_core_fields_set(self, *args):
        core_response = self.format_warning_response(
            failed=True,
            warning='No client core fields updated from value set. ',
            details=args,
        )
        self.log_warning(core_response)
        return core_response

    def warning_could_not_setup_event_handler(self, *args):
        core_response = self.format_warning_response(
            failed=True,
            warning='Could not setup event handler for client event.',
            details=args,
        )
        self.log_warning(core_response)
        return core_response

    def warning_not_all_specified_event_handlers_setup(self, *args):
        core_response = self.format_warning_response(
            failed=True,
            warning='Something went wrong. '
                    'Could not setup all specified event handlers.',
            details=args,
        )
        self.log_warning(core_response)
        return core_response

    def warning_invalid_handler(self, *args):
        core_response = self.format_warning_response(
            failed=True,
            warning='Invalid handler.',
            details=args,
        )
        self.log_warning(core_response)
        return core_response

    def warning_could_not_setup_action_handler(self, *args):
        core_response = self.format_warning_response(
            failed=True,
            warning='Could not setup action handler for client action.',
            details=args,
        )
        self.log_warning(core_response)
        return core_response

    def warning_not_all_specified_action_handlers_setup(self, *args):
        core_response = self.format_warning_response(
            failed=True,
            warning='Something went wrong. '
                    'Could not setup all specified action handlers.',
            details=args,
        )
        self.log_warning(core_response)
        return core_response

    # ERRORS
    '''
    [ TODO ]: Fetch all error messages from message file by key codes
    '''

    def error_server_online_check_failure(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Something went wrong. '
                  'Could not check if EWSC services are available.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_could_not_fetch_previous_execution(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Something went wrong. '
                  'Could not fetch previous execution.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_could_not_purge_all_action_resource_handlers(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Something went wrong. '
                  'Could not purge all action resource handlers.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_could_not_selectively_purge_all_resource_handlers(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Something went wrong. '
                  'Could not selectively purge all resource handlers.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_could_not_purge_all_resources(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Something went wrong. '
                  'Could not purge all core resources.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_could_not_purge_core_and_resources(self):
        core_response = self.format_error_response(
            failed=True,
            error='Something went wrong. '
                  'Could not purge core and resources.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_invalid_resource_label(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Invalid resource label.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_invalid_target_label(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Invalid target label.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_could_not_update_event_handler_set(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Something went wrong. '
                  'Could not update EWCC event handler set.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_could_not_update_action_handler_set(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Something went wrong. '
                  'Could not update EWCC action handler set.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_could_not_update_write_date(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Something went wrong. '
                  'Could not update EWCC write date.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_invalid_target_for_action_new(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Invalid target for action new.',
            details=args,
        )
        self.log_error(core_response)
        return core_response

    def error_invalid_handler_value_set(self, *args):
        core_response = self.format_error_response(
            failed=True,
            error='Invalid handler value set.',
            details=args,
        )
        self.log_error(core_response)
        return core_response
