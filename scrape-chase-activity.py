# /usr/bin/env python3
import csv
import io
import re

from bs4 import BeautifulSoup


def get_html_table_rows(file):
    activity_soup = BeautifulSoup(file, 'html.parser')
    criteria = {
        'id': re.compile('^ACTIVITY.+'),
        'class': 'mds-activity-table__row',
    }
    return activity_soup.find_all(attrs=criteria)


def get_record_string(row):
    return row.get('data-values')


def parse_row(record_string):
    components = record_string.split('$')
    if (len(components) != 2):
        raise SyntaxError(
            'More than one $ character in record: {}'.format(record_string))

    other_components = components[0].split(',')
    if (len(other_components) < 3):
        raise SyntaxError('Too few fields in record: {}'.format(record_string))
    date = other_components[0]
    description = ''.join(other_components[1:-2])

    amount_components = components[1].split(',')
    if (len(amount_components) < 2):
        raise SyntaxError('Too few fields in record: {}'.format(record_string))
    negative_amount = ''.join(amount_components[:len(amount_components) - 1])

    return {
        'date': date,
        'description': description,
        'negative_amount': negative_amount,
    }


def output_row(record):
    return [
        'Sale',
        record['date'],
        record['date'],
        record['description'],
        '',
        record['negative_amount'],
        '',
        '',
    ]


def output_csv_records(file, output_record_list):
    csv_writer = csv.writer(file)
    for record in output_record_list:
        csv_writer.writerow(record)


def main():
    with open('activity.html', encoding='utf-8') as i:
        table_rows = get_html_table_rows(i)

    output_record_list = [['Type', 'Transaction Date', 'Post Date', 'Description',
                           'Amount', 'Negative Amount', 'Additional Description', 'Category']]
    for table_row in table_rows:
        record_string = get_record_string(table_row)
        output_record_list.append(output_row(parse_row(record_string)))

    with open('activity.csv', 'w', newline='') as o:
        output_csv_records(o, output_record_list)


if __name__ == "__main__":
    main()
