# /usr/bin/env python3
import csv
import io
import re

from bs4 import BeautifulSoup


def main():
    with open('activity.html', encoding='utf-8') as f:
        activity_soup = BeautifulSoup(f, 'html.parser')

    criteria = {
        'id': re.compile('^ACTIVITY+'),
        'class': 'mds-activity-table__row',
    }
    for row in activity_soup.find_all(attrs=criteria):
        csvish = row.get('data-values')


if __name__ == "__main__":
    main()
