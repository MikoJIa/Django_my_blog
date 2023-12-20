def func(n: str):
    alf = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    string = n + ' 'f'запретил букву'
    for i in alf.lower():
        if i.lower() in string:
            print(string + ' 'f'{i.lower()}')
            string = string.replace(i.lower(), '').strip().replace('  ', ' ')


n = input()
func(n)


