token = ''
tokenNum = 0
tokenList = []
scopeLvl = 0
scope = []
scope.append(dict())
mainFunc = False
arrayScope = False

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
        print('ACCEPT')
    else:
        print('REJECT')

# Implementations?
def searchScope(checkToken):
    global tokenNum, token, tokenList, scope, scopeLvl, mainFunc

    tempLvl = scopeLvl

    if tokenList[tokenNum][0] == 'NUM':
        return 'int'

    while tempLvl >= 0:
        try:
            if scope[tempLvl].get(checkToken):
                found = scope[tempLvl].get(checkToken)
                return found[0]

        except IndexError:
            pass

        tempLvl = tempLvl - 1

# Implementations?
def searchType(checkToken):
    global tokenNum, token, tokenList, scope, scopeLvl, mainFunc

    tempLvl = scopeLvl


    while tempLvl >= 0:
        try:
            if scope[tempLvl].get(checkToken):
                found = scope[tempLvl].get(checkToken)
                return found[1]

        except IndexError:
            pass

        tempLvl = tempLvl - 1


def checkSem(checkToken):
    global tokenNum, token, tokenList, scope, scopeLvl, mainFunc, arrayScope

    # As a note
    # tokenList[tokenNum][0] = Identifier
    # tokenList[tokenNum][1] = Variable

    # Starting Scope Semantics
    # To check if this is creating a new scope or not
    if checkToken == '{':
        scopeLvl = scopeLvl + 1
        scope.append(dict())

    if checkToken == '}':
        scopeLvl = scopeLvl - 1

    # End scope Semantics


    # Starting Main Semantics
    if tokenList[tokenNum][1] == 'main' and tokenList[tokenNum+1][1] !='(':
        try:
            if scope[0].get('main'):
                print('REJECT')
                exit()
        except IndexError:
            pass

    if checkToken == 'void' and tokenList[tokenNum+1][1] == 'main' and tokenList[tokenNum+4][1] != ')':
        print('REJECT')
        exit()
    elif checkToken == 'void' and tokenList[tokenNum+1][1] == 'main' and tokenList[tokenNum+4][1] == ')':
        mainFunc = True
    elif checkToken == 'int' and tokenList[tokenNum+1][1] == 'main':
        print('REJECT')
        exit()

    if tokenList[tokenNum][1] == 'return' and mainFunc == True:
        print('REJECT')
        exit()

    if tokenList[tokenNum+1][1] == '(' or tokenList[tokenNum+1][1] == '[':
        if arrayScope == True:
            print('REJECT')
            exit()

    if checkToken == '[':
        arrayScope = True
    if checkToken == ']' and arrayScope == True:
        arrayScope = False


def checkTkn(checkToken):
    global tokenNum, token, tokenList, scope, scopeLvl, mainFunc
    identifier = tokenList[tokenNum][0]
    variable = tokenList[tokenNum][1]


    if token == checkToken:

        checkSem(checkToken)

        try:
            if tokenList[tokenNum][0] == 'KW' and tokenList[tokenNum + 1][0] == 'ID':
                if tokenList[tokenNum + 2][1] == '(':
                    scope[scopeLvl].update({tokenList[tokenNum + 1][1]: [tokenList[tokenNum][1], 'FUNCTION']})
                elif tokenList[tokenNum + 2][1] == '[':
                    scope[scopeLvl].update({tokenList[tokenNum + 1][1]: [tokenList[tokenNum][1], 'ARRAY']})
                else:
                    scope[scopeLvl].update({tokenList[tokenNum+1][1] : [tokenList[tokenNum][1], 'NULL']})
        except:
            pass

        #Moves the token up 1
        tokenNum += 1
        if tokenList[tokenNum][0] == 'ID' or tokenList[tokenNum][0] == 'NUM':
            token = tokenList[tokenNum][0]
        else:
            token = tokenList[tokenNum][1]

    else:
        print('REJECT')
        exit()


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

    if token == 'int' or token == 'void':
        E()
        checkTkn('ID')

        if token == ';' or token == '[':
            D()
        elif token == '(':
            F()


def D():

    if token == 'int' or token == 'void':
        C()

    if token == ';':
        checkTkn(';')
    elif token == '[':
        checkTkn('[')
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
    else:
        print('REJECT')
        exit()


def H():

    I()
    Hprime()


def Hprime():

    if token == ',':
        checkTkn(',')
        I()
        Hprime()


def I():

    if token == 'int' or token == 'void':
        E()
        if token == 'ID':
            checkTkn('ID')
            if token == '[':
                checkTkn('[')
                checkTkn(']')


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

    if token == ';':
        checkTkn(';')
    elif token == '(' or token == 'ID' or token =='NUM':
        R()
        checkTkn(';')


def O():

    checkTkn('if')
    checkTkn('(')
    R()
    checkTkn(')')
    M()
    if token == 'else':
        checkTkn('else')
        M()


def P():

    checkTkn('while')
    checkTkn('(')
    R()
    checkTkn(')')
    M()


def Q():

    checkTkn('return')
    if token == ';':
        checkTkn(';')
    elif token == '(' or token == 'ID' or token == 'NUM':
        R()
        checkTkn(';')


def R():

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
            checkTkn('ID')
            checkTkn('=')
            R()

        elif tempToken == '[':
            if tempToken2 == '=':
                checkTkn('ID')
                checkTkn('[')
                R()
                checkTkn(']')
                checkTkn('=')
                R()
            else:
                T()
        else:
            T()

    elif token == '(' or token == 'NUM':
        T()

    else:
        #theres an empty where it shouldn't appear
        print('REJECT')
        exit()


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

    if token == '(':
        checkTkn('(')
        R()
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

