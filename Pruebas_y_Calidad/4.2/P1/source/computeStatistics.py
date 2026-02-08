"""
Programa para calcular estadísticas descriptivas a partir de un archivo.
"""

import sys
import time
import os


def calculate_statistics(numbers):
    """Calcula las medidas estadísticas usando algoritmos básicos."""
    count = len(numbers)
    if count == 0:
        return None

    # Media
    mean = sum(numbers) / count

    # Mediana
    sorted_nums = sorted(numbers)
    if count % 2 == 0:
        median = (sorted_nums[count // 2 - 1] + sorted_nums[count // 2]) / 2
    else:
        median = sorted_nums[count // 2]

    # Moda
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    
    max_freq = max(frequency.values())
    
    if max_freq == 1:
        mode = "#N/A"
    else:
        # # En caso de empate, toma el valor más grande
        modes = [key for key, val in frequency.items() if val == max_freq]
        mode = max(modes)

    # Cálculo auxiliar de suma de cuadrados
    sum_sq_diff = sum((x - mean) ** 2 for x in numbers)

    # 4. Varianza (N-1)
    if count > 1:
        variance = sum_sq_diff / (count - 1)
    else:
        variance = 0.0

    # Desviación Estándar Poblacional
    std_dev = (sum_sq_diff / count) ** 0.5

    return count, mean, median, mode, std_dev, variance


def main():
    """Función principal para el manejo de archivos y ejecución."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Uso: python computeStatistics.py fileWithData.txt")
        return

    file_name = sys.argv[1]
    numbers = []

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    numbers.append(float(line.strip()))
                except ValueError:
                    print(f"Error: Dato inválido omitido -> {line.strip()}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_name}")
        return

    stats = calculate_statistics(numbers)
    if not stats:
        return

    count, mean, median, mode, std_dev, variance = stats
    elapsed_time = time.time() - start_time

    short_name = os.path.basename(file_name)

    # Formateo de resultados
    output = (
        f"Resultados para: {short_name}\n"
        f"Count: {count}\n"
        f"Mean: {mean}\n"
        f"Median: {median}\n"
        f"Mode: {mode}\n"
        f"SD: {std_dev}\n"
        f"Variance: {variance}\n"
        f"Execution Time: {elapsed_time:.4f} seconds\n"
        + "-" * 40 + "\n"
    )

    # Imprimir en pantalla
    print(output)

    # Guardar en archivo (append para no borrar resultados previos si se desea)
    with open("../results/StatisticsResults.txt", "a", encoding='utf-8') as out_f:
        out_f.write(output)


if __name__ == "__main__":
    main()
