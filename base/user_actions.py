import datetime
import json
import logging
import pysnooper

from .config import Config

config = Config()
log = logging.getLogger(config.log_config['log-name'])


class UserActions():

    def __init__(self, *args, **kwargs):
        self.config = kwargs.get('config') or config
        self.client_core = kwargs.get('client_core')
        self.user_action_map = {
            'RequestClientID': self.user_action_request_client_id,
            'RequestSessionToken': self.user_action_request_session_token,
            'CreateMaster': self.client_action_create_master,
            'AcquireMaster': self.client_action_acquire_master,
            'STokenKeepAlive': self.client_action_stoken_keep_alive,
            'CTokenKeepAlive': self.client_action_ctoken_keep_alive,
            'IssueReport': self.client_action_issue_report,
            'ReleaseMaster': self.client_action_release_master,
            'MasterAccountLogin': self.master_action_account_login,
            'MasterAccountLogout': self.master_action_account_logout,
            'MasterViewAccount': self.master_action_view_account,
            'MasterEditAccount': self.master_action_edit_account,
            'MasterUnlinkAccount': self.master_action_unlink_account,
            'MasterRecoverAccount': self.master_action_recover_account,
            'InspectCTokens': self.master_action_inspect_ctokens,
            'InspectCToken': self.master_action_inspect_ctoken,
            'InspectSubPool': self.master_action_inspect_subordonate_pool,
            'InspectSubordonate': self.master_action_inspect_subordonate_account,
            'MasterViewLogin': self.master_action_view_login_records,
            'MasterViewLogout': self.master_action_view_logout_records,
            'CheckCTokenValid': self.client_action_check_ctoken_valid,
            'CheckCTokenLinked': self.client_action_check_ctoken_linked,
            'CheckCTokenSession': self.client_action_check_ctoken_session,
            'CheckCTokenStatus': self.client_action_check_ctoken_status,
            'CheckSTokenValid': self.client_action_check_stoken_valid,
            'CheckSTokenLinked': self.client_action_check_stoken_linked,
            'CheckSTokenSession': self.client_action_check_stoken_session,
            'CheckSTokenStatus': self.client_action_check_stoken_status,
            'PauseClockTimer': self.user_action_pause_clock_timer,
            'ResumeClockTimer': self.user_action_resume_clock_timer,
            'StartClockTimer': self.user_action_start_clock_timer,
            'StopClockTimer': self.user_action_stop_clock_timer,
            'AccountLogin': self.user_action_account_login,
            'AccountLogout': self.user_action_account_logout,
            'RecoverAccount': self.user_action_recover_account,
            'AddContactListRecord': self.user_action_add_contact_list_record,
            'ConvertClockToCredits': self.user_action_convert_clock2credits,
            'ConvertCreditsToClock': self.user_action_convert_credits2clock,
            'CreateAccount': self.user_action_create_new_account,
            'CreateContactList': self.user_action_create_contact_list,
            'CreateConversionSheet': self.user_action_create_conversion_sheet,
            'CreateCreditClock': self.user_action_create_credit_clock,
            'CreateCreditEWallet': self.user_action_create_credit_ewallet,
            'CreateInvoiceSheet': self.user_action_create_invoice_sheet,
            'CreateTimeSheet': self.user_action_create_time_sheet,
            'CreateTransferSheet': self.user_action_create_transfer_sheet,
            'EditAccount': self.user_action_edit_account,
            'PayCredits': self.user_action_pay_credits,
            'SupplyCredits': self.user_action_supply_credits,
            'SwitchSessionUser': self.user_action_switch_active_session_user,
            'SwitchContactList': self.user_action_switch_contact_list,
            'SwitchConversionSheet': self.user_action_switch_conversion_sheet,
            'SwitchCreditClock': self.user_action_switch_credit_clock,
            'SwitchCreditEWallet': self.user_action_switch_credit_ewallet,
            'SwitchInvoiceSheet': self.user_action_switch_invoice_sheet,
            'SwitchTimeSheet': self.user_action_switch_time_sheet,
            'SwitchTransferSheet': self.user_action_switch_transfer_sheet,
            'TransferCredits': self.user_action_transfer_credits,
            'UnlinkAccount': self.user_action_unlink_account,
            'UnlinkContactList': self.user_action_unlink_contact_list,
            'UnlinkContactRecord': self.user_action_unlink_contact_record,
            'UnlinkConversionRecord': self.user_action_unlink_conversion_record,
            'UnlinkConversionSheet': self.user_action_unlink_conversion_sheet,
            'UnlinkCreditClock': self.user_action_unlink_credit_clock,
            'UnlinkCreditEWallet': self.user_action_unlink_credit_ewallet,
            'UnlinkInvoiceRecord': self.user_action_unlink_invoice_record,
            'UnlinkInvoiceSheet': self.user_action_unlink_invoice_sheet,
            'UnlinkTimeRecord': self.user_action_unlink_time_record,
            'UnlinkTimeSheet': self.user_action_unlink_time_sheet,
            'UnlinkTransferRecord': self.user_action_unlink_transfer_record,
            'UnlinkTransferSheet': self.user_action_unlink_transfer_sheet,
            'ViewAccount': self.user_action_view_account,
            'ViewContactList': self.user_action_view_contact_list,
            'ViewContactRecord': self.user_action_view_contact_record,
            'ViewConversionRecord': self.user_action_view_conversion_record,
            'ViewConversionSheet': self.user_action_view_conversion_sheet,
            'ViewCreditClock': self.user_action_view_credit_clock,
            'ViewCreditEWallet': self.user_action_view_credit_ewallet,
            'ViewInvoiceRecord': self.user_action_view_invoice_record,
            'ViewInvoiceSheet': self.user_action_view_invoice_sheet,
            'ViewLoginRecords': self.user_action_view_login_records,
            'ViewLogoutRecords': self.user_action_view_logout_records,
            'ViewTimeRecord': self.user_action_view_time_record,
            'ViewTimeSheet': self.user_action_view_time_sheet,
            'ViewTransferRecord': self.user_action_view_transfer_record,
            'ViewTransferSheet': self.user_action_view_transfer_sheet,
        }

    # FETCHERS

    def fetch_issue_report_label(self, separator=True):
        log.debug('')
        msg = '[ INPUT ]: Specify Issue Report Label -'
        if separator:
           msg = '\n' + msg
        print(msg)
        print(
            '[ NOTES ]: Descriptive name of the issue.\n'
        )
        while True:
            log_content = self.fetch_input_from_user('Label> ')
            if not log_content:
                continue
            break
        return log_content

    def fetch_issue_report_log_content(self, separator=True):
        log.debug('')
        msg = '[ INPUT ]: Specify Issue Report Log File Content -'
        if separator:
           msg = '\n' + msg
        print(msg)
        print(
            '[ NOTES ]: Relevant log file contents from the moment '
            'of the incident.\n'
        )
        while True:
            log_content = self.fetch_input_from_user('Log> ')
            if not log_content:
                continue
            break
        return log_content

    def fetch_issue_report_contact_email(self, separator=True):
        log.debug('')
        msg = '[ INPUT ]: Specify Issue Report Contact Email Address -'
        if separator:
           msg = '\n' + msg
        print(msg)
        print(
            '[ NOTES ]: The person to contact about the reported problem.\n'
        )
        while True:
            details = self.fetch_input_from_user('Email> ')
            if not details:
                continue
            break
        return details

    def fetch_issue_report_details(self, separator=True):
        log.debug('')
        msg = '[ INPUT ]: Specify Issue Report Details -'
        if separator:
           msg = '\n' + msg
        print(msg)
        print(
            '[ NOTES ]: Should contain miscellaneous and '
            'relevant data about the incident.\n'
        )
        while True:
            details = self.fetch_input_from_user('Details> ')
            if not details:
                continue
            break
        return details

    def fetch_master_email_from_user(self, separator=True):
        log.debug('')
        msg = '[ INPUT ]: Specify Master Account Email Address -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            user_email = self.fetch_input_from_user('Email> ')
            if not user_email:
                continue
            break
        return user_email

    def fetch_subordonate_account_id_from_user(self, separator=True):
        log.debug('')
        msg = '[ INPUT ]: Specify Subordonate Account ID -'
        if separator:
            msg = '\n' + msg
        print(msg)
        while True:
            key = self.fetch_input_from_user('SubordonateID> ')
            if not key:
                continue
            break
        return key

    def fetch_master_key_code_from_user(self, separator=True):
        log.debug('')
        msg = '[ INPUT ]: Specify Master Account Key Code -'
        if separator:
            msg = '\n' + msg
        print(msg)
        while True:
            key = self.fetch_input_from_user('Address> ')
            if not key:
                continue
            break
        return key

    def fetch_address_from_user(self, separator=True):
        log.debug('')
        msg = '[ INPUT ]: Specify Address -'
        if separator:
            msg = '\n' + msg
        print(msg)
        while True:
            address = self.fetch_input_from_user('Address> ')
            if not address:
                continue
            break
        return address

    def fetch_company_name_from_user(self, separator=True):
        log.debug('')
        msg = '[ INPUT ]: Specify Company Name -'
        if separator:
            msg = '\n' + msg
        print(msg)
        while True:
            company = self.fetch_input_from_user('Company> ')
            if not company:
                continue
            break
        return company

    def fetch_transfer_record_id_from_user(self, separator=True):
        log.debug('')
        msg = '[ INPUT ]: Specify Transfer Record ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            record_id = self.fetch_input_from_user('RecordID> ')
            if not record_id:
                continue
            break
        return record_id

    def fetch_time_record_id_from_user(self, separator=True):
        log.debug('')
        msg = '[ INPUT ]: Specify Time Record ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            record_id = self.fetch_input_from_user('RecordID> ')
            if not record_id:
                continue
            break
        return record_id

    def fetch_invoice_record_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Invoice Record ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            record_id = self.fetch_input_from_user('RecordID> ')
            if not record_id:
                continue
            break
        return record_id

    def fetch_credit_clock_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Credit Clock ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            clock_id = self.fetch_input_from_user('ClockID> ')
            if not clock_id:
                continue
            break
        return clock_id

    def fetch_conversion_record_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Conversion Record ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            record_id = self.fetch_input_from_user('RecordID> ')
            if not record_id:
                continue
            break
        return record_id

    def fetch_contact_record_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Contact Record ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            record_id = self.fetch_input_from_user('RecordID> ')
            if not record_id:
                continue
            break
        return record_id

    def fetch_transfer_to_email_address_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Partner Email Address -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            transfer_to = self.fetch_input_from_user('TransferTo> ')
            if not transfer_to:
                continue
            break
        return transfer_to

    def fetch_transfer_sheet_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Transfer Sheet ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            transfer_sheet_id = self.fetch_input_from_user('SheetID> ')
            if not transfer_sheet_id:
                continue
            break
        return transfer_sheet_id

    def fetch_time_sheet_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Time Sheet ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            time_sheet_id = self.fetch_input_from_user('SheetID> ')
            if not time_sheet_id:
                continue
            break
        return time_sheet_id

    def fetch_invoice_sheet_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Invoice Sheet ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            invoice_sheet_id = self.fetch_input_from_user('SheetID> ')
            if not invoice_sheet_id:
                continue
            break
        return invoice_sheet_id

    def fetch_ewallet_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify EWallet ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            ewallet_id = self.fetch_input_from_user('EWalletID> ')
            if not ewallet_id:
                continue
            break
        return ewallet_id

    def fetch_clock_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Credit Clock ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            credit_clock_id = self.fetch_input_from_user('ClockID> ')
            if not credit_clock_id:
                continue
            break
        return credit_clock_id

    def fetch_conversion_sheet_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Conversion Sheet ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            conversion_sheet_id = self.fetch_input_from_user('SheetID> ')
            if not conversion_sheet_id:
                continue
            break
        return conversion_sheet_id

    def fetch_currency_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Currency -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            currency = self.fetch_input_from_user('Currency> ')
            if not currency:
                continue
            break
        return currency

    def fetch_cost_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Cost -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            cost = self.fetch_input_from_user('Cost> ')
            if not cost:
                continue
            break
        return cost

    def fetch_pay_email_address_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Email Address -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            pay = self.fetch_input_from_user('Pay> ')
            if not pay:
                continue
            break
        return pay

    def fetch_user_alias_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Alias -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            alias = self.fetch_input_from_user('Alias> ')
            if not alias:
                continue
            break
        return alias

    def fetch_credits_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Credits -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            credits = self.fetch_input_from_user('Credits> ')
            if not credits:
                continue
            break
        return credits

    def fetch_minutes_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Minutes -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            minutes = self.fetch_input_from_user('Minutes> ')
            if not minutes:
                continue
            break
        return minutes

    def fetch_contact_list_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Contact List ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            contact_list = self.fetch_input_from_user('ListID> ')
            if not contact_list:
                continue
            break
        return contact_list

    def fetch_user_email_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Email Address -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            user_email = self.fetch_input_from_user('Email> ')
            if not user_email:
                continue
            break
        return user_email

    def fetch_user_phone_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Phone Number -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            user_phone = self.fetch_input_from_user('Phone> ')
            if not user_phone:
                continue
            break
        return user_phone

    def fetch_user_reference_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Reference -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            reference = self.fetch_input_from_user('Reference> ')
            if not reference:
                continue
            break
        return reference

    def fetch_notes_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Add Notes -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            notes = self.fetch_input_from_user('Notes> ')
            if not notes:
                continue
            break
        return notes

    def fetch_user_name_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Account User Name -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            user_name = self.fetch_input_from_user('Name> ')
            if not user_name:
                continue
            break
        return user_name

    def fetch_user_pass_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Account Password -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            user_pass = self.fetch_input_from_user('Password> ')
            if not user_pass:
                continue
            break
        return user_pass

    def fetch_input_from_user(self, prompt):
        log.debug('')
        return input(prompt)

    def fetch_client_id_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Client ID -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            client_id = self.fetch_input_from_user('ClientID> ')
            if not client_id:
                continue
            break
        return client_id

    def fetch_session_token_from_user(self, separator=False):
        log.debug('')
        msg = '[ INPUT ]: Specify Session Token -'
        if separator:
           msg = '\n' + msg
        print(msg)
        while True:
            session_token = self.fetch_input_from_user('SessionToken> ')
            if not session_token:
                continue
            break
        return session_token

    # DISPLAY

    def display_loading_instruction_set(self, instruction_set):
        log.debug('')
        print(
            '\nLoading Instruction Set: ' + str(
                json.dumps(instruction_set, indent=4)
            ) + '\n'
        )
        return True

    def display_error(self, msg):
        log.error(msg)
        print('\n[ ERROR ]: {}\n'.format(msg))
        return False

    # GENERAL

    def commit_instruction_set(self, separator=False):
        log.debug('')
        prompt = 'Commit Instruction Set? Y/N> '
        if separator:
            prompt = '\n' + prompt
        commit = input(prompt)
        answer = False if commit == 'n' or commit == 'N' else True
        if answer is False:
            print('\n[ INFO ]: Aborting interaction.\n')
        return answer

    # ACTIONS

    def client_action_acquire_master(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['AcquireMaster']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'AcquireMaster', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Acquire Master. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_stoken_keep_alive(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['STokenKeepAlive']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'STokenKeepAlive', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action SToken Keep Alive. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_ctoken_keep_alive(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CTokenKeepAlive']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CTokenKeepAlive', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action CToken Keep Alive. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_issue_report(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['IssueReport']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
            "issue": {
                "name": "<issue-label type-str>",
                "log": "<b64enc-log-content type-str>",
                "email": "<contact-email type-str>",
                "details": "<miscellaneous-data type-list>"
            },
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'issue': {
                'name': self.fetch_issue_report_label(separator=True),
                'log': self.fetch_issue_report_log_content(separator=True),
                'email': self.fetch_issue_report_contact_email(separator=True),
                'details': self.fetch_issue_report_details(separator=True),
            }
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'IssueReport', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Issue Report. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_release_master(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ReleaseMaster']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
            "master": "<email-address type-str>",
            "key": "<master-key-code type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'master': self.fetch_master_email_from_user(separator=True),
            'key': self.fetch_master_key_code_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'MasterAccountLogin', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Release Master. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_account_login(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['MasterAccountLogin']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
            "user_email": "<email-address type-str>",
            "user_pass": "<password type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'user_email': self.fetch_user_email_from_user(separator=True),
            'user_pass': self.fetch_user_pass_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'MasterAccountLogin', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Account Login. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_account_logout(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['MasterAccountLogout']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'MasterAccountLogout', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Account Logout. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_view_account(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['MasterViewAccount']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'MasterViewAccount', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action View Account. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_edit_account(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['MasterEditAccount']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'MasterEditAccount', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Edit Account. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_unlink_account(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['MasterUnlinkAccount']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'MasterUnlinkAccount', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Unlink Account. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_recover_account(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['MasterRecoverAccount']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'MasterRecoverAccount', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Recover Account. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_inspect_ctokens(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['InspectCTokens']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'InspectCTokens', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Inspect CTokens. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_inspect_ctoken(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['InspectCToken']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
            "ctoken": "<client-id type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'ctoken': self.fetch_client_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'InspectCToken', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Inspect CToken. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_inspect_subordonate_pool(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['InspectSubPool']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'InspectSubPool', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Inspect Subordonate Pool. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_inspect_subordonate_account(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['InspectSubordonate']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
            "subordonate": "<account-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'subordonate': self.fetch_subordonate_account_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'InspectSubordonate', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action Inspect Subordonate. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_view_login_records(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['MasterViewLogin']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'MasterViewLogin', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action View Login Records. '
                'Details: {}'.format(e)
            )
        return http_request

    def master_action_view_logout_records(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['MasterViewLogout']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        instruction_set.update({
            'client_id': client_id,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'MasterViewLogout', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute master action View Logout Records. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_check_ctoken_valid(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CheckCTokenValid']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        instruction_set.update({
            'client_id': client_id,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CheckCTokenValid', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Check CToken Valid. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_check_ctoken_linked(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CheckCTokenLinked']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        instruction_set.update({
            'client_id': client_id,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CheckCTokenLinked', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Check CToken Linked. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_check_ctoken_session(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CheckCTokenSession']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        instruction_set.update({
            'client_id': client_id,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CheckCTokenSession', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Check CToken Session. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_check_ctoken_status(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CheckCTokenStatus']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        instruction_set.update({
            'client_id': client_id,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CheckCTokenStatus', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Check CToken Status. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_check_stoken_valid(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CheckSTokenValid']['state']['instruction_set']
        instruction_set.update({
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CheckSTokenValid', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Check SToken Valid. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_check_stoken_linked(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CheckSTokenLinked']['state']['instruction_set']
        instruction_set.update({
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CheckSTokenLinked', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Check SToken Linked. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_check_stoken_session(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CheckSTokenSession']['state']['instruction_set']
        instruction_set.update({
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CheckSTokenSession', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Check SToken Session. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_check_stoken_status(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CheckSTokenStatus']['state']['instruction_set']
        instruction_set.update({
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CheckStokenStatus', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Check SToken Status. '
                'Details: {}'.format(e)
            )
        return http_request

    def client_action_create_master(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CreateMaster']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "user_email": "<email-address type-str>",
            "user_name": "<name type-str>",
            "user_pass": "<password type-str>",
            "user_alias": "<alias type-str>",
            "user_phone": "<phone-number type-str>",
            "company": "<user-company type-str>",
            "address": "<user-address type-str>",
            "key": "<master-key-code type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            "user_email": self.fetch_user_email_from_user(separator=True),
            "user_name": self.fetch_user_name_from_user(separator=True),
            "user_pass": self.fetch_user_pass_from_user(separator=True),
            "user_alias": self.fetch_user_alias_from_user(separator=True),
            "user_phone": self.fetch_user_phone_from_user(separator=True),
            "company": self.fetch_company_name_from_user(separator=True),
            "address": self.fetch_address_from_user(separator=True),
            "key": self.fetch_master_key_code_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CreateMaster', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Create Master. '
                'Details: {}'.format(e)
            )
        return http_request

    def user_action_recover_account(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['RecoverAccount']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'RecoverAccount', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Recover Account. '
                'Details: {}'.format(e)
            )
        return http_request

#   @pysnooper.snoop()
    def user_action_request_client_id(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['RequestClientID']['state']['instruction_set']
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'RequestClientID', instruction_set
            )
        except Exception as e:
            return self.display_error(
                'Something went wrong. '
                'Could not execute use action Request Client ID. '
                'Details: {}'.format(e)
            )
        return http_request

    def user_action_request_session_token(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['RequestSessionToken']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        instruction_set['client_id'] = client_id
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'RequestSessionToken', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Request Session Token.'
            )
        return http_request

    def user_action_pause_clock_timer(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['PauseClockTimer']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'PauseClockTimer', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Pause Clock Timer.'
            )
        return http_request

    def user_action_resume_clock_timer(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ResumeClockTimer']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ResumeClockTimer', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Resume Clock Timer.'
            )
        return http_request

    def user_action_start_clock_timer(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['StartClockTimer']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'StartClockTimer', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Start Clock Timer.'
            )
        return http_request

    def user_action_stop_clock_timer(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['StopClockTimer']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'StopClockTimer', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Stop Clock Timer.'
            )
        return http_request

    def user_action_account_login(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['AccountLogin']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "user_name": "<account-user-name type-str>",
            "user_pass": "<account-user-pass type-str>"
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'user_name': self.fetch_user_name_from_user(separator=True),
            'user_pass': self.fetch_user_pass_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'AccountLogin', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Account Login.'
            )
        return http_request

    def user_action_account_logout(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['AccountLogout']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>"
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'AccountLogout', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Account Logout.'
            )
        return http_request

    def user_action_add_contact_list_record(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['AddContactRecord']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "contact_list": "<contact-list-id type-int>",
            "user_email": "<contact-email type-str>",
            "user_name": "<contact-name type-str>",
            "user_phone": "<contact-phone type-str>",
            "user_reference": "<contact-reference type-str>",
            "notes": "<contact-notes type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'contact_list': self.fetch_contact_list_id_from_user(separator=True),
            'user_email': self.fetch_user_email_from_user(separator=True),
            'user_name': self.fetch_user_name_from_user(separator=True),
            'user_phone': self.fetch_user_phone_from_user(separator=True),
            'user_reference': self.fetch_user_reference_from_user(separator=True),
            'notes': self.fetch_notes_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'AddContactRecord', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Add Contact List Record.'
            )
        return http_request

    def user_action_convert_clock2credits(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ConvertClockToCredits']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "minutes": "<minutes-to-convert type-float>",
            "notes": "<notes type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'minutes': self.fetch_minutes_from_user(separator=True),
            'ntoes': self.fetch_notes_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ConvertClockToCredits', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Convert Clock To Credits.'
            )
        return http_request

    def user_action_convert_credits2clock(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ConvertCreditsToClock']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "credits": "<ewallet-credits type-int>",
            "notes": "<conversion-notes type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'credits': self.fetch_credits_from_user(separator=True),
            'notes': self.fetch_notes_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ConvertCreditsToClock', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Convert Credits To Clock.'
            )
        return http_request

    def user_action_create_new_account(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CreateAccount']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "user_email": "<account-user-email type-str>",
            "user_name": "<account-user-name type-str>",
            "user_pass": "<account-user-pass type-str>"
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'user_email': self.fetch_user_email_from_user(separator=True),
            'user_name':  self.fetch_user_name_from_user(separator=True),
            'user_pass': self.fetch_user_pass_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CreateAccount', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Create New Account.'
            )
        return http_request

    def user_action_create_contact_list(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CreateContactList']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>"
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CreateContactList', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Create Contact List.'
            )
        return http_request

    def user_action_create_conversion_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CreateConversionSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>"
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CreateConversionSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Create Conversion Sheet.'
            )
        return http_request

    def user_action_create_credit_clock(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CreateCreditClock']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CreateCreditClock', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Create Credit Clock.'
            )
        return http_request

    def user_action_create_credit_ewallet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CreateCreditEWallet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CreateCreditEWallet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Create Credit EWallet.'
            )
        return http_request

    def user_action_create_invoice_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CreateInvoiceSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CreateInvoiceSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Create Invoice Sheet.'
            )
        return http_request

    def user_action_create_time_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CreateTimeSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CreateTimeSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Create Time Sheet.'
            )
        return http_request

    def user_action_create_transfer_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['CreateTransferSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'CreateTransferSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Create Transfer Sheet.'
            )
        return http_request

    def user_action_edit_account(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['EditAccount']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "user_alias": "<account-user-alias type-str>",
            "user_email": "<account-user-email type-str>",
            "user_name": "<account-user-name type-str>",
            "user_pass": "<account-user-pass type-str>",
            "user_phone": "<account-user-phone type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'user_alias': self.fetch_user_alias_from_user(separator=True),
            'user_email': self.fetch_user_email_from_user(separator=True),
            'user_name': self.fetch_user_name_from_user(separator=True),
            'user_pass': self.fetch_user_pass_from_user(separator=True),
            'user_phone': self.fethc_user_phone_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'EditAccount', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Edit Account.'
            )
        return http_request

    def user_action_pay_credits(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['PayCredits']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "pay": "<account-user-email type-str>",
            "credits": "<ewallet-credits type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'pay': self.fetch_pay_email_address_from_user(separator=True),
            'credits': self.fetch_credits_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'PayCredits', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Pay Credits.'
            )
        return http_request

    def user_action_supply_credits(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['SupplyCredits']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "credits": "<ewallet-credits type-int>",
            "currency": "<currency-label type-str>",
            "cost": "<currency-cost-per-credit type-float>",
            "notes": "<supply-notes type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'credits': self.fetch_credits_from_user(separator=True),
            'currency': self.fetch_currency_from_user(separator=True),
            'cost': self.fetch_cost_from_user(separator=True),
            'notes': self.fetch_notes_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'SupplyCredits', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Supply Credits.'
            )
        return http_request

    def user_action_switch_active_session_user(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['SwitchAccount']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "account": "<account-user-email type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'account': self.fetch_user_email_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'SwitchAccount', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Switch Active Session User.'
            )
        return http_request

    def user_action_switch_contact_list(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['SwitchContactList']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "list_id": "<contact-list-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'list_id': self.fetch_contact_list_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'SwitchContactList', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Switch Contact List.'
            )
        return http_request

    def user_action_switch_conversion_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['SwitchConversionSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "sheet_id": "<conversion-sheet-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'sheet_id': self.fetch_conversion_sheet_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'SwitchConversionSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Switch Conversion Sheet.'
            )
        return http_request

    def user_action_switch_credit_clock(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['SwitchCreditClock']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "clock_id": "<credit-clock-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'clock_id': self.fetch_clock_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'SwitchCreditClock', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Switch Credit Clock.'
            )
        return http_request

    def user_action_switch_credit_ewallet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['SwitchCreditEWallet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "ewallet_id": "<ewallet-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'ewallet_id': self.fetch_ewallet_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'SwitchCreditEWallet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Switch Credit EWallet.'
            )
        return http_request

    def user_action_switch_invoice_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['SwitchInvoiceSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "sheet_id": "<invoice-sheet-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'sheet_id': self.fetch_invoice_sheet_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'SwitchInvoiceSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Switch Invoice Sheet.'
            )
        return http_request

    def user_action_switch_time_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['SwitchTimeSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "sheet_id": "<time-sheet-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'sheet_id': self.fetch_time_sheet_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'SwitchTimeSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Switch Time Sheet.'
            )
        return http_request

    def user_action_switch_transfer_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['SwitchTransferSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "sheet_id": "<transfer-sheet-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'sheet_id': self.fetch_transfer_sheet_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'SwitchTransferSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Switch Transfer Sheet.'
            )
        return http_request

    def user_action_transfer_credits(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['TransferCredits']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "transfer_to": "<account-user-email type-str>",
            "credits": "<ewallet-credits type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'transfer_to': self.fetch_transfer_to_email_address_from_user(separator=True),
            'credits': self.fetch_credits_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'TransferCredits', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Transfer Credits.'
            )
        return http_request

    def user_action_unlink_account(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkAccount']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkAccount', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Account.'
            )
        return http_request

    def user_action_unlink_contact_list(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkContactList']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "list_id": "<contact-list-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'list_id': self.fetch_contact_list_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkContactList', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Contact List.'
            )
        return http_request

    def user_action_unlink_contact_record(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkContactRecord']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "record_id": "<contact-record-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'record_id': self.fetch_contact_record_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkContactRecord', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Contact Record.'
            )
        return http_request

    def user_action_unlink_conversion_record(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkConversionRecord']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "record_id": "<conversion-record-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'record_id': self.fetch_conversion_record_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkConversionRecord', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Conversion Record.'
            )
        return http_request

    def user_action_unlink_conversion_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkConversionSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "list_id": "<conversion-sheet-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'list_id': self.fetch_conversion_sheet_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkConversionSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Conversion Sheet.'
            )
        return http_request

    def user_action_unlink_credit_clock(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkCreditClock']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "clock_id": "<credit-clock-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'clock_id': self.fetch_credit_clock_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkCreditClock', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Credit Clock.'
            )
        return http_request

    def user_action_unlink_credit_ewallet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkCreditEWallet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "ewallet_id": "<ewallet-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'ewallet_id': self.fetch_ewallet_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkCreditEWallet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Credit EWallet.'
            )
        return http_request

    def user_action_unlink_invoice_record(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkInvoiceRecord']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "record_id": "<invoice-record-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'record_id': self.fetch_invoice_record_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkInvoiceRecord', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Invoice Record.'
            )
        return http_request

    def user_action_unlink_invoice_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkInvoiceSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "list_id": "<invoice-sheet-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'list_id': self.fetch_invoice_sheet_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkInvoiceSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Invoice Sheet.'
            )
        return http_request

    def user_action_unlink_time_record(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkTimeRecord']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "record_id": "<time-record-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'record_id': self.fetch_time_record_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkTimeRecord', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Time Record.'
            )
        return http_request

    def user_action_unlink_time_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkTimeSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "list_id": "<time-sheet-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'time_list': self.fetch_time_sheet_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkTimeSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Time Sheet.'
            )
        return http_request

    def user_action_unlink_transfer_record(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkTransferRecord']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "record_id": "<transfer-record-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'record_id': self.fetch_transfer_record_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkTransferRecord', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Transfer Record.'
            )
        return http_request

    def user_action_unlink_transfer_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['UnlinkTransferSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "list_id": "<transfer-sheet-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'list_id': self.fetch_transfer_sheet_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'UnlinkTransferSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action Unlink Transfer Sheet.'
            )
        return http_request

    def user_action_view_account(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewAccount']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewAccount', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Account.'
            )
        return http_request

    def user_action_view_contact_list(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewContactList']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewContactList', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Contact List.'
            )
        return http_request

    def user_action_view_contact_record(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewContactRecord']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "record_id": "<contact-record-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'record_id': self.fetch_contact_record_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewContactRecord', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Contact Record.'
            )
        return http_request

    def user_action_view_conversion_record(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewConversionRecord']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "record_id": "<conversion-record-id>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'record_id': self.fetch_conversion_record_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewConversionRecord', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Conversion Record.'
            )
        return http_request

    def user_action_view_conversion_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewConversionSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewConversionSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Conversion Sheet.'
            )
        return http_request

    def user_action_view_credit_clock(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewCreditClock']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewCreditClock', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Credit Clock.'
            )
        return http_request

    def user_action_view_credit_ewallet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewCreditEWallet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewCreditEWallet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Credit EWallet.'
            )
        return http_request

    def user_action_view_invoice_record(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewInvoiceRecord']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "record_id": "<invoice-record-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'record_id': self.fetch_invoice_record_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewInvoiceRecord', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Invoice Record.'
            )
        return http_request

    def user_action_view_invoice_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewInvoiceSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewInvoiceSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Invoice Sheet.'
            )
        return http_request

    def user_action_view_login_records(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewLoginRecords']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewLoginRecords', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Login Records.'
            )
        return http_request

    def user_action_view_logout_records(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewLogoutRecords']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewLogoutRecords', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Logout Records.'
            )
        return http_request

    def user_action_view_time_record(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewTimeRecord']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "record_id": "<time-record-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'record_id': self.fetch_time_record_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewTimeRecord', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Time Record.'
            )
        return http_request

    def user_action_view_time_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewTimeSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewTimeSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Time Sheet.'
            )
        return http_request

    def user_action_view_transfer_record(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewTransferRecord']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
            "record_id": "<transfer-record-id type-int>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
            'record_id': self.fetch_transfer_record_id_from_user(separator=True),
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewTransferRecord', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Transfer Record.'
            )
        return http_request

    def user_action_view_transfer_sheet(self, formatter_func, api_func):
        log.debug('')
        instruction_set = self.client_core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )['ViewTransferSheet']['state']['instruction_set']
        instruction_set.update({
            "client_id": "<client-id type-str>",
            "session_token": "<session-token type-str>",
        })
        self.display_loading_instruction_set(instruction_set)
        client_id = self.fetch_client_id_from_user()
        if not client_id:
            return False
        session_token = self.fetch_session_token_from_user(separator=True)
        if not session_token:
            return False
        instruction_set.update({
            'client_id': client_id,
            'session_token': session_token,
        })
        self.display_loading_instruction_set(instruction_set)
        if not self.commit_instruction_set():
            return False
        try:
            http_request = self.client_core.execute(
                'ViewTransferSheet', instruction_set
            )
        except:
            return self.display_error(
                'Something went wrong. '
                'Could not execute user action View Transfer Sheet.'
            )
        return http_request
