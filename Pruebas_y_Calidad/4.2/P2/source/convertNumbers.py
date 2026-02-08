"""
Módulo para convertir números decimales a binario y hexadecimal.
Incluye manejo de errores y cálculo manual de conversiones.
"""

# pylint: disable=invalid-name

import sys
import time


def to_binary(n):
    """Convierte un número entero a binario usando residuos."""
    if n == 0:
        return "0"
    binary = ""
    is_negative = n < 0
    num = abs(int(n))
    while num > 0:
        binary = str(num % 2) + binary
        num //= 2
    return "-" + binary if is_negative else binary


def to_hexadecimal(n):
    """Convierte un número entero a hexadecimal usando residuos."""
    if n == 0:
        return "0"
    hex_chars = "0123456789ABCDEF"
    result = ""
    is_negative = n < 0
    num = abs(int(n))
    while num > 0:
        result = hex_chars[num % 16] + result
        num //= 16
    return "-" + result if is_negative else result


def format_output(file_name, results, duration):
    """Genera el string con el formato de tabla para los resultados."""
    header = f"{'ITEM':<6} {'DECIMAL':<10} {'BINARIO':<20} {'HEX':<12}"
    lines = [f"Resultados para: {file_name}", header, "-" * 50]

    for i, (dec, b, h) in enumerate(results, 1):
        lines.append(f"{i:<6} {dec:<10} {b:<20} {h:<12}")

    lines.append("-" * 50)
    lines.append(f"Execution Time: {duration:.4f} seconds\n")
    return "\n".join(lines)


def main():
    """Función principal para la ejecución del programa."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Uso: python convertNumbers.py fileWithData.txt")
        return

    file_name = sys.argv[1]
    converted_data = []

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                raw_val = line.strip()
                try:
                    val = int(float(raw_val))
                    converted_data.append((val, to_binary(val), to_hexadecimal(val)))
                except ValueError:
                    print(f"Error: Dato inválido omitido -> {raw_val}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_name}")
        return

    total_time = time.time() - start_time
    final_report = format_output(file_name, converted_data, total_time)

    print(final_report)
    with open("../results/ConvertionResults.txt", "a", encoding='utf-8') as f:
        f.write(final_report + "\n")


if __name__ == "__main__":
    main()
