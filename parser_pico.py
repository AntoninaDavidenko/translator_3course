from lexer_pico import lex
from lexer_pico import tableOfSymb

lex()
print('-'*30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('-'*30)

# номер рядка таблиці розбору/лексем/символів ПРОГРАМИ tableOfSymb
numRow=1
# кількість записів у таблиці розбору
len_tableOfSymb = len(tableOfSymb)
print(('len_tableOfSymb',len_tableOfSymb))


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
            parseType()
            parseToken(';', 'punct_op', '\t' * 4)
            numLine, lex, tok = getSymb()
        else:
            failParse('очiкувався iдентифiкатор', (numLine, lex, tok))
    return True


def parseType():
    global numRow
    print('\t' * 4 + 'parseType():')
    numLine, lex, tok = getSymb()
    numRow += 1
    if lex in ['integer', 'real', 'boolval'] and tok == 'keyword':

        print('\t' * 5 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
        return True
    else:
        failParse('невідповідність типу', (numLine, lex, tok, 'integer, real або boolval'))
        return False


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
        parseAssign()
        return True

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

    # тут - ознака того, що всі інструкції були коректно
    # розібрані і була знайдена остання лексема програми.
    # тому parseStatement() має завершити роботу
    elif (lex, tok) == ('stop','keyword'):
            return False

    elif (lex, tok) == ('end','keyword'):
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
        # розібрати арифметичний вираз
        parseExpression()
        return True
    else: return False


def parseExpression():
    global numRow
    print('\t' * 5 + 'parseExpression():')
    numLine, lex, tok = getSymb()

    # унарний мінус
    if lex == '-':
        numRow += 1
        print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))

    parseTerm()
    F = True
    # продовжувати розбирати Доданки (Term)
    # розділені лексемами '+' або '-'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('add_op'):
            numRow += 1
            print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            parseTerm()
        else:
            F = False
    return True


def parseTerm():
    global numRow
    print('\t' * 6 + 'parseTerm():')
    parseFactor()
    F = True
    # продовжувати розбирати Множники (Factor)
    # розділені лексемами '*' або '/'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('mult_op'):
            numRow += 1
            print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            parseFactor()
        elif tok in ('pow_op'):
            numRow += 1
            print('\t' * 6 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            parsePower()
        else:
            F = False
    return True


def parsePower():
    global numRow
    print('\t' * 7 + 'parsePower():')
    parseFactor()
    F = True
    while F:
        numLine, lex, tok = getSymb()
        if lex == '!':
            numRow += 1
            print('\t' * 7 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
            parsePower()
        else:
            F = False
    return True


def parseFactor():
    global numRow
    print('\t' * 7 + 'parseFactor():')
    numLine, lex, tok = getSymb()
    print('\t' * 7 + 'parseFactor():=============рядок: {0}\t (lex, tok):{1}'.format(numLine, (lex, tok)))

    # перша і друга альтернативи для Factor
    # якщо лексема - це константа або ідентифікатор
    if tok in ('integer', 'real', 'boolval', 'ident'):
        numRow += 1
        print('\t' * 7 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))

    # третя альтернатива для Factor
    # якщо лексема - це відкриваюча дужка
    elif lex == '(':
        numRow += 1
        parseExpression()
        parseToken(')', 'brackets_op', '\t' * 7)
        print('\t' * 7 + 'в рядку {0} - {1}'.format(numLine, (lex, tok)))
    else:
        failParse('невідповідність у Expression.Factor',
                  (numLine, lex, tok, 'rel_op, integer, real, ident або \'(\' Expression \')\''))
    return True


def parseRead():
    global numRow
    print('\t' * 3 + 'parseRead():')
    _, lex, tok = getSymb()
    if lex == 'read' and tok == 'keyword':
        numRow += 1
        parseToken('(', 'brackets_op', '\t' * 5)
        parseIdent()
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
    parseExpression()
    numLine, lex, tok = getSymb()
    if tok == 'rel_op':
            numRow += 1
            print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    else:
        failParse('mismatch in BoolExpr',(numLine,lex,tok,'rel_op'))
    parseExpression()
    return True

parseProgram()