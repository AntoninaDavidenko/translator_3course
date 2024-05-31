from lexer_pico import lex
from lexer_pico import tableOfSymb, tableOfConst, FSuccess

lex()
print('-'*30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('-'*30)


tempLexName = ''
# номер рядка таблиці розбору/лексем/символів ПРОГРАМИ tableOfSymb
numRow=1
# кількість записів у таблиці розбору
len_tableOfSymb = len(tableOfSymb)
print(('len_tableOfSymb',len_tableOfSymb))

tableOfVar = {}
tableOfLabel = {}
postfixCode = []
toView = False

forVar = ''
forToValue = 0



def parseProgram():
    try:
        parseToken('program', 'keyword', '')
        parseProgName()
        parseToken('var', 'keyword', '')
        parseDeclarList()

        parseToken('start', 'keyword', '')
        parseStatementList()
        parseToken('stop', 'keyword', '')
        print('Parser: Синтаксичний аналiз завершився успiшно')

        return (True,'codeGeneration')
    except SystemExit as e:
        # Повiдомити про факт виявлення помилки
        print('Parser: Аварiйне завершення програми з кодом {0}'.format(e))
        return (False,'codeGeneration')


# Функцiя перевiряє, чи у поточному рядку таблицi розбору
# зустрiлась вказана лексема lexeme з токеном token
# параметр indent - вiдступ при виведеннi у консоль
def parseToken(lexeme, token, indent):
    # доступ до поточного рядка таблицi розбору
    global numRow
    # якщо всi записи таблицi розбору прочитанi,
    # а парсер ще не знайшов якусь лексему
    if numRow > len_tableOfSymb:
        failParse('неочiкуваний кiнець програми', (lexeme, token, numRow))
        # прочитати з таблицi розбору
        # номер рядка програми, лексему та її токен
    numLine, lex, tok = getSymb()
    # тепер поточним буде наступний рядок таблицi розбору
    numRow += 1
    # чи збiгаються лексема та токен таблицi розбору (lex, tok)
    # з очiкуваними (lexeme,token)
    if (lex, tok) == (lexeme, token):
        # вивести у консоль номер рядка програми та лексему i токен
        print(indent + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lexeme, token)))
        return True
    else:
        # згенерувати помилку та iнформацiю про те, що
        # лексема та токен таблицi розбору (lex,tok) вiдрiзняються вiд
        # очiкуваних (lexeme,token)
        failParse('невiдповiднiсть токенiв', (numLine, lex, tok, lexeme, token))
        return False


def getSymb():
    # таблиця розбору реалiзована у формi словника (dictionary)
    # tableOfSymb = {numRow: (numLine, lexeme, token, indexOfVarOrConst)
    numLine, lexeme, token, _ = tableOfSymb[numRow]
    return numLine, lexeme, token


# Обробити помилки:
# 1) ’неочiкуваний кiнець програми’
# 2) ’невiдповiднiсть токенiв’
def failParse(str, tuple):
    if str == 'неочікуваний кінець програми':
        (lexeme, token, numRow) = tuple
        print(
            'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format(
                (lexeme, token), numRow))
        exit(1001)
    if str == 'getSymb(): неочікуваний кінець програми':
        numRow = tuple
        print(
            'Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}'.format(
                numRow, tableOfSymb[numRow - 1]))
        exit(1002)
    elif str == 'невідповідність токенів':
        (numLine, lexeme, token, lex, tok) = tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - ({3},{4}).'.format(
            numLine, lexeme, token, lex, tok))
        exit(1)
    elif str == 'невідповідність інструкцій':
        (numLine, lex, tok, expected) = tuple
        print(
            'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine, lex,
                                                                                                           tok,
                                                                                                           expected))
        exit(2)
    elif str == 'невідповідність у Expression.Factor':
        (numLine, lex, tok, expected) = tuple
        print(
            'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine, lex,
                                                                                                           tok,
                                                                                                           expected))
        exit(3)
    elif str == 'mismatch in BoolExpr':
        (numLine, lex, tok, expected) = tuple
        print(
            'Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine, lex,
                                                                                                           tok,
                                                                                                           expected))
        exit(4)
    elif str == 'повторне оголошення змiнної':
        (numLine, lex, tok) = tuple
        print(
            'Parser ERROR: \n\t В рядку {0} повторне оголошення змінної ({1},{2}). \n\t'.format(numLine, lex,
                                                                                                           tok))
        exit(5)
    elif str == 'неоголошена змінна':
        (numLine, lex, tok) = tuple
        print(
            'Parser ERROR: \n\t В рядку {0} неоголошена змінна ({1},{2}). \n\t'.format(numLine, lex,
                                                                                                           tok))
        exit(6)
    elif str == 'невідомий тип':
        (numLine, lex, tok) = tuple
        print(
            'Parser ERROR: \n\t В рядку {0} невідомий тип змінної ({1},{2}). \n\t'.format(numLine, lex,
                                                                                                           tok))
        exit(7)
    elif str == 'ділення на нуль':
        (numLine, lex, tok) = tuple
        print(
            'Parser ERROR: \n\t В рядку {0} ділення на нуль ({1},{2}). \n\t'.format(numLine, lex,
                                                                                                           tok))
        exit(8)
    elif str == 'невідповідність типів':
        (numLine, lex, tok) = tuple
        print(
            'Parser ERROR: \n\t В рядку {0} невідповідність типів ({1},{2}). \n\t'.format(numLine, lex,
                                                                                                           tok))
        exit(9)



def parseProgName():
    print('parseProgName():')
    return parseIdent()


def parseIdent(val = False):
    global numRow
    print('\t'*3 + 'parseIdent():')
    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()
    # якщо токен - ідентифікатор
    if tok == 'ident':
        numRow += 1
        print('\t'*4 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
        if val:
            postfixCodeGen('rval', (lex, tok))
        return True
    else:
        failParse('невідповідність інструкцій', (numLine, lex, tok, 'ident'))
        return False


def parseDeclarList():
    global numRow
    print('\t' * 3 + 'parseDeclarList():')
    numLine, lex, tok = getSymb()
    while (lex, tok) not in [('start','keyword')]:
        if tok == 'ident':
            parseIdent()
            parseToken('::', 'decl_op', '\t' * 4)
            parseType(numLine, lex, tok)
            parseToken(';', 'punct_op', '\t' * 4)
            numLine, lex, tok = getSymb()
        else:
            failParse('очiкувався iдентифiкатор', (numLine, lex, tok))
    return True


def parseType(numLine, lex, tok):
    global numRow
    print('\t' * 4 + 'parseType():')
    numLineT, lexT, tokT = getSymb()
    numRow += 1
    if lexT in ('integer', 'real', 'boolval') and tokT == 'keyword':
        print('\t' * 5 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
        procTableOfVar(numLine, lex, lexT, 'undefined')
        return True
    else:
        return failParse('невідомий тип', (numLine, lex, tok))



def procTableOfVar(numLine,lexeme,type,value):
    indx=tableOfVar.get(lexeme)
    if indx is None:
        indx=len(tableOfVar)+1
        tableOfVar[lexeme]=(indx,type,value)
    else: failParse('повторне оголошення змiнної',(numLine, lexeme,type,value))


def getTypeVar(id):
    try:
        return tableOfVar[id][1]
    except KeyError:
        return 'undeclared_variable'


# Функція для розбору за правилом для StatementList
# StatementList = Statement  { Statement }
# викликає функцію parseStatement() доти,
# доки parseStatement() повертає True
def parseStatementList():
        print('\t parseStatementList():')
        while parseStatement():
                pass
        return True


def parseStatement(isFor = False):
    print('\t\t parseStatement():')
    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()
    # якщо токен - ідентифікатор
    # обробити інструкцію присвоювання
    if tok == 'ident':
        if lex in tableOfVar:
            parseAssign(isFor)
            return True
        else: failParse('неоголошена змінна',(numLine, lex, tok))

    elif lex == 'read' and tok == 'keyword':
        parseRead()
        return True

    elif lex == 'write' and tok == 'keyword':
        parseWrite()
        return True

    # якщо лексема - ключове слово 'if'
    # обробити інструкцію розгалудження
    elif (lex, tok) == ('if','keyword'):
        parseIf()
        return True

    elif (lex, tok) == ('for','keyword'):
        parseFor()
        return True

    elif (lex, tok) == ('end', 'keyword'):
        return False

    # тут - ознака того, що всі інструкції були коректно
    # розібрані і була знайдена остання лексема програми.
    # тому parseStatement() має завершити роботу
    elif (lex, tok) == ('stop','keyword'):
            return False

    else:
        # жодна з інструкцій не відповідає
        # поточній лексемі у таблиці розбору,
        failParse('невідповідність інструкцій',(numLine,lex,tok,'ident або if'))
        return False


def parseAssign(isFor = False):
    # номер запису таблиці розбору
    global numRow, forVar
    #print('\t'*4+'parseAssign():')

    # взяти поточну лексему
    numLine, lex, tok = getSymb()
    lType = getTypeVar(lex)
    # ПРОВЕРКА НА ФОР
    # numRow -= 1
    # numLine2, lex2, tok2 = getSymb()
    # if lex2 == 'for':
    #     postfixCodeGen('for', (lex, 'for'))
    # else:
    postfixCodeGen('lval', (lex, tok))

    # numRow += 1
    #postfixCodeGen('lval', (lex, tok))
    if toView: configToPrint(lex, numRow)

    if isFor:
        forVar = lex
        typeOfVar = tableOfVar[lex][1]
        if typeOfVar == 'real':
            print('Тип перемінної в циклі for має бути integer!')
            return failParse('невідповідність типів', (numLine, typeOfVar, 'integer'))

    # встановити номер нової поточної лексеми
    numRow += 1

    #print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    # якщо була прочитана лексема - ':='
    if parseToken('==','assign_op','\t\t\t\t\t'):
        # перевірка на assigned
        numLine1, lex1, tok1 = getSymb()
        numRow -= 1
        if lex1 is not None:
            tableOfVar[lex] = (tableOfVar[lex][0], tableOfVar[lex][1], 'assigned')
            print(tableOfVar)
            # розібрати арифметичний вираз
        numRow += 1
        rType = parseExpression()
        # if lType == rType:
        postfixCodeGen('==', ('==', 'assign_op'))
        # else:
        #     failParse('невiдповiднiсть типiв', (numRow, lex, lType, rType))
        #     return 'type_error'
        if toView: configToPrint('==', numRow)
    return 'void'
        # numLine1, lex1, tok1 = getSymb()
        # numRow -= 1
        # #numLine2, lex2, tok2 = getSymb()
        # if lex1 is not None:
        #     tableOfVar[lex] = (tableOfVar[lex][0], tableOfVar[lex][1], 'assigned')
        #     print(tableOfVar)
        #     # розібрати арифметичний вираз
        # numRow += 1
        # resultType = parseExpression()
        # if resultType != tableOfVar[lex][1]:
        #     return failParse('невідповідність типів', (numLine, lex, tok))
        # return True
    # else: return False


def getTypeOp(lType,op,rType):
    if lType == 'ident':
        lType = tableOfVar[tempLexName][1]

    if rType == 'ident':
        rType = tableOfVar[tempLexName][1]


    # типи збiгаються?
    typesAreSame = lType == rType
    # типи арифметичнi?
    typesArithm = lType in ('integer','real') and rType in ('integer','real')
    if typesAreSame and lType == 'integer' and typesArithm and op in '+-*':
        typeRes = 'integer'
    elif typesAreSame and lType == 'real' and typesArithm and op in '+-*':
        typeRes = 'real'
    elif typesAreSame is not True and typesArithm and op in '+-*':
        typeRes = 'real'
    elif typesArithm and op in '!':
        typeRes = 'real'
    elif typesArithm and op in '/':
        typeRes = 'real'
    elif op in ('<','<=','>','>=','=','=!'):
        # на случай если нужно будет менять тип при подсчете
        #if not typesAreSame:
        #    lType = 'real'
        #    rType = 'real'
        typeRes = 'boolval'
    else: typeRes = 'type_error'
    return typeRes


def parseExpression():
    global numRow, postfixCode
    #print('\t' * 5 + 'parseExpression():')
    numLine, lex, tok = getSymb()

    # унарний мінус
    if (lex == '-'):
        numRow += 1
        lType = parseTerm()
        postfixCodeGen(lex, ('-', '@'))  # lex - унарний оператор '+' чи '-'
        if toView: configToPrint(lex, numRow)
        # print('\t'*4 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
    else:
        lType = parseTerm()
        #numLine1, lex, tok = numLine, lex, tok
        # postfixCodeGen(lex, (lex, "@"))
        # if toView: configToPrint(lex, numRow)
    #     print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))

    # lType = parseTerm()
    resType = lType
    F = True
    # продовжувати розбирати Доданки (Term)
    # розділені лексемами '+' або '-'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('add_op'):
            numRow += 1
            #print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            rType = parseTerm()
            #if lType == rType:
            resType = lType
            postfixCodeGen(lex, (lex, tok))
            if toView: configToPrint(lex, numRow)
            #else:
            #    resType = 'type_error'
            #    failParse('невiдповiднiсть типiв', (numRow, lType, lex, rType))
            # resType = getTypeOp(lType, lex, rType)
            # print(resType)
            #if resType != 'type_error':
            #    ltype = resType
            #else:
            #    tpl = (numLine, lType, lex, rType)  # для повiдомлення про помилку
            #    failSem(resType, tpl)
        else:
            F = False
    return resType


def parseTerm():
    global numRow, postfixCode
    #print('\t' * 6 + 'parseTerm():')
    lType = parseFactor()
    resType = lType
    F = True
    # продовжувати розбирати Множники (Factor)
    # розділені лексемами '*' або '/'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('mult_op'):
            numRow += 1

            # numLine1, lex1, tok1 = getSymb()
            # if lex == '/' and lex1 == '0':
            #     failParse('ділення на нуль', (numLine, lex, tok))
            # print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            rType = parseFactor()
            # if lType == rType:
            resType = lType
            postfixCodeGen(lex, (lex, tok))
            if toView: configToPrint(lex, numRow)
            # else:
            #     resType = 'type_error'
            #     failParse('невiдповiднiсть типiв', (numRow, lType, lex, rType))
            # resType = getTypeOp(lType, lex, rType)
            # print(resType)
        elif tok in ('pow_op'):
            numRow += 1
            #print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            rType = parsePower()
            # if lType == rType:
            resType = lType
            postfixCodeGen(lex, (lex, tok))
            if toView: configToPrint(lex, numRow)
            # else:
            #     resType = 'type_error'
            #     failParse('невiдповiднiсть типiв', (numRow, lType, lex, rType))
            # resType = getTypeOp(lType, lex, rType)
            # print(resType)
        else:
            F = False
    return resType


def parsePower():
    global numRow, postfixCode
    #print('\t' * 7 + 'parsePower():')
    lType = parseFactor()
    resType = lType
    F = True
    while F:
        numLine, lex, tok = getSymb()
        if lex == '!':
            numRow += 1
            #print('\t' * 7 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            rType = parsePower()
            # if lType == rType:
            resType = lType
            postfixCodeGen('pow_op', (lex, tok))
            if toView: configToPrint(lex, numRow)
            # else:
            #     resType = 'type_error'
            #     failParse('невiдповiднiсть типiв', (numRow, lType, lex, rType))
            # resType = getTypeOp(lType, lex, rType)
            # print(resType)
        else:
            F = False
    return resType


def parseFactor(isFor = False):
    global numRow, tempLexName, postfixCode, forToValue
    #print('\t' * 7 + 'parseFactor():')
    numLine, lex, tok = getSymb()
    #print('\t' * 7 + 'parseFactor():=============рядок: {0}\t (lex, tok):{1}'.format(numLine, (lex, tok)))
    numRow +=1
    if tok == 'ident':
        typeRes = getTypeVar(lex)
        # indexVar = getIndexVar(lex)
        postfixCodeGen('rval', (lex, 'rval'))
        if toView: configToPrint(lex, numRow)
    elif tok in ('integer', 'real'):
        if isFor:
            forToValue = lex
            if tok == 'real':
                print("Значення константи після ключового слова 'to' має бути типу integer!")
                return failParse('невідповідність типів', (numLine, tok, 'integer'))
        typeRes = tok
        postfixCodeGen('const', (lex, tok))
        if toView: configToPrint(lex, numRow)
    elif tok == 'boolval':
        typeRes = tok
        postfixCodeGen('boolval', (lex, tok))
        if toView: configToPrint(lex, numRow)
    elif lex == '(':
        typeRes = parseExpression()
        parseToken(')', 'par_op', '\t' * 7)
    elif lex == '-':
        numRow += 1
        resType = parseFactor()
        numRow -= 1
    # перша і друга альтернативи для Factor
    # якщо лексема - це константа або ідентифікатор
    # if tok in ('integer', 'real', 'boolval', 'ident'):
    #     if tok == 'ident':
    #         tempLexName = lex
    #     numRow += 1
    #     print('\t' * 7 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
    #     resType = tok
    # третя альтернатива для Factor
    # якщо лексема - це відкриваюча дужка
    # elif lex == '(':
    #     numRow += 1
    #     resType = parseExpression()
    #     parseToken(')', 'brackets_op', '\t' * 7)
    #     print('\t' * 7 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
    else:
        failParse('невідповідність у Expression.Factor',
                  (numLine, lex, tok, 'rel_op, integer, real, ident або \'(\' Expression \')\''))
    return typeRes


def parseRead():
    global numRow
    print('\t' * 3 + 'parseRead():')
    _, lex, tok = getSymb()
    if lex == 'read' and tok == 'keyword':
        numRow += 1
        parseToken('(', 'brackets_op', '\t' * 5)
        #parseIdent()
        if parseIdent(True):
            numRow -= 1
            numLine1, lex1, tok1 = getSymb()
            numRow += 1
            tableOfVar[lex1] = (tableOfVar[lex1][0], tableOfVar[lex1][1], 'assigned')
        parseToken(')', 'brackets_op', '\t' * 5)
        postfixCodeGen('in', ('IN', 'inp_op'))
        return True
    else:
        return False


def parseWrite():
    global numRow
    print('\t' * 3 + 'parseWrite():')
    _, lex, tok = getSymb()
    if lex == 'write' and tok == 'keyword':
        numRow += 1
        parseToken('(', 'brackets_op', '\t' * 5)
        parseIdent(True)
        parseToken(')', 'brackets_op', '\t' * 5)
        postfixCodeGen('out', ('OUT', 'out_op'))
        return True
    else:
        return False


def parseIf():
    global numRow
    print('\t' * 3 + 'parseIf():')
    _, lex, tok = getSymb()
    if lex=='if' and tok=='keyword':
        numRow += 1

        parseBoolExpr()
        parseToken('then','keyword','\t'*5)
        m1 = createLabel()
        postfixCodeGen('label', m1)
        postfixCodeGen('JF', ('JF', 'jf'))

        parseStatement()
        parseToken('fi','keyword','\t'*5)
        setValLabel(m1)
        postfixCodeGen('label', m1)
        postfixCodeGen('colon', (':', 'colon'))

        return True
    else: return False


def createLabel():
    global tableOfLabel
    nmb = len(tableOfLabel)+1
    lexeme = "m"+str(nmb)
    val = tableOfLabel.get(lexeme)
    if val is None:
        tableOfLabel[lexeme] = 'val_undef'
        tok = 'label' # # #
    else:
        tok = 'Конфлiкт мiток'
        print(tok)
        exit(1003)
    return lexeme, tok


def setValLabel(lbl):
    global tableOfLabel
    lex,_tok = lbl
    tableOfLabel[lex] = len(postfixCode)
    return True


def parseFor():
    global numRow, forVar, forToValue
    # print('\t'*3 + 'parseFor:')
    _, lex, tok = getSymb()

    if lex == 'for' and tok == 'keyword':
        numRow += 1
        start = createLabel()
        action = createLabel()
        increment = createLabel()
        leave = createLabel()

        parseStatement(True)

        setValLabel(start)
        postfixCodeGen('label', start)
        postfixCodeGen('colon', (':', 'colon'))

        postfixCodeGen('rval', (forVar, 'r-val'))
        parseToken('to', 'keyword', '\t' * 4)
        parseFactor(True)

        postfixCodeGen('to', ('TO', 'to'))

        postfixCodeGen('label', leave)
        postfixCodeGen('JF', ('JF', 'jf'))
        postfixCodeGen('label', action)
        postfixCodeGen('JUMP', ('JUMP', 'jump'))

        setValLabel(increment)
        postfixCodeGen('label', increment)
        postfixCodeGen('colon', (':', 'colon'))

        postfixCodeGen('lval', (forVar, 'l-val'))
        postfixCodeGen('rval', (forVar, 'r-val'))
        postfixCodeGen('integer', ('1', 'integer'))
        postfixCodeGen('operator', ('OP', 'operator'))
        postfixCodeGen('==', ('==', 'assign_op'))

        postfixCodeGen('label', start)
        postfixCodeGen('JUMP', ('JUMP', 'jump'))

        parseToken('do', 'keyword', '\t' * 4)

        setValLabel(action)
        postfixCodeGen('label', action)
        postfixCodeGen('colon', (':', 'colon'))
        parseStatementList()

        postfixCodeGen('label', increment)
        postfixCodeGen('JUMP', ('JUMP', 'jump'))

        parseToken('end', 'keyword', '\t' * 4)

        setValLabel(leave)
        postfixCodeGen('label', leave)
        postfixCodeGen('colon', (':', 'colon'))
        return True
    else:
        return False
    # global numRow
    # print('\t' * 3 + 'parseFor():')
    # _, lex, tok = getSymb()
    # if lex == 'for' and tok == 'keyword':
    #     numRow += 1
    #     parseStatement()
    #     start = createLabel()
    #     postfixCodeGen('label', start)
    #     postfixCodeGen('colon', (':', 'colon'))
    #     parseToken('to', 'keyword', '\t' * 5)
    #     parseExpression()
    #     parseToken('do', 'keyword', '\t' * 5)
    #     parseStatementList()
    #     parseToken('end', 'keyword', '\t' * 5)
    #     return True
    #else: return False


def parseBoolExpr():
    global numRow
    lType = parseExpression()
    numLine, lex, tok = getSymb()
    if tok == 'rel_op':
            numRow += 1
            print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    else:
        failParse('mismatch in BoolExpr',(numLine,lex,tok,'rel_op'))
    rType = parseExpression()
    resType = getTypeOp(lType, lex, rType)
    if resType != 'boolval':
        failParse('mismatch in BoolExpr',(numLine,lex,tok,'boolval'))
    if tok in ('rel_op'):
        postfixCodeGen(lex,(lex, tok))
    print(resType)
    return True


def postfixCodeGen(case, toTran):
    if case == 'lval':
        lex, tok = toTran
        postfixCode.append((lex, 'l-val'))
    elif case == 'rval':
        lex, tok = toTran
        postfixCode.append((lex, 'r-val'))
    else:
        lex, tok = toTran
        postfixCode.append((lex, tok))


def configToPrint(lex,numRow):
    stage = '\nКрок трансляцiї\n'
    stage += 'лексема: \'{0}\'\n'
    stage += 'postfixCode = {3}\n'
    print(stage.format(lex,numRow,str(tableOfSymb[numRow]),str(postfixCode)))


def serv():
    print("\n Таблиця ідентифікаторів")
    s1 = '{0:<10s} {1:<15s} {2:<15s} {3:<10s} '
    print(s1.format("Ident", "Type", "Value", "Index"))
    s2 = '{0:<10s} {2:<15s} {3:<15s} {1:<10d} '
    for id in tableOfVar:
        index, type, val = tableOfVar[id]
        print(s2.format(id, index, type, str(val)))
    print('\t\t\t\t')
    print("\n Таблиця міток")
    s3 = '{0:<10s} {1:<10s} '
    print(s3.format("Label", "Value"))
    for label in tableOfLabel:
        value = tableOfLabel[label]
        print(s3.format(label, str(value)))
    print('\t\t\t\t')
    print('Код програми у постфiкснiй формi (ПОЛIЗ):')
    print('\t\t\t\t')

    s4 = '{0:<10s} {1:<15s}'
    print(s4.format("№","postfixCode"))
    for index, item in enumerate(postfixCode):
        print(f"{index:<10d} {item}")


def savePostfixCode(fileName):
    print(f'savePostfixCode({fileName})')

    f = open(fileName + '.postfix', 'w')
    print('.target: Postfix Machine', file=f)
    print('.version: 0.2', file=f)
    print('\n', file=f)
    # перемінні
    print(".vars(", file=f)
    for key, value in tableOfVar.items():
        type = value[1]
        print(f'    {key:<10} {type}', file=f)
    print(")", file=f)
    # мітки
    print('\n', file=f)
    print(".labels(", file=f)
    for key, value in tableOfLabel.items():
        print(f'    {key:<10} {value}', file=f)
    print(")", file=f)

    print('\n', file=f)
    # константи
    print(".constants(", file=f)
    for key, value in tableOfConst.items():
        print(f'    {key:<10} {value}', file=f)
    print(")", file=f)

    print('\n', file=f)
    # код
    print(".code(", file=f)
    for index, item in postfixCode:
        print(f'    {index:<10} {item}', file=f)
    print(")", file=f)

    f.close()


# parseProgram()
# print(tableOfVar)
# serv()
# savePostfixCode('dddd')
def compileToPostfix():
  global len_tableOfSymb, FSuccess
  print('compileToPostfix: lexer Start Up\n')
  print('compileToPostfix: lexer-FSuccess ={0}'.format(FSuccess))

  # чи був успiшним лексичний розбiр
  if (True,'Lexer') == FSuccess:
    print('-'*55)
    print('compileToPostfix: Start Up compiler = parser + codeGenerator\n')
    FSuccess = (False,'codeGeneration')
    FSuccess = parseProgram()

    if FSuccess == (True,'codeGeneration'):
      serv()
      savePostfixCode('test2')
  return FSuccess


compileToPostfix()