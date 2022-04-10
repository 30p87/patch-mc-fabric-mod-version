#!/bin/python3

import zipfile
import shutil
import os
import json
from sys import platform
from argparse import ArgumentParser


def main(path, version, output, tmp):
    if tmp is None:
        if platform == 'win32':
            tmp = '.patchjar_TMP'
        else:
            tmp = '/tmp/patchjar'
    if path is None:
        for i in os.listdir():
            main(i, version, None, tmp)
    elif os.path.isdir(path):
        for i in os.listdir(path):
            main(f'{path}/{i}', version, None, tmp)
    elif path.endswith('.jar'):
        if output is None:
            output = path
        if zipfile.is_zipfile(path):
            # Extract
            zf = zipfile.ZipFile(path, 'r')
            zf.extractall(tmp)

            # patch
            with open(f'{tmp}/fabric.mod.json') as f:
                fmodjson = json.load(f)
            try:
                fmodjson['depends']['minecraft']
            except KeyError:
                pass
            else:
                if version is None:
                    del fmodjson['depends']['minecraft']
                else:
                    fmodjson['depends']['minecraft'] = version
                with open(f'{tmp}/fabric.mod.json', 'w') as f:
                    json.dump(fmodjson, f)

            # Repackage and clean
            shutil.make_archive(output, 'zip', tmp)
            os.rename(f'{output}.zip', output)
            shutil.rmtree(tmp)
        else:
            raise Warning(f'Argument {path} is not a valid zip-/jarfile')


if __name__ == '__main__':
    argparser = ArgumentParser(description='A simple tool to remove the Minecraft version limitation in Minecraft fabric mods. Useful for snapshot players who use simple mods that wouldn\'t need to be updated')
    argparser.add_argument('-p', '--path', help='The path to the file to patch', type=str)
    argparser.add_argument('-v', '--version', help='Which version string (regex or smth) the mod should require now', required=False, type=str)
    argparser.add_argument('-o', '--output', help='Which file the patched jar should be written to', required=False, type=str)
    argparser.add_argument('--tmp', help='Where to store the temporary files', required=False, type=str)
    args = argparser.parse_args()
    main(args.path, args.version, args.output, args.tmp)
