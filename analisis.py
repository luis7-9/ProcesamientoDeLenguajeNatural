import re

# Paso 1: Definir las categorías de tokens
# Estos diccionarios mapean lexemas a categorías de token
palabras_reservadas = {
    'if': 'PALABRA_RESERVADA',
    'else': 'PALABRA_RESERVADA',
    'while': 'PALABRA_RESERVADA',
    'for': 'PALABRA_RESERVADA',
    'return': 'PALABRA_RESERVADA',
    'int': 'PALABRA_RESERVADA',
    'float': 'PALABRA_RESERVADA',
    'double': 'PALABRA_RESERVADA',
    'char': 'PALABRA_RESERVADA',
    'void': 'PALABRA_RESERVADA',
    'bool': 'PALABRA_RESERVADA',
    'true': 'PALABRA_RESERVADA',
    'false': 'PALABRA_RESERVADA'
}

operadores = {
    '+': 'OP_ARITMETICO',
    '-': 'OP_ARITMETICO',
    '*': 'OP_ARITMETICO',
    '/': 'OP_ARITMETICO',
    '%': 'OP_ARITMETICO',
    '++': 'OP_ARITMETICO',
    '--': 'OP_ARITMETICO',
    '=': 'OP_ASIGNACION',
    '+=': 'OP_ASIGNACION',
    '-=': 'OP_ASIGNACION',
    '*=': 'OP_ASIGNACION',
    '/=': 'OP_ASIGNACION',
    '%=': 'OP_ASIGNACION',
    '==': 'OP_RELACIONAL',
    '!=': 'OP_RELACIONAL',
    '<': 'OP_RELACIONAL',
    '>': 'OP_RELACIONAL',
    '<=': 'OP_RELACIONAL',
    '>=': 'OP_RELACIONAL',
    '&&': 'OP_LOGICO',
    '||': 'OP_LOGICO',
    '!': 'OP_LOGICO'
}

delimitadores = {
    '(': 'PAR_ABRE',
    ')': 'PAR_CIERRA',
    '{': 'LLAVE_ABRE',
    '}': 'LLAVE_CIERRA',
    '[': 'COR_ABRE',
    ']': 'COR_CIERRA',
    ';': 'PUNTO_Y_COMA',
    ',': 'COMA',
    '.': 'PUNTO',
    ':': 'DOS_PUNTOS'
}


# Paso 2: Código de lectura de archivo
def leer_codigo(nombre_archivo):
    """
    Lee el contenido completo de un archivo.
    Maneja el error si el archivo no existe.
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encontró.")
        return None


# Paso 3: Tokenización (escáner con expresiones regulares y soporte de comentarios)
def tokenizar(codigo):
    """
    Mejora la tokenización usando re.finditer para una lógica más robusta.
    Devuelve una lista de tuplas (lexema, linea, columna).
    Ignora espacios y comentarios.
    """
    token_spec = [
        ('COMENTARIO_ML', r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'),
        ('COMENTARIO_SL', r'//[^\n]*'),
        ('CADENA', r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''),
        ('NUMERO', r'\d+(?:\.\d+)?'),
        ('IDENT', r'[A-Za-z_]\w*'),
        ('OPERADOR', r'==|!=|<=|>=|\+\+|--|\+=|-=|\*=|/=|%='
                     r'|&&|\|\||[+\-*/%!=<>]'),
        ('DELIM', r'[()\[\]{};,.:]'),
        ('NUEVA_LINEA', r'\n'),
        ('ESPACIO', r'[ \t\r]+'),
        ('DESCONOCIDO', r'.')
    ]

    # Combina todas las expresiones regulares en un solo patrón
    tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_spec)

    linea = 1
    tokens = []
    line_start = 0

    # Itera sobre todas las coincidencias encontradas por el patrón
    for m in re.finditer(tok_regex, codigo, re.DOTALL):
        kind = m.lastgroup
        lexema = m.group()

        if kind == 'NUEVA_LINEA':
            linea += 1
            line_start = m.end()  # Actualiza el inicio de la nueva línea
        elif kind in ('ESPACIO', 'COMENTARIO_SL', 'COMENTARIO_ML'):
            pass  # Ignorar
        elif kind == 'DESCONOCIDO':
            columna = m.start() - line_start + 1
            tokens.append((lexema, linea, columna))
        else:
            columna = m.start() - line_start + 1
            tokens.append((lexema, linea, columna))

    return tokens


# Paso 4: Código de clasificación
def clasificar_token(token):
    """
    Clasifica un lexema en una de las categorías de token.
    """
    if token in palabras_reservadas:
        return palabras_reservadas[token]
    elif token in operadores:
        return operadores[token]
    elif token in delimitadores:
        return f'DELIMITADOR_{delimitadores[token]}'
    elif re.fullmatch(r'\d+(?:\.\d+)?', token):
        return 'LITERAL_NUMERICO'
    elif (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'")):
        return 'LITERAL_CADENA'
    elif re.match(r'^[a-zA-Z_]\w*$', token):
        return 'IDENTIFICADOR'
    else:
        return 'SIMBOLO_DESCONOCIDO'


# Paso 5: Código de guardado de resultados
def guardar_resultados(resultados, nombre_archivo):
    """
    Guarda los resultados del análisis en un archivo.
    """
    with open(nombre_archivo, 'w', encoding='utf-8') as file:
        for token, categoria, linea, columna in resultados:
            file.write(f'({token}, {categoria}) @ linea {linea}, col {columna}\n')


# Lógica principal del programa
if __name__ == "__main__":
    nombre_archivo_entrada = "codigo.txt"
    nombre_archivo_salida = "analisis_lexico.txt"

    # Llama a las funciones para procesar el archivo
    codigo_fuente = leer_codigo(nombre_archivo_entrada)

    if codigo_fuente:
        tokens_crudos = tokenizar(codigo_fuente)

        resultados_analisis = []
        for lexema, linea, columna in tokens_crudos:
            categoria = clasificar_token(lexema)
            resultados_analisis.append((lexema, categoria, linea, columna))

        guardar_resultados(resultados_analisis, nombre_archivo_salida)
        print(f"Análisis léxico completado. Resultados guardados en '{nombre_archivo_salida}'.")
