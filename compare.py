import ast
import re
import argparse
import zipfile


def levenshtein(str1: str, str2: str) -> int:
    if len(str1) > len(str2):
        str1, str2 = str2, str1

    cur_line = list(range(0, len(str1) + 1))
    for i in range(1, len(str2) + 1):
        prev_line = cur_line.copy()
        cur_line.clear()
        cur_line = [i] + [0] * len(str2)
        for j in range(1, len(str1) + 1):
            c = 1 if str1[j - 1] != str2[i - 1] else 0
            cur_line[j] = min(prev_line[j] + 1, cur_line[j - 1] + 1, prev_line[j - 1] + c)
        prev_line.clear()

    return cur_line[len(str1)]


def compare_files(file1, file2, z) -> None:
    for line in file1.readlines():
        if '\n' in line:
            first_file, second_file = line[:-1].split()
        else:
            first_file, second_file = line.split()
        try:
            if '.py' in first_file:
                if '.py' in second_file:
                    str1 = normalize_text(
                        z.open(first_file).read().decode()
                    )
                    str2 = normalize_text(
                        z.open(second_file).read().decode()
                    )
                    result = round(levenshtein(str1, str2) / len(str1), 3)
                    file2.write(str(result) + '\n')
                    print(f"The files {first_file} and {second_file} have been parsed and compared successfully.")
                else:
                    print(f"{second_file} is not a Python-file")
            else:
                print(f"{first_file} is not a Python-file")

        except KeyError:
            print(f"It seems that {first_file} or {second_file} doesn't exist.")
            continue
    file1.close()
    file2.close()
    z.close()


def normalize_text(file_text: str) -> str:
    ast_text = ast.parse(file_text)
    for vertex in ast.walk(ast_text):
        if isinstance(vertex, ast.Name):
            vertex.id = 'o'
    new_str = ast.unparse(ast_text)
    new_str = re.sub('#.*', '', new_str, len(new_str))
    new_str = re.sub('\n', '_n_', new_str, len(new_str))
    new_str = re.sub('""".*"""', '', new_str, len(new_str))
    return re.sub('_n_', '\n', new_str, len(new_str))


def main(script_parameters) -> None:
    try:
        file1 = open(script_parameters.file_1, 'r')
        file2 = open(script_parameters.file_2, 'w')
        print(f"The files {script_parameters.file_1} and {script_parameters.file_2} have been opened successfully.")
        zip_file = zipfile.ZipFile(input("Please insert zip-archive name where files are located: "), 'r')
        compare_files(file1, file2, zip_file)
        zip_file.close()
        file1.close()
        file2.close()
    except FileNotFoundError:
        print(f"Some of this files doesn't exist.")
    except UnicodeDecodeError:
        print(f"Decoding problem has occurred.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file_1", type=str)
    parser.add_argument("file_2", type=str)
    args = parser.parse_args()
    main(args)
