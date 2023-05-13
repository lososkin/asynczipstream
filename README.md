
# asynczipstream

zipstream.py is a zip archive generator based on python 3.3's zipfile.py. It was created to
generate a zip file generator for streaming (ie web apps). This is beneficial for when you
want to provide a downloadable archive of a large collection of regular files, which would be infeasible to
generate the archive prior to downloading or of a very large file that you do not want to store entirely on disk or on memory.

The archive is generated as an iterator of strings, which, when joined, form
the zip archive. For example, the following code snippet would write a zip
archive containing files from 'path' to a normal file:

```python
import asynczipstream
import asyncio

async def main():
    z = asynczipstream.ZipFile()
    z.write('path/to/files')

    with open('zipfile.zip', 'wb') as f:
        async for data in z:
            f.write(data)

asyncio.run(main())
```

zipstream also allows to take as input a byte string iterable and to generate
the archive as an iterator.
This avoids storing large files on disk or in memory.
To do so you could use something like this snippet:

```python
import asynczipstream
import asyncio

async def main():
    async def iterable():
        for _ in range(10):
            yield b'this is a byte string\x01\n'

    z = asynczipstream.ZipFile()
    z.write_iter('my_archive_iter', iterable())

    with open('zipfile.zip', 'wb') as f:
        async for data in z:
            f.write(data)

asyncio.run(main())
```

Of course both approach can be combined:

```python
import asynczipstream
import asyncio

async def main():
    async def iterable():
        for _ in range(10):
            yield b'this is a byte string\x01\n'

    z = asynczipstream.ZipFile()
    z.write('path/to/files', 'my_archive_files')
    z.write_iter('my_archive_iter', iterable())

    with open('zipfile.zip', 'wb') as f:
        async for data in z:
            f.write(data)

asyncio.run(main())
```

If the zlib module is available, asynczipstream.ZipFile can generate compressed zip
archives.

## Installation

```
pip install asynczipstream
```

## Requirements

  * Python 3.8+


### aiohttp Example

```python
from aiohttp import web, hdrs
import asynczipstream

async def handle_license(request):
    """
        Example with file from disk
    """
    filename = "license.zip"
    response = web.StreamResponse(
        status=200,
        headers={
            hdrs.CONTENT_TYPE: "application/octet-stream",
            hdrs.CONTENT_DISPOSITION: (f"attachment; " f'filename="{filename}"; '),
        },
    )
    await response.prepare(request)

    z = asynczipstream.ZipFile()
    z.write('LICENSE')
    async for data in z:
        await response.write(data)
    return response

async def handle_readme(request):
    """
        Example with file from iterable object
    """
    filename = "readme.zip"
    response = web.StreamResponse(
        status=200,
        headers={
            hdrs.CONTENT_TYPE: "application/octet-stream",
            hdrs.CONTENT_DISPOSITION: (f"attachment; " f'filename="{filename}"; '),
        },
    )
    await response.prepare(request)

    async def iterable(filename):
        with open(filename, "rb") as f:
            yield f.readline()

    z = asynczipstream.ZipFile()
    z.write_iter('README.md', iterable("README.md"))
    async for data in z:
        await response.write(data)
    return response


app = web.Application()
app.add_routes([web.get('/license', handle_license),web.get('/readme', handle_readme)])

if __name__ == '__main__':
    web.run_app(app)
```

## Running tests

Just run the following command: `python -m unittest discover`
