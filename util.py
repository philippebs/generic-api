import json
import time
import glob
import os
from os.path import exists


def getPathFileName(file_name: str, mais_atual:bool = True):
    list_files = glob.glob("./resource/*.json")

    list_files = sorted( list_files, key = lambda file: os.path.getctime(file), reverse=mais_atual)

    for file_json in list_files:
        if (str.lower(file_json).__contains__(str.lower(file_name))):
            return file_json
    return ''


def ler_json_file(file_name):
    file = getPathFileName(file_name=file_name).replace('.\\', '')
    with open(file, 'r', encoding='utf-8') as outfile:
        return outfile.read().rstrip()


def salvar_json(name, list_dados):
    param = json.dumps(list_dados, ensure_ascii=False, default=lambda o: o.__dict__, indent=3)
    f = open(f"./resource/{name}.json", "w", encoding='utf-8')
    f.write(param)
    f.close()


def exists_json(name):
    return exists(f'./resource/{name}.json')


if __name__ == '__main__':
    file_name = 'servers'
    # print(getPathFileName('prod'))
    print(os.path.realpath(__file__))