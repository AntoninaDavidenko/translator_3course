tableOfLanguageTokens = {'program': 'keyword', 'var': 'keyword', 'start': 'keyword', 'stop': 'keyword',
                         'boolval': 'keyword', 'true': 'boolval', 'false': 'boolval', 'integer': 'keyword', 'real': 'keyword',
                         'if': 'keyword', 'then': 'keyword', 'fi': 'keyword', 'UnderScore': 'keyword', 'write': 'keyword',
                         'for': 'keyword', 'to': 'keyword', 'do': 'keyword', 'end': 'keyword', 'read': 'keyword',
                         '==': 'assign_op', '.': 'dot', ' ': 'ws', '\t': 'ws', '\n': 'nl',
                         '-': 'add_op', '+': 'add_op', '*': 'mult_op', '/': 'mult_op', '(': 'brackets_op', ')': 'brackets_op',
                         '!': 'pow_op', ';': 'punct_op', '::': 'decl_op',
                         '=': 'rel_op', '<': 'rel_op', '>': 'rel_op', '<=': 'rel_op', '>=': 'rel_op', '=!': 'rel_op'}

# Решту токенів визначаємо не за лексемою, а за заключним станом
tableIdentFloatInt = {2: 'ident', 6: 'real', 9: 'integer'}
stf = {(0, 'Letter'): 1, (1, 'Letter'): 1, (1, 'Digit'): 1, (1, 'UnderScore'): 1, (1, 'other'): 2,
       (0, 'Digit'): 4, (4, 'Digit'): 4, (4, 'dot'): 5, (5, 'Digit'): 55, (55, 'Digit'): 55, (4, 'other'): 9,
       (55, 'other'): 6,
       (0, '='): 11, (11, '='): 12, (11, '!'): 41, (11, 'other'): 42,
       (5, 'other'): 102,
       (0, 'ws'): 0,
       (0, 'nl'): 13,
       (0, '+'): 14, (0, '-'): 14, (0, '*'): 14, (0, '/'): 14, (0, '('): 14, (0, ')'): 14, (0, '!'): 14, (0, ';'): 14,
       (0, ':'): 15, (15, ':'): 16,
       (15, 'other'): 103,
       (0, '<'): 20, (20, '='): 21,
       (20, 'other'): 22,
       (0, '>'): 30, (30, '='): 31,
       (30, 'other'): 32,
       (0, 'other'): 101
       }
# Добавить isfinal и lex + переменные
initState = 0  # q0 - стартовий стан
F = {2, 6, 9, 12, 13, 14, 16, 101, 102, 103, 21, 22, 31, 32, 41, 42}
Fstar = {2, 6, 9, 22, 32, 42}  # зірочка
Ferror = {101, 102, 103}  # обробка помилок

tableOfId = {}  # Таблиця ідентифікаторів
tableOfConst = {}  # Таблиць констант
tableOfSymb = {}  # Таблиця символів програми (таблиця розбору)

state = initState  # поточний стан

f = open('test2.my_lang', 'r')
sourceCode = f.read()
f.close()

FSuccess = (True, 'Lexer')

lenCode = len(sourceCode) - 1
numLine = 1  # лексичний аналіз починаємо з першого рядка
numChar = -1  # з першого символа (в Python'і нумерація - з 0)
char = ''  # ще не брали жодного символа
lexeme = ''  # ще не починали розпізнавати лексеми


def classOfChar(char):
    if char in '.':
        res = "dot"
    elif char in 'abcdefghijklmnopqrstuvwxyz':
        res = "Letter"
    elif char in "0123456789":
        res = "Digit"
    elif char in " \t":
        res = "ws"
    elif char in "\n":
        res = "nl"
    elif char in "+-:=*/();!^<>":
        res = char
    elif char in '_':
        res = "UnderScore"
    else:
        res = 'символ не належить алфавіту'
    return res


# мб переделать
def fail():
    global state, numLine, char
    print(numLine)
    if state == 101:
        print('Lexer: у рядку ', numLine, ' неочікуваний символ ' + char)
        exit(101)
    if state == 102:
        print('Lexer: у рядку ', numLine, ' очікувалася цифра, а не ' + char)
        exit(102)
    if state == 103:
        print('Lexer: у рядку ', numLine, 'очікувався символ ":", а не  ' + char)
        exit(103)


def nextChar():
    global numChar
    numChar += 1
    return sourceCode[numChar]


def putCharBack(numChar):
    return numChar - 1


def nextState(state, classCh):
    try:
        return stf[(state, classCh)]
    except KeyError:
        return stf[(state, 'other')]


def getToken(state, lexeme):
    try:
        return tableOfLanguageTokens[lexeme]
    except KeyError:
        return tableIdentFloatInt[state]


def indexIdConst(state, lexeme):
    indx = 0
    if state == 2:
        indx = tableOfId.get(lexeme)
        #		token=getToken(state,lexeme)
        if indx is None:
            indx = len(tableOfId) + 1
            tableOfId[lexeme] = indx
    if state == 6:
        indx = tableOfConst.get(lexeme)
        if indx is None:
            indx = len(tableOfConst) + 1
            constType = 'real'
            tableOfConst[lexeme] = constType
    if state == 9:
        indx = tableOfConst.get(lexeme)
        if indx is None:
            indx = len(tableOfConst) + 1
            constType = 'integer'
            tableOfConst[lexeme] = constType
    return indx


def isFinal(state):
    if (state in F):
        return True
    else:
        return False


def processing():
    global state, lexeme, numLine, numChar  # , tableOfSymb ,char
    if state == 13:  # \n
        numLine += 1
        state = 0
    if state in (2, 6, 9):  # keyword, ident, float, int
        token = getToken(state, lexeme)
        if token != 'keyword':  # не keyword
            index = indexIdConst(state, lexeme)
            print('{0:<3d} {1:<10s} {2:<10s} {3:<10s} '.format(numLine, lexeme, token, str(index)))
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, index)
        else:  # якщо keyword
            print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))  # print(numLine,lexeme,token)
            tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        numChar = putCharBack(numChar)  # зірочка
        state = 0
    if state in (12, 16, 14, 21, 31, 41): # ==, ::, char, <=, >=, =!
        lexeme += char
        token = getToken(state, lexeme)
        print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        state = 0
    if state in (32, 22, 42): # <, >, =
        token = getToken(state, lexeme)
        print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine, lexeme, token))
        tableOfSymb[len(tableOfSymb) + 1] = (numLine, lexeme, token, '')
        lexeme = ''
        numChar = putCharBack(numChar)  # зірочка
        state = 0
    if state in (101, 102, 103):  # ERROR
        fail()


def lex():
    global state, numLine, char, lexeme, numChar, FSuccess
    try:
        while numChar < lenCode:
            char = nextChar()  # прочитати наступний символ
            classCh = classOfChar(char)  # до якого класу належить
            state = nextState(state, classCh)  # обчислити наступний стан
            if isFinal(state):  # якщо стан заключний
                processing()  # виконати семантичні процедури
            # if state in Ferror:	    # якщо це стан обробки помилки
            # break					#      то припинити подальшу обробку
            elif state == initState:
                lexeme = ''  # якщо стан НЕ заключний, а стартовий - нова лексема
            else:
                lexeme += char  # якщо стан НЕ закл. і не стартовий - додати символ до лексеми
        print('Lexer: Лексичний аналіз завершено успішно')
    except SystemExit as e:
        # Встановити ознаку неуспішності
        FSuccess = (False, 'Lexer')
        # Повідомити про факт виявлення помилки
        print('Lexer: Аварійне завершення програми з кодом {0}'.format(e))


lex()

# Таблиці: розбору, ідентифікаторів та констант
print('-' * 30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('tableOfId:{0}'.format(tableOfId))
print('tableOfConst:{0}'.format(tableOfConst))
