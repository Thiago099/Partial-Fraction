import re
import copy
def solve(input):
    def serialize(s):
        return [[1 if x.group(1) == 'x' or not x.group(1) else int(x.group(1)), int(x.group(2)) if x.group(1) == 'x' and x.group(2) else int(x.group(3)) if x.group(3) else 1] for x in re.finditer('(-?\d+)?(x)\^?(-?\d+)?', s)] + [[int(x.group(1)), 0]for x in re.finditer('(?<!\^)(\d+)(?!x)', s)]
    
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
    preb = [ [(int(x.group(2)) if x.group(2) else 1), x.group(1)] for x in re.finditer('(\(.*?\))\^?(\d+)?',input[i+1::])]

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
        
    def build(obj):
        if(obj[1]) == 0:
            return str(obj[0])
        if(obj[1] == 1):
            return str(obj[0]) + 'x'
        return str(obj[0]) + 'x^' + str(obj[1])

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
                current_a.append(str(i[0]))
        for i in bm:
            if(degree == i[1]):
                current_bm.append(i[0]) 
                working = True
        if(not working):
            break
        simplified_bm.append(current_bm if len(current_bm) > 0 else '0')
        simplified_a.append(current_a if len(current_a) > 0 else '0')
        degree += 1
    
    expression = []
    for i in range(len(b)):
        term = []
        for j in b[i]:
            term.append(build(j))
        expression.append('[' + ('(' + ' + '.join(term) + ')' if len(term) > 1 else term[0]) + '/' + div[i]+']')
    print(' + '.join(expression))
    print()
    for i in range(len(simplified_a)):
        print(' + '.join(simplified_bm[i]) + ' = ' + ' + '.join(simplified_a[i]))