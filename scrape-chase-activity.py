# /usr/bin/env python3
import argparse

import scrape.chase


class OldChaseOutputFormatter(scrape.chase.OutputRecordFormatter):
    def __init__(self) -> None:
        pass

    def format_header(self) -> list[str]:
        return [
            'Type',
            'Transaction Date',
            'Post Date',
            'Description',
            'Amount',
            'Negative Amount',
            'Additional Description',
            'Category']

    def format_output_record(
            self,
            output_record: scrape.chase.OutputRecord) -> list[str]:
        return [
            'Sale',
            output_record.date,
            output_record.date,
            output_record.description,
            '-{}'.format(output_record.amount),
            output_record.amount,
            '',
            '',
        ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Scrape activity data from a chase.com UI snapshot')
    parser.add_argument('input_html', help='input HTML file')
    parser.add_argument('output_csv', help='output CSV file')
    args = parser.parse_args()

    with open(args.input_html, encoding='utf-8') as input_html:
        with open(args.output_csv, 'w', newline='') as output_csv:
            chase_scraper = scrape.chase.Chase(
                input_html, output_csv, OldChaseOutputFormatter())
            chase_scraper.scrape()


if __name__ == "__main__":
    main()
