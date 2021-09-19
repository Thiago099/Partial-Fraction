import re
import copy
def solve(input):
    for i in range(len(input)):
        if(input[i] == '/'):
            break

    def serialize(s):
        return [ [int(x.group(1)),( int(x.group(3)) if x.group(3) else 1 if x.group(2) else 0)] for x in re.finditer('(-?\d)(x?)\^?(\d+)?', s)]


    def pad(len):
        ret = ''
        for i in range(len):
            ret+='\t'
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
                ret.append([str(j[0]) + i[0], j[1] + i[1]])
        return ret
        
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

    ret = []

    i = 0
    def compile(v):
        return '0' if len(v) == 0 else ' + '.join(v)

    while(True):
        working = False
        c = []
        for j in range(len(a)):
            if(a[j][1] == i):
                c.append(build(a[j]))
                working = True
        d = []
        for j in range(len(bm)):
            if(bm[j][1] == i):
                d.append(build(bm[j]))
                working = True

        ret.append(compile(c) + ' = ' + compile(d))
        i += 1
        if(not working):
            break
    bbb = []
    for i in range(len(b)):
        bb = []
        for j in b[i]:
            bb.append(build(j))
        bbb.append('[(' + ' + '.join(bb) + ')/' + div[i]+']')
    print(' + '.join(bbb))
    print()
    for i in ret[:-1]:
        print(i)
