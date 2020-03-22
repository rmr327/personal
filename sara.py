def h_psi(a, b):
    res = 0.0
    for i in range(1, b+1):
        res += (b**i)/(i**a)

    return '{:.10f}'.format(res)


def kruskal_frac(a, b):
    res = 0.0
    for i in range(1, b+1):
        res += ((a + b)**i)/i

    return '{:.10f}'.format(res)


def sqrt_star(n):
    if n < 2:
        return 1
    else:
        if n**0.5 < 2:
            return 1

        return 1 + sqrt_star(n**0.5)


def all_capital(L, start, stop):
    print(L[start])
    if L[start].islower():
        print('ab')
        return False
    elif start == stop:
        print('bb')
        return True
    else:
        all_capital(L, start+1, stop)


def count_case_switches(letters):
    count = 0

    try:
        state = letters[0].isupper()
    except IndexError:
        state = False  # place holder

    if len(letters) < 2:
        return 0
    else:
        for c in letters:
            if c.isupper() != state:
                state = c.isupper()
                count += 1

    return count


def qhash():
    print('To Exit type "quit"')
    user_input = None
    while user_input != 'quit':
        ones_num = 0
        two_num = 0
        user_input = input("Enter Text: ")
        if user_input == 'quit':
            break

        for a in user_input:
            n = str(ord(a))
            ones_num += int(n[-1])
            two_num += int(n[-2])

        print("Hash is {}".format(ones_num*two_num))


def barcode():
    user_input = input("Please Enter your ZIP Code:")
    dict = {1 : '00011', 2: '00101', 3: '00110', 4: ' 01001', 5: '01010', 6 : '01100', 7 : '10001', 8: '10010',
            9 : '10100', 0: '11000'}
    res = '1'
    res_2 = 0
    for c in user_input:
        res_2 += int(c)
        res += dict[int(c)]

    for c in str(res_2):
        res += dict[int(c)]

    res += '1'
    print('Your Bar Code is  {}'.format(res))


if __name__ == "__main__":
    t1 = "AAAbbbAcfGGGAA"
    barcode()
