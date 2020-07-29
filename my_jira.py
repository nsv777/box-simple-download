import re

import yaml
from jira import JIRA


class Jira(object):
    def __init__(self):
        self._read_settings()
        self._authenticate()

    def _read_settings(self):
        with open("config.yml", "r") as yml_file:
            cfg = yaml.load(yml_file, Loader=yaml.SafeLoader)
        self.jira_username = cfg["jira"]["username"]
        self.jira_password = cfg["jira"]["password"]
        self.jira_url = cfg["jira"]["url"]

    def _authenticate(self):
        self.jira = JIRA(
            basic_auth=(self.jira_username, self.jira_password),
            options={"server": self.jira_url}
        )

    def get_ticket(self, ticket_key):
        tickets = self.jira.search_issues(
            jql_str="key = {}".format(ticket_key),
            fields="id, key, project, summary, description, status"
        )
        return tickets[0]

    def _get_ticket_description(self, ticket_key):
        return self.get_ticket(ticket_key=ticket_key).fields.description

    def get_box_link(self, ticket_key):
        description = self._get_ticket_description(ticket_key=ticket_key)
        for descr_line in description.splitlines():
            box_link = re.search('(https://.*.box.com/s/[a-z0-9]{32})', descr_line)
            if box_link:
                return box_link.group(1)
        return False

    def get_file_list(self, ticket_key):
        description = self._get_ticket_description(ticket_key=ticket_key)
        f_list = list()
        for descr_line in description.splitlines():
            font_name = re.search('^(.*\.(otf|ttf|txt|zip))$', descr_line, flags=re.IGNORECASE)
            if font_name:
                f_list.append(font_name.group(1))
        return f_list

    def get_target_folder(self, ticket_key):
        description = self._get_ticket_description(ticket_key=ticket_key)
        for descr_line in description.splitlines():
            t_folder = re.search("^The target is (.*)$", descr_line)
            if t_folder:
                return t_folder.group(1)
        return False
