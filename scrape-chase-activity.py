# /usr/bin/env python3
import csv
import io
import re

from bs4 import BeautifulSoup


def main():
    with open('activity.html', encoding='utf-8') as f:
        activity_soup = BeautifulSoup(f, 'html.parser')

    output_list = [["Type", "Transaction Date", "Post Date", "Description",
                    "Amount", "Negative Amount", "Additional Description", "Category"]]
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
        if (len(other_components) < 3):
            raise SyntaxError('Too few fields in record: {}'.format(csvish))

        date = other_components[0]

        description = ''.join(other_components[1:-2])

        amount_components = components[1].split(',')
        negative_amount = ''.join(
            amount_components[:len(amount_components) - 1])

        output_list.append(
            ["Sale", date, date, description, "", negative_amount, "", ""])

    with open('activity.csv', 'w', newline='') as output_file:
        activity_writer = csv.writer(output_file)
        for row in output_list:
            activity_writer.writerow(row)


if __name__ == "__main__":
    main()
