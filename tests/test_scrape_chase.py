#!/usr/bin/env python3
import io
import unittest

from .context import Chase
from .context import OutputRecord
from .context import OutputRecordFormatter


class TestOutputFormatter(unittest.TestCase):
    def test_output_record_formatter_format_header(self) -> None:
        header = OutputRecordFormatter().format_header()
        self.assertIn('Date', header)
        self.assertIn('Description', header)
        self.assertIn('Amount', header)

    def test_ouput_record_formatter_format_output_record(self) -> None:
        record = OutputRecord('a', 'b', 'c')
        formatter = OutputRecordFormatter()
        self.assertEqual(
            formatter.format_output_record(record), [
                'a', 'b', 'c'])


class TestChase(unittest.TestCase):
    test_chase_html = """<html><head><title>Test Chase UI</title></head>
<body>
<div>
    <table id="PENDING-dataTableId-mds-diy-data-table" class="mds-activity-table">
        <tr id="PENDING-dataTableId-row-1" class="mds-activity-table__row mds-activity-table__row--relaxed mds-activity-table__row--activated mds-activity-table__row--solid" data-values="09/06/2023,SHOULD NOT SEE,$22.99">
            <td>Irrelevant</td>
        </tr>
    </table>
    <table id="ACTIVITY-dataTableId-mds-diy-data-table" class="mds-activity-table">
        <tr id="ACTIVITY-dataTableId-row-1" class="mds-activity-table__row mds-activity-table__row--relaxed mds-activity-table__row--activated" data-values="{}">
            <td>Also irrelevant</td>
        </tr>
    </table>
</div>
</body>
</html>
"""

    def test_parse_good_input(self) -> None:
        expected_output = 'Date,Description,Amount\r\n07/29/2023,CIRCLE K # 40645,32.89\r\n'
        html = self.test_chase_html.format(
            '07/29/2023,CIRCLE K # 40645,,$32.89,')
        formatter = OutputRecordFormatter()

        with io.StringIO(html) as html_input:
            with io.StringIO() as csv_output:
                Chase(html_input, csv_output, formatter).scrape()
                self.assertEqual(csv_output.getvalue(), expected_output)

    def test_parse_too_many_dollar_signs(self) -> None:
        html = self.test_chase_html.format(
            '07/29/2023,CIRCLE $K # 40645,,$32.89,')
        formatter = OutputRecordFormatter()

        with io.StringIO(html) as html_input:
            with io.StringIO() as csv_output:
                with self.assertRaises(SyntaxError):
                    Chase(html_input, csv_output, formatter).scrape()

    def test_parse_too_few_dollar_signs(self) -> None:
        html = self.test_chase_html.format(
            '07/29/2023,CIRCLE K # 40645,,32.89,')
        formatter = OutputRecordFormatter()

        with io.StringIO(html) as html_input:
            with io.StringIO() as csv_output:
                with self.assertRaises(SyntaxError):
                    Chase(html_input, csv_output, formatter).scrape()


if __name__ == '__main__':
    unittest.main()
