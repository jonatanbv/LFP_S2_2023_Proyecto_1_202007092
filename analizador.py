from collections import namedtuple
from expre import *
from arit import ExpresionAritmetica
from trigonometira import ExpresionTrigonometrica
from arbol import *

Token = namedtuple("Token", ["value", "line", "col"])

# numero de linea
line = 1
# numero de columna
col = 1

tokens = []


configuracion = {
    "texto": None,
    "fondo": None,
    "fuente": None,
    "forma": None,
}


# formar un string
def tokenize_string(input_str, i):
    token = ""
    for char in input_str:
        if char == '"':
            return [token, i]
        token += char
        i += 1
    print("Error: string no cerrado")


# formar un numero
def tokenize_number(input_str, i):
    token = ""
    isDecimal = False
    for char in input_str:
        if char.isdigit():
            token += char
            i += 1
        elif char == "." and not isDecimal:
            token += char
            i += 1
            isDecimal = True
        else:
            break
    if isDecimal:
        return [float(token), i]
    return [int(token), i]


# formar los tokens
def tokenize_input(input_str):
    # referenciar las variables globales
    global line, col, tokens
    # iterar sobre cada caracter del input
    i = 0
    # mientras no se llegue al final del input
    while i < len(input_str):
        # obtener el caracter actual
        char = input_str[i]
        if char.isspace():
            # si es un salto de linea
            if char == "\n":
                # print({"char": char, "line": line, "col": col, "i": i})
                # tokens.append("EOL")
                line += 1
                col = 1
            # si es un tabulador
            elif char == "\t":
                col += 4
            # si es un espacio
            else:
                col += 1
            # incrementar el indice
            i += 1
        # si es un string formar el token
        elif char == '"':
            string, pos = tokenize_string(input_str[i + 1 :], i)
            col += len(string) + 1
            i = pos + 2
            token = Token(string, line, col)
            tokens.append(token)
        elif char in ["{", "}", "[", "]", ",", ":"]:
            print({"char": char, "line": line, "col": col, "i": i})
            col += 1
            i += 1
            token = Token(char, line, col)
            tokens.append(token)
        elif char.isdigit():
            number, pos = tokenize_number(input_str[i:], i)
            col += pos - i
            i = pos
            token = Token(number, line, col)
            tokens.append(token)
        else:
            print(
                "Error: caracter desconocido:",
                char,
                "en linea:",
                line + 1,
                "columna:",
                col + 1,
            )
            i += 1
            col += 1


# crear las instrucciones a partir de los tokens
def get_instruccion():
    global tokens
    operacion = None
    value1 = None
    value2 = None
    while tokens:
        token = tokens.pop(0)
        print("VALUE: ", token)
        if token.value == "operacion":
            # eliminar el :
            tokens.pop(0)
            operacion = tokens.pop(0).value
        elif token.value == "valor1":
            # eliminar el :
            tokens.pop(0)
            value1 = tokens.pop(0).value
            if value1 == "[":
                value1 = get_instruccion()
        elif token.value == "valor2":
            # eliminar el :
            tokens.pop(0)
            value2 = tokens.pop(0).value
            if value2 == "[":
                value2 = get_instruccion()
        elif token.value in ["texto", "fondo", "fuente", "forma"]:
            tokens.pop(0)
            configuracion[token.value] = tokens.pop(0).value
        else:
            print("\033[1;31;40m Error: token desconocido:", token, "\033[0m")

        if operacion and value1 and value2:
            return ExpresionAritmetica(operacion, value1, value2, 0, 0)
        if operacion and operacion in ["seno"] and value1:
            return ExpresionTrigonometrica(operacion, value1, 0, 0)
    return None


# entrada = open("ejemplo_entrada.json", "r").read()


def create_instructions():
    global tokens
    global arbol
    instrucciones = []
    while tokens:
        instruccion = get_instruccion()
        if instruccion:
            instrucciones.append(instruccion)
    arbol.agregarConfiguracion(configuracion)
    return instrucciones


def analizar(entrada):
    tokenize_input(entrada)
    arbol.dot.clear()
    arbol.agregarConfiguracion(configuracion)
    instrucciones = create_instructions()
    for i in instrucciones:
        print("RESULTADO INSTRUCCION: ", i.interpretar())

    return arbol
# for i in tokens:
#     print(i)

# print("INSTRUCCIONES: ", instrucciones)

# print("\n" * 3)
# print(arbol.dot.source)