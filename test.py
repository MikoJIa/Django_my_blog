
def is_pangram(s):
    string = s
    count = 0
    p = 'ABCDFGHJKLMNPQRSTVWXZ'
    new_lst = []
    for i in ''.join(string).lower():
        if i in p.lower() and i != ' ' and i != int():
                count += 1
                if i not in new_lst:
                    new_lst.append(i)
        else:
            count = count
    print(new_lst)
    if len(new_lst) == len(p):
        return True
    else:
        return False


print(is_pangram("1bcdefghijklmnopqrstuvwxyz"))