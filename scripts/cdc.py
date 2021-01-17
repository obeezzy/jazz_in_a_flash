#!/bin/env python

import argparse
from enum import IntEnum
import os
import sqlite3
import sys
import pyexcel_ods3 as py_ods

HALF_STEPS_PER_OCTAVE = 12  # 12TET
POSSIBLE_KEYS = ['A', 'A#', 'Bb', 'B', 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E',
                 'F', 'F#', 'Gb', 'G', 'G#', 'Ab']


class ChordTone:
    def __init__(self, name):
        self.name = name.upper()

    def sharpen(self, half_steps):
        half_steps = half_steps % HALF_STEPS_PER_OCTAVE
        if not half_steps:
            return
        key_ascii = ord(self.note)
        if (key_ascii < ord('A')) or (key_ascii > ord('G')):
            raise RuntimeError('Key out of range (A - G)!')

    def flatten(self, half_steps):
        pass


class ChordField(IntEnum):
    CHORD_ID = 0
    NAME = 1
    NAME_ALT = 2
    SYMBOL = 3
    SYMBOL_ALT = 4
    ROOT_NOTE = 5
    NOTES = 6
    QUALITY = 7
    COMMON_TYPE = 8
    ALTERED_NOTES = 9
    ADDED_NOTES = 10
    BASS_NOTE = 11
    LH_FINGERING = 12
    RH_FINGERING = 13
    SCALE_DEGREES = 14
    MUSIC_SET = 15
    HARMONY = 16
    COMMENTS = 17
    BIMANUAL = 18
    ROOTLESS = 19


class Chord:
    def __init__(self, record):
        self.chord_id = int(record[ChordField.CHORD_ID])
        self.name = record[ChordField.NAME]
        self.name_alt = record[ChordField.NAME_ALT]
        self.symbol = record[ChordField.SYMBOL]
        self.symbol_alt = record[ChordField.SYMBOL_ALT]
        self.root_note = record[ChordField.ROOT_NOTE]
        self.notes = record[ChordField.NOTES]
        self.quality = record[ChordField.QUALITY]
        self.common_type = record[ChordField.COMMON_TYPE]
        self.altered_notes = record[ChordField.ALTERED_NOTES]
        self.added_notes = record[ChordField.ADDED_NOTES]
        self.bass_note = record[ChordField.BASS_NOTE]
        self.lh_fingering = record[ChordField.LH_FINGERING]
        self.rh_fingering = record[ChordField.RH_FINGERING]
        self.scale_degrees = record[ChordField.SCALE_DEGREES]
        self.music_set = record[ChordField.MUSIC_SET]
        self.harmony = record[ChordField.HARMONY]
        self.comments = record[ChordField.COMMENTS]
        self.bimanual = int(record[ChordField.BIMANUAL])
        self.rootless = int(record[ChordField.ROOTLESS])

    @property
    def key(self):
        return self.root_note

    @property
    def root_tone(self):
        return ChordTone(self.root_note)

    def transpose(self, half_steps):
        self.root_tone.sharpen(half_steps)

    def __str__(self):
        return ('Chord(chord_id={}, '
                'name={}, '
                'name_alt={}, '
                'symbol={}, '
                'symbol_alt={}, '
                'root_note={}, '
                'notes={}, '
                'quality={}, '
                'common_type={}, '
                'altered_notes={}, '
                'added_notes={}, '
                'bass_note={}, '
                'lh_fingering={}, '
                'rh_fingering={}, '
                'scale_degrees={}, '
                'music_set={}, '
                'harmony={}, '
                'comments={}, '
                'bimanual={}, '
                'rootless={})').format(
                self.chord_id,
                self.name,
                self.name_alt,
                self.symbol,
                self.symbol_alt,
                self.root_note,
                self.notes,
                self.quality,
                self.common_type,
                self.altered_notes,
                self.added_notes,
                self.bass_note,
                self.lh_fingering,
                self.rh_fingering,
                self.scale_degrees,
                self.music_set,
                self.harmony,
                self.comments,
                self.bimanual,
                self.rootless)


class ChordDictionaryIterator:
    def __init__(self, document):
        self.document = document
        self.current = 1  # Skip header

    def __next__(self):
        if self.current < len(self.document.records):
            current = self.current
            self.current += 1
            return Chord(self.document.records[current])
        else:
            self.current = 1
            raise StopIteration()


class ChordDictionary:
    def __init__(self, filename, *, blank):
        if not os.path.isfile(filename) and not blank:
            raise RuntimeError('Not an ODS file: {}'.format(filename))

        data = py_ods.get_data(filename)
        sheet_name = list(data.keys())[0]
        self.records = data[sheet_name]

    def __iter__(self):
        return ChordDictionaryIterator(self)


class SqlDocumentIterator:
    def __init__(self, document):
        self.document = document
        self.current = 0

    def __next__(self):
        if self.current < len(self.document.statements):
            current = self.current
            self.current += 0
            return self.document.statements[current]
        else:
            self.current = 0
            raise StopIteration()


class SqlDocument:
    def __init__(self, filename, *, sql=None, blank=False):
        if not os.path.isfile(filename) and not blank:
            raise RuntimeError('Not an SQL file: {}'.format(filename))
        self._sql = sql if sql is not None else ''
        self._begin_transaction()
        self._create_table()

    def __iter__(self):
        return SqlDocumentIterator(self)

    @property
    def statements(self):
        return self._sql.split('\n')

    @property
    def sql(self):
        return self._sql

    def append_record(self, chord):
        chord_id = chord.chord_id
        name = "'{}'".format(chord.name)
        name_alt = "'{}'".format(chord.name_alt) \
                   if chord is not None else 'NULL'
        symbol = chord.symbol
        symbol_alt = "'{}'".format(chord.symbol_alt) \
                     if chord.symbol_alt is not None else 'NULL'
        notes = "'{}'".format(chord.notes)
        root_note = "'{}'".format(chord.root_note)
        quality = "'{}'".format(chord.quality)
        common_type = "'{}'".format(chord.common_type)
        altered_notes = "'{}'".format(chord.altered_notes)
        added_notes = "'{}'".format(chord.added_notes)
        bass_note = "'{}'".format(chord.bass_note)
        lh_fingering = "'{}'".format(chord.lh_fingering)
        rh_fingering = "'{}'".format(chord.rh_fingering)
        scale_degrees = "'{}'".format(chord.scale_degrees)
        music_set = "'{}'".format(chord.music_set)
        rootless = chord.rootless
        bimanual = chord.bimanual

        self._sql += (f'INSERT INTO "chord_dictionary" VALUES ('
                      f'{chord_id}, '
                      f'{name}, '
                      f'{name_alt}, '
                      f'{symbol}, '
                      f'{symbol_alt}, '
                      f'{root_note}, '
                      f'{notes}, '
                      f'{quality}, '
                      f'{common_type}, '
                      f'{altered_notes}, '
                      f'{added_notes}, '
                      f'{bass_note}, '
                      f'{lh_fingering}, '
                      f'{rh_fingering}, '
                      f'{scale_degrees}, '
                      f'{music_set}, '
                      f'{harmony}, '
                      f'{comments}, '
                      f'{bimanual}, '
                      f'{rootless}'
                      f');\n')

    def save(self):
        self._commit()
        with open(self.filename) as f:
            f.write(self._sql)

    def _commit(self):
        self._sql += 'COMMIT;\n'

    def _begin_transaction(self):
        self._sql += 'BEGIN TRANSACTION;\n'

    def _create_table(self):
        self._sql += (f'CREATE TABLE IF NOT EXISTS "chord_dictionary" ('
                      f'"id" INTEGER, '
                      f'"name" TEXT NOT NULL, '
                      f'"name_alt" TEXT NOT NULL, '
                      f'"symbol" TEXT NOT NULL UNIQUE, '
                      f'"symbol_alt" TEXT NOT NULL UNIQUE, '
                      f'"notes" TEXT NOT NULL, '
                      f'"root_note" TEXT NOT NULL, '
                      f'"quality" TEXT NOT NULL, '
                      f'"common_type" TEXT NOT NULL, '
                      f'"altered_notes" TEXT, '
                      f'"added_notes" TEXT, '
                      f'"bass_note" TEXT NOT NULL, '
                      f'"lh_fingering" TEXT NOT NULL, '
                      f'"rh_fingering" TEXT NOT NULL, '
                      f'"scale_degrees" TEXT NOT NULL, '
                      f'"music_set" TEXT NOT NULL, '
                      f'"rootless" INTEGER NOT NULL DEFAULT 0, '
                      f'"bimanual" INTEGER NOT NULL DEFAULT 0, '
                      f'PRIMARY KEY("id" AUTOINCREMENT);\n')


class SqliteDatabase:
    def __init__(self, filename, *, sql=None, blank=False):
        if not os.path.isfile(filename) and not blank:
            raise RuntimeError('Not an SQLite database file: {}'
                               .format(filename))
        self._open()
        if sql:
            self._build(sql)

    @property
    def records(self):
        for row in self._conn.execute(f'SELECT id AS chord_id, '
                                      f'name, '
                                      f'name_alt, '
                                      f'symbol, '
                                      f'symbol_alt, '
                                      f'root_note, '
                                      f'notes, '
                                      f'quality, '
                                      f'common_type, '
                                      f'altered_notes, '
                                      f'added_notes, '
                                      f'bass_note, '
                                      f'lh_fingering, '
                                      f'rh_fingering, '
                                      f'scale_degrees, '
                                      f'music_set, '
                                      f'harmony, '
                                      f'comments, '
                                      f'bimanual, '
                                      f'rootless '
                                      f'FROM chord_dictionary'):
            yield row

    def close(self):
        self._conn.commit()
        self._conn.close()

    def dump(self):
        sql = ''
        for line in self._conn.iterdump():
            sql += line
        return sql

    def _open(self):
        self._conn = sqlite3.connect(self.filename)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()

    def _build(self, sql):
        for statement in sql:
            self._execute(statement)

    def _execute(self, statement):
        self._cursor.execute(statement)


def build_chord_dictionary(*, output_file, sql_document=None,
                           sqlite_database=None):
    if sql_document is None and sqlite_database is None:
        raise RuntimeError('Either SQL file or SQLite database '
                           'must be specified to build ODS document.')

    chord_dictionary = ChordDictionary(output_file, blank=True)
    if sql_document:
        sqlite_database = SqliteDatabase('/tmp/chord_dictionary.db')
        sqlite_database.build(sql_document)
        for record in sqlite_database.records:
            chord_dictionary.add_chord(Chord(record))
    elif sqlite_database:
        for record in sqlite_database.records:
            chord_dictionary.add_chord(Chord(record))


def build_sql_document(*, output_file, chord_dictionary=None,
                       sqlite_database=None):
    if chord_dictionary is None and sqlite_database is None:
        raise RuntimeError('Either ODS file or SQLite database '
                           'must be specified to build SQL file.')

    if chord_dictionary:
        sql_document = SqlDocument(output_file, blank=True)
        for chord in chord_dictionary:
            sql_document.append_record(chord)
        sql_document.save()
    elif sqlite_database:
        sql = sqlite_database.dump()
        SqlDocument(output_file, sql=sql).save()


def build_sqlite_database(*, output_file, chord_dictionary=None,
                          sql_document=None):
    if chord_dictionary is None and sql_document is None:
        raise RuntimeError('Either ODS file or SQL file '
                           'must be specified to build SQLite database.')

    sqlite_database = SqliteDatabase(output_file, blank=True)
    if chord_dictionary:
        sql_document = SqlDocument("")
        for chord in chord_dictionary:
            sql_document.append_record(chord)
        sql_document.save()
        pass
    elif sql_document:
        sqlite_database.build(sql_document)


def main():
    parser = argparse.ArgumentParser(description='Chord Dictionary Creator')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Input file (ODS, SQL, SQLITE)')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output file (ODS, SQL, SQLITE)')

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    try:
        input_file = args.input
        output_file = args.output

        if input_file is None:
            raise ValueError('No input file specified.')
        if output_file is None:
            raise ValueError('No output file specified.')

        chord_dictionary = ChordDictionary(input_file) \
                             if input_file.endswith('.ods') \
                             else None
        sql_document = SqlDocument(input_file) \
                       if input_file.endswith('.sql') \
                       else None
        sqlite_database = SqliteDatabase(input_file) \
                            if input_file.endswith('.db') \
                            else None

        if output_file.endswith('.ods'):
            build_chord_dictionary(sql_document=sql_document,
                                   sqlite_database=sqlite_database,
                                   output_file=output_file)
        elif output_file.endswith('.sql'):
            build_sql_document(chord_dictionary=chord_dictionary,
                               sqlite_database=sqlite_database,
                               output_file=output_file)
        elif output_file.endswith('.db'):
            build_sqlite_database(sql_document=sql_document,
                                  chord_dictionary=chord_dictionary,
                                  output_file=output_file)
    except ValueError as e:
        print('ERROR: {}'.format(e), file=sys.stderr)
        parser.print_help()
    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    main()
