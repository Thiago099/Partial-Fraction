import re
import copy
import math
import system as si

def solve(input):
    def serialize(s):
        return [[1 if x.group(1) == 'x' or not x.group(1) else int(x.group(1)), int(x.group(2)) if x.group(1) == 'x' and x.group(2) else int(x.group(3)) if x.group(3) else 1] for x in re.finditer(r'(-?\d+)?(x)\^?(-?\d+)?', s)] + [[int(x.group(1)), 0]for x in re.finditer(r'(?<!\^)(\d+)(?!x)', s)]
    
    def pad(len):
        ret = ''
        for i in range(len):
            ret += '\t'
        return ret

    def power(exp, value):
        applied = []
        command = ''
        a = []
        b = []
        depth = 0
        for i in range(value):
            cur = chr(i + ord('a'))
            command += pad(depth) + 'for ' + cur +' in exp:\n'
            a.append(cur + '[0]')
            b.append(cur + '[1]')
            depth += 1
        exec(command + '\n' + pad(depth) + 'applied.append([' + ' * '.join(a) + ', ' + ' + '.join(b) +'])')
        simplfied = []
        for i in range(len(applied)):
            found = False
            for j in simplfied:
                if(applied[i][1] == j[1]):
                    found = True
                    break
            if(found):
                continue
            cur = applied[i]
            for j in range(len(applied)):
                if(j != i and cur[1] == applied[j][1]):
                    cur[0] += applied[j][0]
            simplfied.append(cur)
        return simplfied

    def mul_str_int(a, b):
        ret = []
        for i in a:
            for j in b:
                ret.append([(str(j[0]) if j[0] != 1 else '') + i[0], j[1] + i[1]])
        return ret
    
    for i in range(len(input)):
        if(input[i] == '/'):
            break
    
    a = serialize(input[:i])
    preb = [ [(int(x.group(2)) if x.group(2) else 1), x.group(1)] for x in re.finditer(r'(\(.*?\))\^?(\d+)?',input[i+1::])]

    div = []
    letter = 0
    b = []
    bmul = []
    bc = []
    for i in preb:
        bc.append(power(serialize(i[1]),i[0]))
    for i in range(len(preb)):
        for j in range(preb[i][0]):
            cbc =  copy.deepcopy(bc)
            cj = cbc[i]
            del cbc[i]
            cur = cbc[0]
            bmul.append(cur)
                    
            highest = 1
            for k in re.finditer('\^(\d+)', preb[i][1]):
                kk = int(k.group(1))
                if(kk > highest):
                    highest = kk
            pair = []
            for k in range(highest-1,-1,-1):
                pair.append(k)

            cb = []
            for k in range(highest):
                cb.append([chr(letter + k + ord('A')), pair[k]])
            b.append(cb)
            letter += highest 
            div.append(preb[i][1] + ('^' + str(j+1) if j > 0 else ''))
    bm = []
    for i in range(len(b)):
        bm += mul_str_int(b[i],bmul[i])
        

    simplified_bm = []
    simplified_a = []
    degree = 0
    while(True):
        working = False
        current_bm = []
        current_a = []
        for i in a:
            if(degree == i[1]):
                working = True
                current_a.append(i[0])
        for i in bm:
            if(degree == i[1]):
                current_bm.append(i[0]) 
                working = True
        if(not working):
            break
        simplified_bm.append(current_bm if len(current_bm) > 0 else '0')
        
        sum_a = 0
        for i in current_a:
            sum_a += i
        simplified_a.append(sum_a)
        degree += 1

    # for i in range(len(simplified_a)):
    #     print(' + '.join(simplified_bm[i]) + ' = ' + str(simplified_a[i]))

    split_bm = []
    width = 0
    for i in simplified_bm:
        current_line = []
        for j in i:
            result = re.search(r'(-?\d+)?(\w)', j)
            current_symbol = [ord(result.group(2)) - ord('A'), int(result.group(1))] if result.group(1) else [ord(result.group(2)) - ord('A'), 1]
            if(current_symbol[0] > width):
                width = current_symbol[0]
            current_line.append(current_symbol)
        split_bm.append(current_line)
    
    
    matrix_bm = []
    for i in range(len(split_bm)):
        current_line = [0 for j in range(width+1)]
        for j in split_bm[i]:
            current_line[j[0]] = j[1]
        current_line.append(simplified_a[i])
        matrix_bm.append(current_line)

    si.solve(matrix_bm)
    
    solved_bm = {}
    for i in matrix_bm:
        for j in range(len(i)-1):
            if(i[j] == 1):
                solved_bm[chr(j+ord('A'))] = i[len(i)-1]
    
    def build(obj):
        if(obj[1]) == 0:
            return ''
        if(obj[1] == 1):
            return 'x'
        return  'x^' + str(obj[1])
    
    expression = []
    for i in range(len(b)):
        term = []
        for j in b[i]:
            k = solved_bm[j[0]]
            if(k != 0):
                if(k == 1):
                    if(j[1] == 0):
                        term.append('1')
                    else:
                        term.append(build(j))
                else:
                    term.append(j[0] + build(j))
        expression.append('[' + ('(' + ' + '.join(term) + ')' if len(term) > 1 else term[0] if len(term) == 1 else '0') + '/' + div[i]+']')
    return ' + ' . join(expression)
    