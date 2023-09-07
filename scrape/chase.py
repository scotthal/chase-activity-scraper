#!/usr/bin/env python3
import csv
import re

from bs4 import BeautifulSoup


class OutputRecordFormatter:
    def __init__(self):
        pass

    def format_header(self):
        return ["Date", "Description", "Amount"]

    def format_output_record(self, output_record):
        return [
            output_record['date'],
            output_record['description'],
            output_record['amount']
        ]


class Chase:
    def __init__(self, input_html, output_csv, output_formatter):
        self.input_html = input_html
        self.output_csv = output_csv
        self.output_csv_writer = csv.writer(self.output_csv)
        self.output_formatter = output_formatter

    def get_html_table_rows(self):
        activity_soup = BeautifulSoup(self.input_html, 'html.parser')
        criteria = {
            'id': re.compile('^ACTIVITY.+'),
            'class': 'mds-activity-table__row',
        }
        return activity_soup.find_all(attrs=criteria)

    def get_record_string(self, row):
        return row.get('data-values')

    def parse_input_record_string(self, input_record_string):
        components = input_record_string.split('$')
        if (len(components) != 2):
            raise SyntaxError(
                'More than one $ character in record: {}'.format(input_record_string))

        other_components = components[0].split(',')
        if (len(other_components) < 3):
            raise SyntaxError(
                'Too few fields in record: {}'.format(input_record_string))
        date = other_components[0]
        description = ''.join(other_components[1:-2])

        amount_components = components[1].split(',')
        if (len(amount_components) < 2):
            raise SyntaxError(
                'Too few fields in record: {}'.format(input_record_string))
        amount = ''.join(
            amount_components[:len(amount_components) - 1])

        return {
            'date': date,
            'description': description,
            'amount': amount,
        }

    def scrape(self):
        input_table_rows = self.get_html_table_rows()
        self.output_csv_writer.writerow(self.output_formatter.format_header())
        for input_table_row in input_table_rows:
            input_record_string = self.get_record_string(input_table_row)
            output_record = self.parse_input_record_string(input_record_string)
            self.output_csv_writer.writerow(
                self.output_formatter.format_output_record(output_record))
