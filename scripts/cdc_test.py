#!/bin/env python

import os
import unittest
import subprocess
from cdc import SqlDocument, SqliteDatabase

class TestCdc(unittest.TestCase):
    def setUp(self):
        self.input_ods = 'resources/chord_dictionary.ods'
        self.input_sql = 'resources/chord_dictionary.sql'
        self.input_sqlite = 'resources/chord_dictionary.sqlite'
        self.output_ods = 'artifacts/chord_dictionary.ods'
        self.output_sql = 'artifacts/chord_dictionary.sql'
        self.output_sqlite = 'artifacts/chord_dictionary.sqlite'

    def test_ods_to_sql(self):
        completed_process = subprocess.run(['./cdc.py',
                                            '-i', self.input_ods,
                                            '-o', self.output_sql],
                                           check=False)
        self.assertEqual(completed_process.returncode, 0,
                         'Failed to convert ODS to SQL.')
        self.assertTrue(os.path.isfile(self.output_sql),
                        'Failed to create SQL file.')
        sql_document = SqlDocument(self.output_sql)
        sqlite_database = SqliteDatabase(self.output_sqlite,
                                         sql=sql_document.sql, blank=True)
        records_exist = True if next(sqlite_database.records) else False
        self.assertTrue(records_exist, 'Failed to populate SQLite database.')

    def test_ods_to_sqlite(self):
        completed_process = subprocess.run(['./cdc.py',
                                           '-i', self.input_ods,
                                           '-o', self.output_sqlite])
        self.assertEqual(completed_process.returncode, 0,
                         'Failed to convert ODS to SQL.')
        self.assertTrue(os.path.isfile(self.output_sql),
                        'Failed to create SQL file.')
        sql_document = SqlDocument(self.output_sql)
        sqlite_database = SqliteDatabase(self.output_sqlite,
                                         sql=sql_document.sql, blank=True)
        records_exist = True if next(sqlite_database.records) else False
        self.assertTrue(records_exist, 'Failed to populate SQLite database.')

    def test_sql_to_ods(self):
        completed_process = subprocess.run(['./cdc.py',
                                           '-i', self.input_sql,
                                           '-o', self.output_ods])
        self.assertEqual(completed_process.returncode, 0,
                         'Failed to convert ODS to SQL.')
        self.assertTrue(os.path.isfile(self.output_sql),
                        'Failed to create SQL file.')
        sql_document = SqlDocument(self.output_sql)
        sqlite_database = SqliteDatabase(self.output_sqlite,
                                         sql=sql_document.sql, blank=True)
        records_exist = True if next(sqlite_database.records) else False
        self.assertTrue(records_exist, 'Failed to populate SQLite database.')

    def test_sql_to_sqlite(self):
        completed_success = subprocess.run(['./cdc.py',
                                           '-i', self.input_sql,
                                           '-o', self.output_sqlite])
        self.assertEqual(completed_process.returncode, 0,
                         'Failed to convert ODS to SQL.')
        self.assertTrue(os.path.isfile(self.output_sql),
                        'Failed to create SQL file.')
        sql_document = SqlDocument(self.output_sql)
        sqlite_database = SqliteDatabase(self.output_sqlite,
                                         sql=sql_document.sql, blank=True)
        records_exist = True if next(sqlite_database.records) else False
        self.assertTrue(records_exist, 'Failed to populate SQLite database.')

    def test_sqlite_to_ods(self):
        subprocess.run(['./cdc.py',
                        '-i', self.input_sqlite,
                        '-o', self.output_ods])

    def test_sqlite_to_sql(self):
        subprocess.run(['./cdc.py',
                        '-i', self.input_sqlite,
                        '-o', self.output_sql])

    def tearDown(self):
        pass

    def _generate_ods_file(self):
        pass

    def _generate_sql_file(self):
        pass

    def _generate_sqlite_file(self):
        pass
