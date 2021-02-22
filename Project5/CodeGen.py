token = ''
var = ''
tokenNum = 0
tokenList = []
counter = 1
funcCounter = 0
funcList = []
regCount = 0
registers = ['t0','t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19']
output = []

brCounter = 0
openR = ''
closedR = ''
openZ = ''
closedZ = ''
varR = ''
bpo = 0
parenZ = False


def main(inputList):
    global tokenNum, token, tokenList

    #checks to see if the input is empty
    try:
        token = inputList[tokenNum][1]
        tokenList = inputList
    except IndexError:
        print('REJECT')
        exit()

    #Adds the last Accept
    tokenList.append(('FIN', '$'))

    #the beginning of the program (Sends it over to A: Program)
    A()

    if token == '$':
        for x in output:
            print("{:7} {:7} {:7} {:7} {:7}".format(x[0], x[1], x[2], x[3], x[4]))
    else:
        print('REJECT')


def checkTkn(checkToken):
    global tokenNum, token, tokenList, scope, scopeLvl, mainFunc
    identifier = tokenList[tokenNum][0]
    variable = tokenList[tokenNum][1]


    if token == checkToken:
        #Moves the token up 1
        tokenNum += 1
        if tokenList[tokenNum][0] == 'ID' or tokenList[tokenNum][0] == 'NUM':
            token = tokenList[tokenNum][0]
        else:
            token = tokenList[tokenNum][1]
    else:
        print('REJECT')
        exit()

def checkFuncs(list):
    global regCount, funcList, counter, funcCounter, registers
    i = 0

    while i < len(list):
        try:
            if list[i] in funcList[0] and list[i+1] == '(':
                func = list[i]

                list.pop(i)
                j = i
                while list[j] != ')':
                    if list[j] != '(' and list[j] != ',':
                        output.append((str(counter), 'arg', ' ', ' ', list[j]))
                        counter += 1
                    list.pop(j)

                list.pop(j)
                list.insert(i, registers[regCount])
                funcIndex = funcList[0].index(func)
                output.append((str(counter), 'call', func, str(funcList[funcIndex][1]), registers[regCount]))
                counter += 1
                regCount += 1
            elif list[i + 1] == '[':
                arrayVar = list[i]

                list.pop(i)
                list.pop(i)

                indexVar = list[i]

                list.pop(i)
                list.pop(i)

                arrayAddr = registers[regCount]

                output.append((str(counter), 'mult', indexVar, '4', registers[regCount]))
                counter += 1
                regCount += 1

                output.append((str(counter), 'disp', arrayVar, arrayAddr, registers[regCount]))

                list.insert(i, registers[regCount])

                counter += 1
                regCount += 1




        except IndexError:
            pass

        i += 1
    return list


def mult(operand1, operand2):
    global counter, regCount
    output.append((str(counter), 'mult', operand1, operand2, registers[regCount]))
    counter += 1
    reg = registers[regCount]
    regCount += 1
    return reg


def div(operand1, operand2):
    global counter, regCount
    output.append((str(counter), 'div', operand1, operand2, registers[regCount]))
    counter += 1
    reg = registers[regCount]
    regCount += 1
    return reg


def add(operand1, operand2):
    global counter, regCount
    output.append((str(counter), 'add', operand1, operand2, registers[regCount]))
    counter += 1
    reg = registers[regCount]
    regCount += 1
    return reg


def sub(operand1, operand2):
    global counter, regCount
    output.append((str(counter), 'sub', operand1, operand2, registers[regCount]))
    counter += 1
    reg = registers[regCount]
    regCount += 1
    return reg


def parenth(open, close, list):
    global counter, regCount, brCounter, bpo
    i = open + 1
    operations = []

    try:
        while i <= close - 1:
            operations.append(list[i][1])
            i += 1
    except IndexError:
        i = open + 1
        operations = []
        while i <= close - 1:
            operations.append(list[i])
            i += 1

    operations = checkFuncs(operations)

    #Parenthesis
    tempList = []
    if '(' in operations:
        while '(' in operations:
            newOpen = operations.index('(')
            i = newOpen
            while operations[i] != ')':
                if operations[i-1] == '(':
                    continue
                tempList.append(operations[i])
                operations.pop(i)
            tempList.append(operations[i])
            newClosed = len(tempList)-1
            operations.pop(i)

            operations.insert(i, parenth(newOpen, newClosed, tempList))

    while '*' in operations:
        tempIndex = operations.index('*')-1
        operator1 = operations[tempIndex]
        operator2 = operations[tempIndex+2]

        operations.pop(tempIndex)
        operations.pop(tempIndex)
        operations.pop(tempIndex)

        operations.insert(tempIndex, mult(operator1, operator2))

    while '/' in operations:
        tempIndex = operations.index('/')-1
        operator1 = operations[tempIndex]
        operator2 = operations[tempIndex + 2]

        operations.pop(tempIndex)
        operations.pop(tempIndex)
        operations.pop(tempIndex)

        operations.insert(tempIndex, div(operator1, operator2))

    while '+' in operations:
        tempIndex = operations.index('+')-1
        operator1 = operations[tempIndex]
        operator2 = operations[tempIndex + 2]

        operations.pop(tempIndex)
        operations.pop(tempIndex)
        operations.pop(tempIndex)

        operations.insert(tempIndex, add(operator1, operator2))

    while '-' in operations:
        tempIndex = operations.index('-')-1
        operator1 = operations[tempIndex]
        operator2 = operations[tempIndex + 2]

        operations.pop(tempIndex)
        operations.pop(tempIndex)
        operations.pop(tempIndex)

        operations.insert(tempIndex, sub(operator1, operator2))

    if {'<', '>', '>=', '<=', '==', '!='} & set(operations):
        operator = {'<', '>', '>=', '<=', '==', '!='} & set(operations)
        operator = operator.pop()

        tempIndex = operations.index(operator)-1
        operand1 = operations[tempIndex]
        operand2 = operations[tempIndex+2]

        output.append((str(counter), 'cmpr', operand1, operand2, registers[regCount]))
        newRegister = registers[regCount]
        bpo = counter
        counter += 1
        regCount +=1

        if operator == '>':
            output.append((str(counter), 'BRLEQ', newRegister, ' ', 'temp'))
            brCounter += 1
            counter += 1

        if operator == '>=':
            output.append((str(counter), 'BRLT', newRegister, ' ', 'temp'))
            counter += 1
            brCounter += 1

        if operator == '<':
            output.append((str(counter), 'BGE', newRegister, ' ', 'temp'))
            counter += 1
            brCounter += 1

        if operator == '<=':
            output.append((str(counter), 'BGT', newRegister, ' ', 'temp'))
            counter += 1
            brCounter += 1

        if operator == '==':
            output.append((str(counter), 'BEQ', newRegister, ' ', 'temp'))
            counter += 1
            brCounter += 1

        if operator == '!=':
            output.append((str(counter), 'BNE', newRegister, ' ', 'temp'))
            counter += 1
            brCounter += 1

        return newRegister

    newRegister = operations[0]
    return newRegister

def A():
    B()

def B():
    C()
    Bprime()

def Bprime():
    if token == 'int' or token == 'void':
        C()
        Bprime()

def C():
    global var, counter, funcCounter
    if token == 'int' or token == 'void':
        typeSpec = token
        E()
        checkTkn('ID')
        var = tokenList[tokenNum - 1][1]
        if token == ';' or token == '[':
            D()
        elif token == '(':
            funcVar = tokenList[tokenNum-1][1]
            if funcVar == 'main':
                funcList.append((funcVar, 0))
                output.append((str(counter), 'func', funcVar, typeSpec, '0'))
                counter += 1
                funcCounter += 1
            else:
                funcList.append((funcVar, counter))
                output.append((str(counter), 'func', funcVar, typeSpec, str(counter)))
                counter += 1
                funcCounter += 1
            F()

            output.append((str(counter), 'end', 'func', ' ', funcVar))
            counter += 1

def D():
    global counter, var
    if token == 'int' or token == 'void':
        C()

    if token == ';':
        checkTkn(';')
        output.append((str(counter), 'alloc', '4', ' ', str(var)))
        counter += 1
    elif token == '[':
        checkTkn('[')
        size = tokenList[tokenNum][1]
        size= 4 * int(size)
        output.append((str(counter), 'alloc', str(size), ' ', str(var)))
        counter += 1
        checkTkn('NUM')
        checkTkn(']')
        checkTkn(';')

def E():
    if token == 'int':
        checkTkn('int')
    elif token == 'void':
        checkTkn('void')

def F():
    if token == '(':
        checkTkn('(')
        G()
        checkTkn(')')
        J()


def G():
    if token == 'int':
        H()
    elif token == 'void':
        checkTkn('void')
        if token == 'ID':
            checkTkn('ID')
            if token == '[':
                checkTkn('[')
                checkTkn(']')
            Hprime()

def H():
    I()
    Hprime()

def Hprime():
    if token == ',':
        checkTkn(',')
        I()
        Hprime()

def I():
    global counter
    if token == 'int' or token == 'void':
        E()
        if token == 'ID':
            param = tokenList[tokenNum][1]
            checkTkn('ID')
            if token == '[':
                checkTkn('[')
                checkTkn(']')
            else:
                output.append((str(counter), 'param', ' ', ' ', param))
                counter += 1
                output.append((str(counter), 'alloc', '4', ' ', param))
                counter += 1

def J():
    checkTkn('{')
    K()
    L()
    checkTkn('}')


def K():
    Kprime()

def Kprime():
    if token == 'int' or token == 'void':
        D()
        Kprime()

def L():
    Lprime()

def Lprime():
    if token == '(' or token == 'ID' or token == ';' or token == 'if' or token == 'NUM' or token == 'return' or token == 'while' or token == '{':
        M()
        Lprime()

def M():
    if token == '(' or token == ';' or token == 'ID' or token == 'NUM':
        N()
    elif token == '{':
        J()
    elif token == 'if':
        O()
    elif token == 'while':
        P()
    elif token == 'return':
        Q()

def N():
    global counter, openR, closedR, varR
    if token == ';':
        checkTkn(';')
    elif token == '(' or token == 'ID' or token =='NUM':
        R()
        closedR = tokenNum
        checkTkn(';')
        regOut = parenth(openR, closedR, tokenList)
        output.append((str(counter), 'assign', regOut, ' ', varR))
        counter += 1

def O():
    global tokenNum, counter, bpo

    checkTkn('if')
    open = tokenNum
    bpw = counter
    checkTkn('(')
    R()
    close = tokenNum
    checkTkn(')')

    parenth(open, close, tokenList)
    M()

    bpif = counter-1
    output.append((str(counter), 'BR', ' ', ' ', 'temp'))
    counter += 1

    # WORK ON THE IF ELSE STATEMENT NEXT
    if token == 'else':

        tempbranch = (output[bpo][0], output[bpo][1], output[bpo][2], output[bpo][3], str(counter))
        output.pop(bpo)
        output.insert(bpo, tempbranch)

        checkTkn('else')
        M()

        tempbranch = (output[bpif][0], output[bpif][1], output[bpif][2], output[bpif][3], str(counter))
        output.pop(bpif)
        output.insert(bpif, tempbranch)





def P():
    global tokenNum, counter, bpo

    checkTkn('while')
    open = tokenNum
    bpw = counter
    checkTkn('(')
    R()
    close = tokenNum
    checkTkn(')')
    parenth(open, close, tokenList)
    M()
    output.append((str(counter), 'BR', ' ', ' ', str(bpw)))
    counter += 1

    tempbranch = (output[bpo][0], output[bpo][1], output[bpo][2], output[bpo][3], str(counter))
    output.pop(bpo)
    output.insert(bpo, tempbranch)



def Q():
    global counter, openZ, closedZ
    openZ = tokenNum
    checkTkn('return')
    if token == ';':

        checkTkn(';')
    elif token == '(' or token == 'ID' or token == 'NUM':
        R()
        if not parenZ:
            closedZ = tokenNum
        checkTkn(';')

        returnReg = parenth(openZ, closedZ, tokenList)
        output.append((str(counter), 'return', ' ', ' ', returnReg))
        counter += 1

def R():
    global openR, closedR, varR
    if token == 'ID':
        # the Try/Catch is implemented just in case an indexoutofbounds occurs
        #Essentially, the "Worst case scenario" when it comes to ID is that it gets sent to T()
        try:
            tempToken = tokenList[tokenNum + 1][1]
        except IndexError:
            return

        try:
            tempToken2 = tokenList[tokenNum + 4][1] # Essentially checking if there is a + after
        except IndexError:
            return

        if tempToken == '(':
            T()

        elif tempToken == '=':
            varR = tokenList[tokenNum][1]
            checkTkn('ID')
            openR = tokenNum
            checkTkn('=')
            R()

        elif tempToken == '[':
            if tempToken2 == '=':
                temp = ''
                index = 0
                while temp != ']':
                    temp = tokenList[tokenNum + index][1]
                    varR += temp
                    index +=1
                checkTkn('ID')
                checkTkn('[')
                R()
                checkTkn(']')
                openR = tokenNum
                checkTkn('=')
                R()

            else:
                T()
        else:
            T()

    elif token == '(' or token == 'NUM':
        T()


def T():
    if token == '(' or token == 'ID' or token == 'NUM':
        V()
        if token == '!=' or token == '<' or token == '<=' or token == '==' or token == '>' or token == '>=':
            U()
            V()

def U():
    if token == '!=':
        checkTkn('!=')
    elif token == '<':
        checkTkn('<')
    elif token == '<=':
        checkTkn('<=')
    elif token == '==':
        checkTkn('==')
    elif token == '>':
        checkTkn('>')
    elif token == '>=':
        checkTkn('>=')

def V():
    X()
    Vprime()

def Vprime():
    if token == '+' or token == '-':
        W()
        X()
        Vprime()

def W():
    if token == '+':
        checkTkn('+')
    elif token == '-':
        checkTkn('-')

def X():
    Z()
    Xprime()

def Xprime():
    if token == '*' or token == '/':
        Y()
        Z()
        Xprime()

def Y():
    if token == '*':
        checkTkn('*')
    elif token == '/':
        checkTkn('/')

def Z():
    global tokenNum, counter, bpo, openZ, closedZ, paranZ
    if token == '(':
        openZ = tokenNum
        checkTkn('(')
        R()
        closedZ = tokenNum
        parenZ = True
        checkTkn(')')
    elif token == 'NUM':
        checkTkn('NUM')

    elif token == 'ID':
        checkTkn('ID')
        if token == '[':
            checkTkn('[')
            R()
            checkTkn(']')
        elif token == '(':
            checkTkn('(')
            BB()
            checkTkn(')')
        closedZ = tokenNum

def BB():
    if token == 'ID' or token == '(' or token == 'NUM':
        CC()

def CC():
    R()
    CCprime()

def CCprime():
    if token == ',':
        checkTkn(',')
        R()
        CCprime()
