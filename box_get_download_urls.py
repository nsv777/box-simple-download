import sys

from my_box import Box

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise ValueError(
            "Usage: python box_get_download_urls.py <shared_link> <developer token>\n"
            "Example: python box_get_download_urls.py "
            "https://somename.box.com/s/7ei54ueq1234567o7uisp6kyq7654321 XBvK7s1fI77gbsLdcDHeyJBx1azAFo9N"
        )
    my_box = Box(developer_token=sys.argv[2])
    link = sys.argv[1]
    print(my_box.get_download_urls(item_link=link))
