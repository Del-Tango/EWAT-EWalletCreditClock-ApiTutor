import logging
import pysnooper
import base64

from .config import Config
from .action_base import ActionBase

config = Config()
config.config_init()
log_name = config.log_config['log-name']
log = logging.getLogger(log_name or __name__)


class IssueReport(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(IssueReport, self).__init__(*args, **kwargs)
        self.instruction_set = {
            'controller': 'client',
            'ctype': 'action',
            'action': 'report',
            'report': 'issue',
        }
        return res

    # FETCHERS

    def fetch_ewcc_log_file(self):
        log.debug('IssueReport')
        log_file_path = self.config.log_config.get('log-path')
        return log_file_path

    def fetch_default_issue_report_format(self):
        log.debug('IssueReport')
        issue = {
            'name': '<issue-label type-str>',
            'log': '<b64enc-ewcc-log type-str>',
            'email': '<contact-email type-str>',
            'details': '<miscellaneous-data type-str>',
        }
        return issue

    def fetch_resource_purge_map(self):
        log.debug('IssueReport')
        return {
            'instruction_set': {
                'controller': 'client',
                'ctype': 'action',
                'action': 'report',
                'report': 'issue',
            }
        }

    def fetch_resource_key_map(self):
        log.debug('IssueReport')
        return {
            'instruction_set': '<instruction-set type-dict>',
            'client_id': '<client-id type-str>',
            'session_token': '<session-token type-str>',
            'issue': '<issue-report type-dict>',
        }

    # CHECKERS

#   @pysnooper.snoop('logs/ewcc.log')
    def check_issue_report_format(self, value_set):
        log.debug('IssueReport')
        if not value_set.get('issue') or \
                not isinstance(value_set['issue'], dict):
            return self.error_invalid_issue_report_format(value_set)
        valid_tags = list(self.fetch_default_issue_report_format().keys())
        valid_found, invalid_found = [], []
        for report_tag in value_set['issue']:
            if report_tag not in valid_tags:
                invalid_found.append(report_tag)
                self.warning_invalid_issue_report_tag_found(
                    report_tag, value_set, valid_tags
                )
                continue
            valid_found.append(report_tag)
        if not valid_found:
            return self.error_no_valid_issue_report_tags_found(
                value_set, valid_tags, valid_found, invalid_found
            )
        issue_report = {
            report_tag: value_set['issue'][report_tag]
            for report_tag in valid_found
        }
        return {
            'failed': False,
            'report': issue_report,
            'valid_tags': valid_found,
            'invalid_tags': invalid_found,
        }

    def check_for_illegal_instruction_set_keys(self, instruction_keys, valid_key_set):
        log.debug('IssueReport')
        return super(IssueReport, self).check_for_illegal_instruction_set_keys(
            instruction_keys, valid_key_set
        )

    # GENERAL

    def read_file_content(self, file_path):
        log.debug('IssueReport')
        with open(file_path, 'r') as fl:
            file_content = fl.read()
        return file_content

    def encode_text_base64(self, message):
        log.debug('IssueReport')
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    def encode_base64_ewcc_log_content(self):
        log.debug('IssueReport')
        log_file = self.fetch_ewcc_log_file()
        file_content = self.read_file_content(log_file)
        encoded_content = self.encode_text_base64(file_content)
        return encoded_content

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(IssueReport, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, **kwargs):
        log.debug('')
        instruction_set = self.fetch_instruction_set()
        return super(IssueReport, self).execute(instruction_set)

#   @pysnooper.snoop('logs/ewcc.log')
    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        valid_keys = list(self.fetch_resource_key_map().keys())
        if 'instruction_set' not in value_set:
            check_issue_format = self.check_issue_report_format(value_set)
            if not check_issue_format or isinstance(check_issue_format, dict) and \
                    check_issue_format.get('failed'):
                return self.error_invalid_issue_report_format(
                    value_set, valid_keys, check_issue_format, args, kwargs
                )
            check_issue_format['report']['log'] = self.encode_base64_ewcc_log_content()
        return super(IssueReport, self).set_values(
            value_set, valid_keys=valid_keys, *args, **kwargs
        )

    # WARNINGS

    def warning_invalid_issue_report_tag_found(self, *args):
        core_response = {
            'failed': True,
            'level': 'action-handler',
            'warning': 'Invalid issue report tag found. '
                       'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response

    # ERRORS

    def error_invalid_issue_report_format(self, *args):
        core_response = {
            'failed': True,
            'level': 'action-handler',
            'error': 'Invalid issue report format. '
                     'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response

    def error_no_valid_issue_report_tags_found(self, *args):
        core_response = {
            'failed': True,
            'level': 'action-handler',
            'error': 'No valid issue report tags found. '
                     'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response
