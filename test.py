def func(n: str):
    alf = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
    string = n + ' 'f'запретил букву'
    for i in range(0, len(string.replace(' ', '')) - 1):
        if alf[i].lower() in string:
            string = string.replace(alf[i].lower(), '')
        print(string + ' 'f'{alf[i].lower()}')


n = input()
func(n)


