#!/usr/bin/env python3
import unittest

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


if __name__ == '__main__':
    unittest.main()
