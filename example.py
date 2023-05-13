# -*- coding: utf-8 -*-
import os
import asynczipstream
import zipfile
import asyncio

async def main():
    with asynczipstream.ZipFile(mode='w', compression=asynczipstream.ZIP_DEFLATED) as z:
        z.write('LICENSE')
        z.write('LICENSE', arcname='stuff/LICENSE')

        with open('tests/sample.rtf', 'rb') as fp:
            z.writestr('sample.rtf', fp.read())

        for root, directories, files in os.walk('asynczipstream'):
            for filename in files:
                path = os.path.join(root, filename)
                z.write(path, path)

        with open('test.zip', 'wb') as f:
            async for chunk in z:
                f.write(chunk)


    with zipfile.ZipFile('test.zip') as z:
        z.testzip()

asyncio.run(main())