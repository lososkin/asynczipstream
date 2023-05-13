# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import os
import tempfile
import time
import unittest
import asynczipstream
import zipfile
import asyncio


SAMPLE_FILE_RTF = 'tests/sample.rtf'


def async_test(f):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f(*args, **kwargs))
    return wrapper


class ZipInfoTestCase(unittest.TestCase):
    pass


class asynczipstreamTestCase(unittest.TestCase):
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
        asynczipstream.ZipFile()

    def test_init_mode(self):
        try:
            asynczipstream.ZipFile(mode='w')
        except Exception as err:
            self.fail(err)

        for mode in ['wb', 'r', 'rb', 'a', 'ab']:
            self.assertRaises(Exception, asynczipstream.ZipFile, mode=mode)

        for mode in ['wb', 'r', 'rb', 'a', 'ab']:
            self.assertRaises(Exception, asynczipstream.ZipFile, mode=mode + '+')

    @async_test
    async def test_write_file(self):
        z = asynczipstream.ZipFile(mode='w')
        for fileobj in self.fileobjs:
            z.write(fileobj.name)

        f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)
        async for chunk in z:
            f.write(chunk)
        f.close()

        z2 = zipfile.ZipFile(f.name, 'r')
        self.assertFalse(z2.testzip())

        os.remove(f.name)

    @async_test
    async def test_write_iterable(self):
        z = asynczipstream.ZipFile(mode='w')
        async def string_generator():
            for _ in range(10):
                yield b'zipstream\x01\n'
        data = [string_generator(), string_generator()]
        for i, d in enumerate(data):
            z.write_iter(iterable=d, arcname='data_{0}'.format(i))

        f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)
        async for chunk in z:
            f.write(chunk)
        f.close()

        z2 = zipfile.ZipFile(f.name, 'r')
        self.assertFalse(z2.testzip())

        os.remove(f.name)

    @async_test
    async def test_write_iterable_with_date_time(self):
        file_name_in_zip = "data_datetime"
        file_date_time_in_zip = time.strptime("2011-04-19 22:30:21", "%Y-%m-%d %H:%M:%S")

        z = asynczipstream.ZipFile(mode='w')
        async def string_generator():
            for _ in range(10):
                yield b'zipstream\x01\n'
        z.write_iter(iterable=string_generator(), arcname=file_name_in_zip, date_time=file_date_time_in_zip)

        f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)
        async for chunk in z:
            f.write(chunk)
        f.close()

        z2 = zipfile.ZipFile(f.name, 'r')
        self.assertFalse(z2.testzip())

        self.assertEqual(file_date_time_in_zip[0:5], z2.getinfo(file_name_in_zip).date_time[0:5])

        os.remove(f.name)

    @async_test
    async def test_writestr(self):
        z = asynczipstream.ZipFile(mode='w')

        with open(SAMPLE_FILE_RTF, 'rb') as fp:
            z.writestr('sample.rtf', fp.read())

        f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)
        async for chunk in z:
            f.write(chunk)
        f.close()

        z2 = zipfile.ZipFile(f.name, 'r')
        self.assertFalse(z2.testzip())

        os.remove(f.name)

    @async_test
    async def test_partial_writes(self):
        z = asynczipstream.ZipFile(mode='w')
        f = tempfile.NamedTemporaryFile(suffix='zip', delete=False)

        with open(SAMPLE_FILE_RTF, 'rb') as fp:
            z.writestr('sample1.rtf', fp.read())

        async for chunk in z.flush():
            f.write(chunk)

        with open(SAMPLE_FILE_RTF, 'rb') as fp:
            z.writestr('sample2.rtf', fp.read())

        async for chunk in z.flush():
            f.write(chunk)

        async for chunk in z:
            f.write(chunk)
        
        f.close()
        z2 = zipfile.ZipFile(f.name, 'r')
        self.assertFalse(z2.testzip())

        os.remove(f.name)

    def test_write_iterable_no_archive(self):
        z = asynczipstream.ZipFile(mode='w')
        async def async_range(x):
            for i in range(x):
                yield i
        self.assertRaises(TypeError, z.write_iter, iterable=async_range(10))

if __name__ == '__main__':
    unittest.main()
