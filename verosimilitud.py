import re
from collections import defaultdict, Counter


# Nuevo: Función para leer el archivo del corpus
def leer_corpus_desde_archivo(nombre_archivo):
    """
    Lee un archivo de texto, asumiendo una oración por línea.
    Devuelve una lista de cadenas de texto (oraciones).
    """
    try:
        # 'r' para modo lectura, 'utf-8' para manejar tildes y caracteres especiales
        with open(nombre_archivo, 'r', encoding='utf-8') as file:
            # Lee cada línea y elimina espacios en blanco al inicio/final
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encontró. "
              "Asegúrate de que está en la misma carpeta que el script.")
        return None


# El corpus de ejemplo ha sido eliminado, ya que ahora se leerá desde un archivo.

def preprocesar_corpus(corpus, incluir_fronteras=False):
    """
    Preprocesa el corpus, tokenizando las oraciones y opcionalmente
    añadiendo tokens de inicio y fin de oración.
    """
    tokenized_corpus = []
    for sentence in corpus:
        tokens = sentence.lower().split()
        if incluir_fronteras:
            tokens = ["<s>"] + tokens + ["</s>"]
        tokenized_corpus.append(tokens)
    return tokenized_corpus


def construir_ngrams(corpus_tokenizado, n):
    """
    Construye los n-gramas a partir de un corpus tokenizado.
    """
    ngrams = []
    for sentence in corpus_tokenizado:
        for i in range(len(sentence) - n + 1):
            ngrams.append(tuple(sentence[i:i + n]))
    return ngrams


def calcular_probabilidades_mle(ngrams, n):
    """
    Calcula las probabilidades condicionales P(W_n | W_n-1, ..., W_1)
    usando la Estimación de Máxima Verosimilitud (MLE).
    """
    # Contadores para los n-gramas y los (n-1)-gramas
    ngram_counts = Counter(ngrams)
    context_counts = defaultdict(int)

    for ngram in ngrams:
        context = ngram[:-1]
        context_counts[context] += 1

    # Calcular las probabilidades
    probabilities = {}
    for ngram, count in ngram_counts.items():
        context = ngram[:-1]
        if context_counts[context] > 0:
            prob = count / context_counts[context]
            probabilities[ngram] = prob
    return probabilities


def imprimir_resultados(probabilidades, n, titulo):
    """
    Imprime los n-gramas, sus conteos y las probabilidades calculadas.
    """
    print(f"--- {titulo} ---")
    print("N-grama\t\t\t\t\tFrecuencia\t\tProbabilidad (MLE)")
    print("-" * 70)

    # Ordenar los n-gramas para una presentación más clara
    sorted_ngrams = sorted(probabilidades.keys())

    # Recalcular conteos para la presentación
    ngram_counts = Counter(sorted_ngrams)

    for ngram in sorted_ngrams:
        count = ngram_counts[ngram]
        prob = probabilidades[ngram]

        # Formato de la tabla
        context = " ".join(ngram[:-1])
        word = ngram[-1]
        print(f"P({word} | {context})\t\t{count}\t\t\t{prob:.4f}")
    print("\n")


if __name__ == "__main__":
    # Nombre del archivo que contendrá el corpus
    nombre_archivo_corpus = "texto.txt"

    # Nuevo: Llama a la función para leer el corpus desde el archivo
    corpus = leer_corpus_desde_archivo(nombre_archivo_corpus)

    if corpus:
        n_value = 2  # Usaremos bigramas para el ejemplo

        # PARTE 1: Cálculo sin fronteras de oración
        print("Análisis sin fronteras de oración (bigramas)")

        corpus_sin_fronteras = preprocesar_corpus(corpus, incluir_fronteras=False)
        bigramas_sin_fronteras = construir_ngrams(corpus_sin_fronteras, n_value)

        # Este conteo es solo para mostrar en la tabla, no para el cálculo
        counts_sin_fronteras = Counter(bigramas_sin_fronteras)

        probabilidades_sin_fronteras = calcular_probabilidades_mle(bigramas_sin_fronteras, n_value)

        # Imprimir la tabla de resultados
        print("Tabla de n-gramas (sin fronteras):")
        print("N-grama\t\t\tFrecuencia")
        print("-" * 35)
        for ngram, count in counts_sin_fronteras.items():
            print(f"{ngram}\t\t\t{count}")

        print("\n")
        imprimir_resultados(probabilidades_sin_fronteras, n_value, "Probabilidades (MLE) sin fronteras")

        print("=" * 70)

        # PARTE 2: Cálculo con fronteras de oración
        print("Análisis con fronteras de oración (bigramas)")

        corpus_con_fronteras = preprocesar_corpus(corpus, incluir_fronteras=True)
        bigramas_con_fronteras = construir_ngrams(corpus_con_fronteras, n_value)

        # Conteo para la tabla
        counts_con_fronteras = Counter(bigramas_con_fronteras)

        probabilidades_con_fronteras = calcular_probabilidades_mle(bigramas_con_fronteras, n_value)

        # Imprimir la tabla de resultados
        print("Tabla de n-gramas (con fronteras):")
        print("N-grama\t\t\tFrecuencia")
        print("-" * 35)
        for ngram, count in counts_con_fronteras.items():
            print(f"{ngram}\t\t\t{count}")

        print("\n")
        imprimir_resultados(probabilidades_con_fronteras, n_value, "Probabilidades (MLE) con fronteras")

        # PARTE 3: Reflexión sobre la utilidad de las fronteras
        print("=" * 70)
        print("Reflexión sobre la utilidad de las fronteras de oración:")
        print(
            "La inclusión de tokens de inicio (<s>) y fin (</s>) permite al modelo de lenguaje aprender la probabilidad de"
            " que una oración comience o termine con una palabra específica. Por ejemplo, al calcular P(perro | el), "
            "el modelo sin fronteras consideraría todas las veces que la palabra 'el' precede a 'perro'. Sin embargo, "
            "al usar fronteras, se puede calcular P(el | <s>), que nos dice la probabilidad de que una oración empiece con "
            "la palabra 'el'. Esto evita mezclar el contexto entre oraciones distintas y mejora la precisión del modelo al "
            "generar texto que se ajusta a la estructura gramatical y semántica de las oraciones individuales, en lugar de "
            "tratar todo el corpus como un solo flujo de palabras.")