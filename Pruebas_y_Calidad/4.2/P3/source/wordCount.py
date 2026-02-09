"""
Módulo para contar la frecuencia de palabras en un archivo de texto.
"""

# pylint: disable=invalid-name

import sys
import time


def count_word_frequencies(data_lines):
    """Identifica palabras distintas y cuenta su frecuencia."""
    frequencies = {}
    for line in data_lines:
        # Dividimos por espacios y limpiamos caracteres básicos
        words = line.split()
        for word in words:
            # Limpieza básica para evitar que "Hola," y "Hola" sean diferentes
            clean_word = word.strip('.,"()!?¿¡').lower()
            if clean_word:
                if clean_word in frequencies:
                    frequencies[clean_word] += 1
                else:
                    frequencies[clean_word] = 1
    return frequencies


def format_word_results(file_name, frequencies, duration):
    """Formatea los resultados del conteo en una tabla clara."""
    header = f"{'WORD':<20} {'FREQUENCY':<10}"
    lines = [f"Resultados para: {file_name}", header, "-" * 35]

    # Ordenamos por frecuencia descendente o alfabético si prefieres
    sorted_words = sorted(frequencies.items(), key=lambda item: item[1],
                          reverse=True)

    for word, count in sorted_words:
        lines.append(f"{word:<20} {count:<10}")

    lines.append("-" * 35)
    total_words = sum(frequencies.values())
    lines.append(f"Total de palabras: {total_words}")
    lines.append(f"Execution Time: {duration:.4f} seconds\n")
    return "\n".join(lines)


def main():
    """Función principal para la ejecución del programa."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Uso: python wordCount.py fileWithData.txt")
        return

    file_name = sys.argv[1]
    raw_lines = []

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            raw_lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_name}")
        return
    except Exception as e: # pylint: disable=broad-except
        print(f"Error al leer el archivo: {e}")
        return

    word_map = count_word_frequencies(raw_lines)
    total_time = time.time() - start_time
    final_report = format_word_results(file_name, word_map, total_time)

    print(final_report)
    with open("../results/WordCountResults.txt", "a", encoding='utf-8') as f:
        f.write(final_report + "\n")


if __name__ == "__main__":
    main()
