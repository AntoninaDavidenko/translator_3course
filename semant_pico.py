from lexer_pico import lex
from lexer_pico import tableOfSymb

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

        return True
    except SystemExit as e:
        # Повiдомити про факт виявлення помилки
        print('Parser: Аварiйне завершення програми з кодом {0}'.format(e))


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


def parseIdent():
    global numRow
    print('\t'*3 + 'parseIdent():')
    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()
    # якщо токен - ідентифікатор
    if tok == 'ident':
        numRow += 1
        print('\t'*4 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
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
    else: failParse('повторне оголошення змiнної',(numLine, lexeme,type))


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


def parseStatement():
    print('\t\t parseStatement():')
    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()
    # якщо токен - ідентифікатор
    # обробити інструкцію присвоювання
    if tok == 'ident':
        if lex in tableOfVar:
            parseAssign()
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


def parseAssign():
    # номер запису таблиці розбору
    global numRow
    print('\t'*4+'parseAssign():')

    # взяти поточну лексему
    numLine, lex, tok = getSymb()

    # встановити номер нової поточної лексеми
    numRow += 1

    print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    # якщо була прочитана лексема - ':='
    if parseToken('==','assign_op','\t\t\t\t\t'):

        numLine1, lex1, tok1 = getSymb()
        numRow -= 1
        #numLine2, lex2, tok2 = getSymb()
        if lex1 is not None:
            tableOfVar[lex] = (tableOfVar[lex][0], tableOfVar[lex][1], 'assigned')
            print(tableOfVar)
            # розібрати арифметичний вираз
        numRow += 1
        resultType = parseExpression()
        if resultType != tableOfVar[lex][1]:
            return failParse('невідповідність типів', (numLine, lex, tok))
        return True
    else: return False


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
    global numRow
    print('\t' * 5 + 'parseExpression():')
    numLine, lex, tok = getSymb()

    # унарний мінус
    if lex == '-':
        numRow += 1
        print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))

    lType = parseTerm()
    resType = lType
    F = True
    # продовжувати розбирати Доданки (Term)
    # розділені лексемами '+' або '-'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('add_op'):
            numRow += 1
            print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            rType = parseTerm()
            resType = getTypeOp(lType, lex, rType)
            print(resType)
            #if resType != 'type_error':
            #    ltype = resType
            #else:
            #    tpl = (numLine, lType, lex, rType)  # для повiдомлення про помилку
            #    failSem(resType, tpl)
        else:
            F = False
    return resType


def parseTerm():
    global numRow
    print('\t' * 6 + 'parseTerm():')
    lType = parseFactor()
    resType = lType
    F = True
    # продовжувати розбирати Множники (Factor)
    # розділені лексемами '*' або '/'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('mult_op'):
            numRow += 1

            numLine1, lex1, tok1 = getSymb()
            if lex == '/' and lex1 == '0':
                failParse('ділення на нуль', (numLine, lex, tok))
            print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            rType = parseFactor()
            resType = getTypeOp(lType, lex, rType)
            print(resType)
        elif tok in ('pow_op'):
            numRow += 1
            print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            rType = parsePower()
            resType = getTypeOp(lType, lex, rType)
            print(resType)
        else:
            F = False
    return resType


def parsePower():
    global numRow
    print('\t' * 7 + 'parsePower():')
    lType = parseFactor()
    resType = lType
    F = True
    while F:
        numLine, lex, tok = getSymb()
        if tok == '!':
            numRow += 1
            print('\t' * 7 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            rType = parsePower()
            resType = getTypeOp(lType, lex, rType)
            print(resType)
        else:
            F = False
    return resType


def parseFactor():
    global numRow, tempLexName
    print('\t' * 7 + 'parseFactor():')
    numLine, lex, tok = getSymb()
    print('\t' * 7 + 'parseFactor():=============рядок: {0}\t (lex, tok):{1}'.format(numLine, (lex, tok)))

    # перша і друга альтернативи для Factor
    # якщо лексема - це константа або ідентифікатор
    if tok in ('integer', 'real', 'boolval', 'ident'):
        if tok == 'ident':
            tempLexName = lex
        numRow += 1
        print('\t' * 7 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
        resType = tok
    # третя альтернатива для Factor
    # якщо лексема - це відкриваюча дужка
    elif lex == '(':
        numRow += 1
        resType = parseExpression()
        parseToken(')', 'brackets_op', '\t' * 7)
        print('\t' * 7 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
    else:
        failParse('невідповідність у Expression.Factor',
                  (numLine, lex, tok, 'rel_op, integer, real, ident або \'(\' Expression \')\''))
    return resType


def parseRead():
    global numRow
    print('\t' * 3 + 'parseRead():')
    _, lex, tok = getSymb()
    if lex == 'read' and tok == 'keyword':
        numRow += 1
        parseToken('(', 'brackets_op', '\t' * 5)
        #parseIdent()
        if parseIdent():
            numRow -= 1
            numLine1, lex1, tok1 = getSymb()
            numRow += 1
            tableOfVar[lex1] = (tableOfVar[lex1][0], tableOfVar[lex1][1], 'assigned')
        parseToken(')', 'brackets_op', '\t' * 5)
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
        parseIdent()
        parseToken(')', 'brackets_op', '\t' * 5)
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
        parseStatement()
        parseToken('fi','keyword','\t'*5)
        return True
    else: return False


def parseFor():
    global numRow
    print('\t' * 3 + 'parseFor():')
    _, lex, tok = getSymb()
    if lex == 'for' and tok == 'keyword':
        numRow += 1
        parseStatement()
        parseToken('to', 'keyword', '\t' * 5)
        parseExpression()
        parseToken('do', 'keyword', '\t' * 5)
        parseStatementList()
        parseToken('end', 'keyword', '\t' * 5)
        return True
    else: return False


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
    print(resType)
    return True

parseProgram()
