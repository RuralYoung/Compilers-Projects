token = ''
tokenNum = 0
tokenList = []


def main(inputList):
    global tokenNum, token, tokenList

    #checks to see if the input is empty
    try:
        token = inputList[tokenNum]
        tokenList = inputList
    except IndexError:
        print('REJECT')
        exit()

    #Adds the last Accept
    tokenList.append('$')

    #the beginning of the program (Sends it over to A: Program)
    A()

    if token == '$':
        print('ACCEPT')
    else:
        print('REJECT')


def check(checkToken):
    global tokenNum, token, tokenList
    if token == checkToken:
        #Checks the next token in the list
        tokenNum += 1
        token = tokenList[tokenNum]
        print("Updated: "+ token)
    else:
        print('REJECT')
        exit()


def A():
    print("A: Program")
    B()
    print("End A: Program")

def B():
    print("B: Declaration List")
    C()
    Bprime()
    print("End B: Declaration List")

def Bprime():
    print("Bprime: Declaration List Prime")
    if token == 'int' or token == 'void':
        C()
        Bprime()
    print("End Bprime: Declaration List Prime")

def C():
    print("C: Declaration")
    if token == 'int' or token == 'void':
        E()
        check('ID')
        if token == ';' or token == '[':
            D()
        elif token == '(':
            F()
    print("End C: Declaration")

def D():
    print("D: Var-Declaration")
    if token == 'int' or token == 'void':
        C()

    if token == ';':
        check(';')
    elif token == '[':
        check('[')
        check('NUM')
        check(']')
        check(';')
    print("End D: Var-Declaration")

def E():
    print("E: Type-Specifier")
    if token == 'int':
        check('int')
    elif token == 'void':
        check('void')
    print("End E: Type-Specifier")

def F():
    print("F: Fun-Declaration")
    if token == '(':
        check('(')
        G()
        check(')')
        J()
    print("End F: Fun-Declaration")

def G():
    print("G: Params")
    if token == 'int':
        H()
    elif token == 'void':
        check('void')
        if token == 'ID':
            check('ID')
            if token == '[':
                check('[')
                check(']')
            Hprime()
    else:
        print('REJECT')
        exit()
    print("End G: Params")

def H():
    print("H: Param-list")
    I()
    Hprime()
    print("End H: Param-list")

def Hprime():
    print("Hprime: Param-list Prime")
    if token == ',':
        check(',')
        I()
        Hprime()
    print("End Hprime: Param-list Prime")

def I():
    print("I: Param")
    if token == 'int' or token == 'void':
        E()
        if token == 'ID':
            check('ID')
            if token == '[':
                check('[')
                check(']')
    print("End I: Param")

def J():
    print("J: Compound STMT")
    check('{')
    K()
    L()
    check('}')
    print("End J: Compound STMT")

def K():
    print("K: Local-Declarations")
    Kprime()
    print("End K: Local-Declarations")

def Kprime():
    print("Kprime: Local-Declarations Prime")
    if token == 'int' or token == 'void':
        D()
        Kprime()
    print("End Kprime: Local-Declarations Prime")

def L():
    print("L: Statement-List")
    Lprime()
    print("End L: Statement-List")

def Lprime():
    print("Lprime: Statement-List Prime")
    if token == '(' or token == 'ID' or token == ';' or token == 'if' or token == 'NUM' or token == 'return' or token == 'while' or token == '{':
        M()
        Lprime()
    print("End Lprime: Statement-List Prime")

def M():
    print("M: Statement")
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
    print("End M: Statement")

def N():
    print("N: Expression-Stmt")
    if token == ';':
        check(';')
    elif token == '(' or token == 'ID' or token =='NUM':
        R()
        check(';')
    print("End N: Expression-Stmt")

def O():
    print("O: Selection-Stmt")
    check('if')
    check('(')
    R()
    check(')')
    M()
    if token == 'else':
        check('else')
        M()
    print("End O: Selection-Stmt")

def P():
    print("P: Iteration-Stmt")
    check('while')
    check('(')
    R()
    check(')')
    M()
    print("End P: Iteration-Stmt")

def Q():
    print("Q: Return-Stmt")
    check('return')
    if token == ';':
        check(';')
    elif token == '(' or token == 'ID' or token == 'NUM':
        R()
        check(';')
    print("End Q: Return-Stmt")

def R():
    print("R: Expression")
    if token == 'ID':
        # the Try/Catch is implemented just in case an indexoutofbounds occurs
        #Essentially, the "Worst case scenario" when it comes to ID is that it gets sent to T()
        try:
            tempToken = tokenList[tokenNum + 1]
        except IndexError:
            return

        try:
            tempToken2 = tokenList[tokenNum + 4] # Essentially checking if there is a + after
        except IndexError:
            return

        if tempToken == '(':
            T()

        elif tempToken == '=':
            check('ID')
            check('=')
            R()

        elif tempToken == '[':
            if tempToken2 == '=':
                check('ID')
                check('[')
                R()
                check(']')
                check('=')
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
    print("End R: Expression")

#I included this for posterity but commented it out as it was no longer necessary
#def S():
#    S: Var
#
#    check('ID')
#    check('[')
#    R()
#    check(']')


def T():
    print("T: Simple-Expression")
    if token == '(' or token == 'ID' or token == 'NUM':
        V()
        if token == '!=' or token == '<' or token == '<=' or token == '==' or token == '>' or token == '>=':
            U()
            V()
    print("End T: Simple-Expression")

def U():
    print("U: Relop")
    if token == '!=':
        check('!=')
    elif token == '<':
        check('<')
    elif token == '<=':
        check('<=')
    elif token == '==':
        check('==')
    elif token == '>':
        check('>')
    elif token == '>=':
        check('>=')
    print("End U: Relop")

def V():
    print("V: Additive-Expression")
    X()
    Vprime()
    print("End V: Additive-Expression")

def Vprime():
    print("Vprime: Additive-Expression Prime")
    if token == '+' or token == '-':
        W()
        X()
        Vprime()
    print("End Vprime: Additive-Expression Prime")

def W():
    print("W: Addop")
    if token == '+':
        check('+')
    elif token == '-':
        check('-')
    print("End W: Addop")

def X():
    print("X: Term")
    Z()
    Xprime()
    print("End X: Term")

def Xprime():
    print("Xprime: Term Prime")
    if token == '*' or token == '/':
        Y()
        Z()
        Xprime()
    print("End Xprime: Term Prime")

def Y():
    print("Y: Mulop")
    if token == '*':
        check('*')
    elif token == '/':
        check('/')
    print("End Y: Mulop")

def Z():
    print("Z: Factor")
    if token == '(':
        check('(')
        R()
        check(')')
    elif token == 'NUM':
        check('NUM')
    elif token == 'ID':
        check('ID')
        if token == '[':
            check('[')
            R()
            check(']')
        elif token == '(':
            check('(')
            BB()
            check(')')
    print("End Z: Factor")

#Same with this, I left this as a "This was an original function"
#def AA():
#    AA: Call

#    check('(')
#    BB()
#    check(')')


def BB():
    print("BB: Args")
    if token == 'ID' or token == '(' or token == 'NUM':
        CC()
    print("End BB: Args")

def CC():
    print("CC: Arg-List")
    R()
    CCprime()
    print("End CC: Arg-List")

def CCprime():
    print("CCprime: Arg-List prime")
    if token == ',':
        check(',')
        R()
        CCprime()
    print("End CCprime: Arg-List prime")