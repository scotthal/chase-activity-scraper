# /usr/bin/env python3
import csv
import io
import re

from bs4 import BeautifulSoup


def main():
    with open('activity.html', encoding='utf-8') as f:
        activity_soup = BeautifulSoup(f, 'html.parser')

    criteria = {
        'id': re.compile('^ACTIVITY.+'),
        'class': 'mds-activity-table__row',
    }
    for row in activity_soup.find_all(attrs=criteria):
        csvish = row.get('data-values')
        components = csvish.split('$')
        if (len(components) != 2):
            raise SyntaxError(
                'More than one $ character in record: {}'.format(csvish))

        other_components = components[0].split(',')
        date = other_components[0]
        print('Date: {}'.format(date))

        description = ''.join(other_components[1:-2])
        print('Description: {}'.format(description))

        amount_components = components[1].split(',')
        print('Negative Amount: {}'.format(
            ''.join(amount_components[:len(amount_components) - 1])))

        print()


if __name__ == "__main__":
    main()
