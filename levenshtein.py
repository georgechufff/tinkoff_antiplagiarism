def levenshtein(str1, str2):
    if len(str1) > len(str2):
        str1, str2 = str2, str1

    arr = [[0] * (len(str1) + 1) for _ in range(len(str2) + 1)]
    arr[0][0] = 0

    for i in range(1, len(str1) + 1):
        arr[0][i] = i
    for j in range(1, len(str2) + 1):
        arr[j][0] = j

    for i in range(1, len(str2) + 1):
        for j in range(1, len(str1) + 1):
            s = 1 if str1[j - 1] != str2[i - 1] else 0
            arr[i][j] = min(arr[i][j-1] + 1, arr[i-1][j] + 1, arr[i-1][j-1] + s)

    return arr[-1][-1]

print(levenshtein("Лабрадор", "Гибралтар"))
