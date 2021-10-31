import cmath, copy, random, json

def my_int(x):
    return int(x) if int(x) == x else x

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

# Translated from fortran version in "Numerical Recipes" book.
def ludcmp(a_in):
    a = copy.deepcopy(a_in)
    n = len(a)
    indx = [None] * n
    n_max = 100
    tiny = 1e-20
    parity = True
    vv = []
    for i in range(n):
        a_max = 0
        for j in range(n):
            this_abs = abs(a[i][j])
            a_max = a_max if a_max > this_abs else this_abs
        if not a_max:
            return {"determinant": 0}
        vv.append(1/a_max)
    for j in range(n):
        for i in range(j):
            sum = a[i][j]
            for k in range(i):
                sum -= a[i][k] * a[k][j]
            a[i][j] = sum
        a_max = 0
        for i in range(j, n):
            sum = a[i][j]
            for k in range(j):
                sum -= a[i][k] * a[k][j]
            a[i][j] = sum
            dum = vv[i] * abs(sum)
            if dum >= a_max:
                i_max = i
                a_max = dum
        if not j == i_max:
            for k in range(n):
                [a[i_max][k], a[j][k]] = [a[j][k], a[i_max][k]]
            parity = not parity
            vv[i_max] = vv[j]
        indx[j] = i_max
        if not a[j][j]:
            return {"determinant": 0}
            # a[j][j] = tiny
        if not j == n:
            dum = 1/a[j][j]
            for i in range(j + 1, n):
                a[i][j] *= dum
        det = 1 if parity else -1
        for i in range(n):
            det *= a[i][i]
    return {"determinant": det, "lu": a, "indx":indx}

def lubskb(a, indx, b_in):
    b = copy.deepcopy(b_in)
    n = len(a)
    ii = -1
    for i in range(n):
        ll = indx[i]
        sum = b[ll]
        b[ll] = b[i]
        if not ii == -1:
            for j in range(ii, i):
                sum -= a[i][j] * b[j]
        elif sum:
            ii = i
        b[i] = sum
    for i in range(n - 1, -1, -1):
        sum = b[i]
        if i < n - 1:
            for j in range(i + 1, n):
                sum -= a[i][j] * b[j]
        b[i] = sum / a[i][i]
    return b

def invert(a):
    n = len(a)
    identity = []
    zero_row = [0] * n
    for i in range(n):
        zero_copy = list(zero_row)
        zero_copy[i] = 1
        identity.append(zero_copy)
    results = ludcmp(a)
    a_inv_transpose = []
    for j in range(n):
        a_inv_transpose.append(lubskb(results["lu"], results["indx"], identity[j]))
    a_transpose = []
    for i in range(n):
        a_transpose.append(list(zero_row))
        for j in range(n):
            a_transpose[i][j] = a_inv_transpose[j][i]
    return a_transpose

def parse(square_in, rect_in = '[]'):
    try:
        a = json.loads(square_in)
    except:
        return {'error': "There is something wrong with your matrix ('A')."}
    if not isinstance(a, list):
        return {'error': 'Your matrix should be a comma-separated list of lists, with both the inner- and outer lists enclosed by square brackets.'}
    n = len(a)
    number_of_wrong_lists = 0
    number_of_wrong_lengths = 0
    for inner_list in a:
        if not isinstance(inner_list, list):
            number_of_wrong_lists += 1
        else:
            if not len(inner_list) == n:
                number_of_wrong_lengths += 1
    if number_of_wrong_lists:
        return {'error': str(number_of_wrong_lists) + ' of your inner lists have/has something wrong with them/it.'}
    if number_of_wrong_lengths:
        return {'error': str(number_of_wrong_lengths) + ' of your inner lists have/has the wrong length, ie have/has a length other than ' + str(n) + ". Recall that 'A' must be a square matrix."}
    try:
        rect_in = json.loads(rect_in)
    except:
        return {"error": "There is something wrong with your inhomogeneous part ('B')."}
    if rect_in:
        if not isinstance(rect_in[0], list):
            rect_in = [rect_in]
        number_of_wrong_lists = 0
        number_of_wrong_lengths = 0
        for inner_list in rect_in:
            if not isinstance(inner_list, list):
                number_of_wrong_lists += 1
            else:
                if not len(inner_list) == n:
                    number_of_wrong_lengths += 1
        if number_of_wrong_lists:
            return {"error": str(number_of_wrong_lists) + " of the inner lists for your inhomogeneous part have/has something wrong with them/it."}
        if number_of_wrong_lengths:
            return {"error": str(number_of_wrong_lengths) + " of the inner lists for your inhomogeneous part have/has the wrong length, ie have/has a length other  than " + str(n) + "."}
    results = ludcmp(a)
    if results['determinant']:
        zero_row = [0] * n
        identity = []
        for i in range(n):
            row = list(zero_row)
            row[i] = 1
            identity.append(row)
        a_inv_transpose = []
        for j in range(n):
            a_inv_transpose.append(lubskb(results['lu'], results['indx'], identity[j]))
        a_inv = []
        for i in range(n):
            a_inv.append(list(zero_row))
            for j in range(n):
                a_inv[i][j] = a_inv_transpose[j][i]
        results['inverse matrix'] = a_inv
        solutions = []
        for row in rect_in:
            solutions.append(lubskb(results['lu'], results['indx'], row))
        results.pop('lu')
        results.pop('indx')
        if solutions:
            results['solutions'] = solutions
    results['original matrix'] = a
    return results

general = [ \
    'After "...herokuapp.com" above you should type "/json/" and then your polynomial.  Input your polynomial according to one of the two formats below: "array" or "string".', \
    'If you w   ant the response in html rather than in json, omit "/json" from the address.', \
    'Spaces are allowed - but discouraged - in whichever format you use, because a "%20" will replace each space after you hit "return", thereby making the address uglier.', \
    'The resulting page will show some "validity checks", along with the roots themselves.' \
]
array = [ \
    'This is a comma-separated list of coefficients, enclosed by square brackets.  List the coefficients in order of increasing exponent, ie starting with the "constant" term.', \
    'Example: 1+5x-4x**3 would be represented by the following array: [1,5,0,-4].', \
]
string = [ \
    'Each of the polynomial\'s coefficients may be represented as an integer or decimal but not as fraction, because "/" has special meaning in a URL.',\
    'Your variable must be a string which starts with a letter (upper- or lowercase) or underscore. If your variable has multiple characters, they may only be letters, underscores, or digits.',\
    'Represent the product of a coefficient and a variable in the usual sequence: coefficient before variable, and represent the multiplication operation either by * or in an implied manner (ie with nothing separating the coefficient and the variable).',\
    'Represent "x squared" either as "x**2" (preferably) or "x^2" (OK) but not as "x*x". Do likewise for larger powers.', \
    'You need not represent the absolute value of a coefficient if it equals 1.  For instance you may type "x" instead of "1x" or "1*x", or "-x" instead of "-1x" or "-1*x".',\
    'You need not type the polynomial\'s terms in any particular order (such as largest power first or last).',\
    'You need not include any terms in the polynomial for which the coefficient is zero. For instance you may write "4x**2-9" instead of "4x**2+0x-9".',\
]
