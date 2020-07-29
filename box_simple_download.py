import sys

from my_box import Box
from my_jira import Jira

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise ValueError(
            "Usage: python box_simple_download.py <jira ticket> <developer token>\n"
            "Example: python box_simple_download.py ABC-12345 XBvK7s1fI77gbsLdcDHeyJBx1azAFo9N"
        )
    my_box = Box(developer_token=sys.argv[2])
    my_jira = Jira()
    ticket = my_jira.get_ticket(ticket_key=sys.argv[1])

    link = my_jira.get_box_link(ticket_key=sys.argv[1])
    target_folder = my_jira.get_target_folder(ticket_key=sys.argv[1])
    file_list = my_jira.get_file_list(ticket_key=sys.argv[1])

    print("\nSummary: {}\n\nBox shared url: {}\nTarget folder: {}\nFile list: {}".format(
        ticket.fields.summary,
        link,
        target_folder,
        file_list
    ))

    my_box.download_by_url(item_link=link, f_list=file_list, t_folder=target_folder)
