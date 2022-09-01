import os

from PIL import Image
import pytesseract

from say import say
from helpers.hash_file import hash_file

def hasExt(path, E):
    return any(path.endswith(ext) for ext in E.split())

def scanDir(DB, parent, dir, count, scanId):
    say(DB, f'Scanning {dir.path}')

    fId = DB.addNode(dir.path, [], False)
    DB.addNode('source', [fId, scanId], False, True)
    DB.addNode('name', [fId, DB.addNode(dir.name, [], False)], False, True)
    DB.addNode('size', [fId, DB.addNode(os.stat(dir).st_size, [], False)], False, True)
    DB.addNode('accessed', [fId, DB.addNode(os.stat(dir).st_atime, [], False)], False, True)
    DB.addNode('modified', [fId, DB.addNode(os.stat(dir).st_mtime, [], False)], False, True)
    DB.addNode('parent', [fId, parent], False, True)

    if dir.is_dir() and (count < 100):
        say(DB, f'Scanning directory')
        for item in os.scandir(dir):
            count = scanDir(DB, fId, item, count, scanId)

    if dir.is_file():
        DB.addNode('md5_hash', [fId, DB.addNode(hash_file(dir.path), [], False)])
        # if any(dir.path.endswith('.'+ext) for ext in ['png', 'jpg']):
        if hasExt(dir.path, 'png jpg PNG JPG JPEG'):
            try:
                say(DB, f'Running Tesseract OCR on {dir.path}')
                tesseractParse = pytesseract.image_to_string(Image.open(dir.path))
                DB.addNode('tesseract_parse', [fId, DB.addNode(tesseractParse, [], False)], False, True)
            except Exception as ex:
                print(ex)
        if hasExt(dir.path, 'py js txt java md ipynb tex'):
            try:
                say(DB, f'Reading lines from text file {dir.path}')
                with open(dir.path, 'r') as txtFile:
                    lines = txtFile.readlines()
                    if len(lines) <= 1000:
                        for line in lines:
                            DB.addNode('line_from', [DB.addNode(line, [], False), fId], False, True)
            except Exception as ex:
                print(ex)
    return count+1
