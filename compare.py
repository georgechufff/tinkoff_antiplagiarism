import ast
import argparse
import zipfile
from levenshtein import *

parser = argparse.ArgumentParser()
parser.add_argument("file_1", type=str)
parser.add_argument("file_2", type=str)
args = parser.parse_args()

z = zipfile.ZipFile('plagiat.zip', 'r')

file1 = open(f'{args.file_1}', 'r')
file2 = open(f'{args.file_2}', 'w')

for line in file1.readlines():
    if '\n' in line:
        str1, str2 = line[:-1].split()
    else:
        str1, str2 = line.split()
    print(str1, str2)
    try:
        str1 = z.open(str1).read().decode()
        str2 = z.open(str2).read().decode()
        file2.write(str(levenshtein(str1, str2)) + '\n')
    except KeyError:
        print("Какого-то из этих файлов нет")

z.close()
file1.close()
file2.close()