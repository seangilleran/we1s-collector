#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""json_into_mongo.py
"""
import argparse
import json
import os
import zipfile

from pymongo import MongoClient


def main(filespath, namefilter='.json'):
    """Loop through zip files..."""

    client = MongoClient('mongo', 27017)
    db = client['we1s']
    db_collection = db['Corpus'] # filespath

    os.chdir(filespath)
    count = 0
    for (dirname, _dirs, files) in os.walk(filespath):
        for filename in files:
            if filename.endswith('.zip'):  # scan for zip files
                filepath = os.path.join(dirname, filename)
                # print('\n', filepath, '\n')
                source = zipfile.ZipFile(filepath, 'r')  # read zip
                for afile in source.filelist:
                    if namefilter:
                        if namefilter in afile.filename:
                            count += 1
                            # print('   ', afile.filename)
                            with source.open(afile) as f:
                                file_data = json.loads(f.read().decode('utf-8'))
                                db_collection.insert(file_data)
                    else:
                        count += 1
                        # print('   ', afile.filename)
        # print('   ' + str(count))
    client.close()
    print(count)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=__doc__)
    PARSER.add_argument('dir', nargs='?', default='',
                        help='directory tree to process')
    PARSER.add_argument('-n', '--namefilter', default='.json',
                        help='pattern for content filenames, e.g. json')
    ARGS = PARSER.parse_args()
    main(os.path.abspath(ARGS.dir), ARGS.namefilter)
