# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import tempfile
import unittest
import zipstream
import zipfile


SAMPLE_FILE_RTF = 'tests/sample.rtf'


class ZipInfoTestCase(unittest.TestCase):
    pass


class ZipStreamTestCase(unittest.TestCase):
    def setUp(self):
        self.fileobjs = [
            tempfile.NamedTemporaryFile(delete=False, suffix='.txt'),
            tempfile.NamedTemporaryFile(delete=False, suffix='.py'),
        ]

    def tearDown(self):
        for fileobj in self.fileobjs:
            fileobj.close()
            os.remove(fileobj.name)

    def test_init_no_args(self):
        zipstream.ZipFile()

    def test_init_mode(self):
        try:
            zipstream.ZipFile(mode='w')
        except Exception as err:
            self.fail(err)

        for mode in ['wb', 'r', 'rb', 'a', 'ab']:
            self.assertRaises(Exception, zipstream.ZipFile, mode=mode)

        for mode in ['wb', 'r', 'rb', 'a', 'ab']:
            self.assertRaises(Exception, zipstream.ZipFile, mode=mode + '+')

    def test_write_file(self):
        z = zipstream.ZipFile(mode='w')
        for fileobj in self.fileobjs:
            z.write(fileobj.name)

        f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)
        for chunk in z:
            f.write(chunk)
        f.close()

        z2 = zipfile.ZipFile(f.name, 'r')
        self.assertFalse(z2.testzip())

        os.remove(f.name)

    def test_write_iterable(self):
        z = zipstream.ZipFile(mode='w')
        def string_generator():
            for _ in range(10):
                yield b'zipstream\x01\n'
        data = [string_generator(), string_generator()]
        for i, d in enumerate(data):
            z.write_iter(iterable=d, arcname='data_{0}'.format(i))

        f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)
        for chunk in z:
            f.write(chunk)
        f.close()

        z2 = zipfile.ZipFile(f.name, 'r')
        self.assertFalse(z2.testzip())

        os.remove(f.name)

    def test_writestr(self):
        z = zipstream.ZipFile(mode='w')

        with open(SAMPLE_FILE_RTF, 'rb') as fp:
            z.writestr('sample.rtf', fp.read())

        f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)
        for chunk in z:
            f.write(chunk)
        f.close()

        z2 = zipfile.ZipFile(f.name, 'r')
        self.assertFalse(z2.testzip())

        os.remove(f.name)

    def test_partial_writes(self):
        z = zipstream.ZipFile(mode='w')
        f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)

        with open(SAMPLE_FILE_RTF, 'rb') as fp:
            z.writestr('sample1.rtf', fp.read())

        for chunk in z.flush():
            f.write(chunk)

        with open(SAMPLE_FILE_RTF, 'rb') as fp:
            z.writestr('sample2.rtf', fp.read())

        for chunk in z.flush():
            f.write(chunk)

        for chunk in z:
            f.write(chunk)
        
        f.close()
        z2 = zipfile.ZipFile(f.name, 'r')
        self.assertFalse(z2.testzip())

        os.remove(f.name)

    def test_write_iterable_no_archive(self):
        z = zipstream.ZipFile(mode='w')
        self.assertRaises(TypeError, z.write_iter, iterable=range(10))

if __name__ == '__main__':
    unittest.main()
