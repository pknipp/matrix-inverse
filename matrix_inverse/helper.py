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
        det = None
        if not a[j][j]:
            det = 0
            a[j][j] = tiny
        if not j == n:
            dum = 1/a[j][j]
            for i in range(j + 1, n):
                a[i][j] *= dum
        if det == None:
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

# Following is not used.
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

def parse(is_json, square_in, rect_in = '[]'):
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
        return {"error": "There is something wrong with your inhomogeneous part ('b', which equals " + rect_in + ")."}
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
    else:
        results["WARNING"] = "Because the determinant is zero, the solutions MAY be huge."
    if rect_in:
        solutions = []
        for row in rect_in:
            solution = lubskb(results["lu"], results["indx"], row)
            for i in range(len(solution)):
                solution[i] = my_int(solution[i])
            solutions.append(solution)
        results['solutions'] = solutions
    results.pop('lu')
    results.pop('indx')
    results['original matrix'] = a
    results['inhomogeneous part'] = rect_in
    results['determinant'] = my_int(results["determinant"])
    for i in range(n):
        if results["determinant"]:
            for j in range(n):
                results["inverse matrix"][i][j] = my_int(results["inverse matrix"][i][j])
    heading = 'RESULTS'
    results = {heading: results}
    if is_json:
        return results
    else:
        # Strip off heading, to make subsequent rows of code less cumbersome.
        results = results[heading]
        original_matrix = []
        for row in results["original matrix"]:
            html_row = ''
            for j in range(len(row)):
                html_row += '<td style=text-align:center>' + str(row[j]) + '</td>'
            original_matrix.append(html_row)
        if rect_in:
            inhomogeneous_part = []
            for j in range(n):
                html_row = ''
                for column in results["inhomogeneous part"]:
                    html_row += '<td style=text-align:center >' + str(column[j]) + '</td>'
                inhomogeneous_part.append(html_row)

        inverse_matrix = []
        if "inverse matrix" in results:
            for row in results["inverse matrix"]:
                html_row = ''
                for j in range(len(row)):
                    html_row += '<td style=text-align:center>' + str(row[j]) + '</td>'
                inverse_matrix.append(html_row)
        if rect_in:
            solutions = []
            for j in range(n):
                html_row = ''
                for column in results["solutions"]:
                    html_row += '<td style=text-align:center >' + str(column[j]) + '</td>'
                solutions.append(html_row)

        html = "<p align=center>" + heading + "</p>"
        html += "<p align=center>determinant = " + str(results["determinant"]) + "</p>"
        if "WARNING" in results:
            html += "<p align=center>" + results["WARNING"] + "</p>"
        html += '<p align=center><table border="1"><thead><tr><th colspan=' + str(n)
        html += '>original matrix</th><th colspan=' + str(len(rect_in))
        html += '>inhomogeneous part</th></tr></thead><tbody>'
        for i in range(n):
            html += '<tr>' + original_matrix[i]
            if rect_in:
                html += inhomogeneous_part[i]
        html += '</tr></tbody><thead><tr><th colspan=' + str(n)
        html += '>inverse matrix</th><th colspan=' + str(len(rect_in))
        html += '>solution</th></tr></thead><tbody>'
        for i in range(n):
            html += '<tr>'
            if "inverse matrix" in results:
                html += inverse_matrix[i]
            else:
                if not i:
                    html += '<td style=text-align:center rowspan=' + str(n) + ' colspan='
                    html += str(n) + '>does<br/>not<br/>exist</td>'
            if rect_in:
                html += solutions[i]
            html += '</tr>'
        return html + '</tbody></table></p><br/>'

instructions = [ \
    'After "...herokuapp.com" above you should type "/json/" and then your (square) matrix.', \
    'Spaces are allowed - but discouraged - in whichever format you use, because a "%20" will replace each space after you hit "return", thereby making the address uglier.', \
    'Input your matrix ("A") as a comma-separated list of comma-separated lists, each list being contained by square brackets.', \
    'example of a 2x2 matrix: [[1,2],[3,4]]', \
    'If you want to solve a matrix equation of the form Ax = b, then type "/" followed by one or more column vectors ("b"), formatted in the same way as for your square matrix.', \
    'example of 3 different linear systems of equations, each having the same square matrix A (which is the same as in the example above): /[[1,2],[3,4]]/[[3,5],[2,4],[-1,0]]', \
    'If you want the response in html rather than in json, omit "/json" from the address.', \
]
