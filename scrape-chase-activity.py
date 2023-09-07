# /usr/bin/env python3
import argparse
import scrape.chase


class ChaseOutputFormatter:
    def __init__(self):
        pass

    def format_header(self):
        return ['Type', 'Transaction Date', 'Post Date', 'Description',
                'Amount', 'Negative Amount', 'Additional Description', 'Category']

    def format_output_record(self, output_record):
        return [
            'Sale',
            output_record['date'],
            output_record['date'],
            output_record['description'],
            '',
            output_record['negative_amount'],
            '',
            '',
        ]


def main():
    parser = argparse.ArgumentParser(
        description='Scrape activity data from a chase.com UI snapshot')
    parser.add_argument('input_html', help='input HTML file')
    parser.add_argument('output_csv', help='output CSV file')
    args = parser.parse_args()

    with open(args.input_html, encoding='utf-8') as input_html:
        with open(args.output_csv, 'w', newline='') as output_csv:
            chase_scraper = scrape.chase.Chase(
                input_html, output_csv, ChaseOutputFormatter())
            chase_scraper.scrape()


if __name__ == "__main__":
    main()
