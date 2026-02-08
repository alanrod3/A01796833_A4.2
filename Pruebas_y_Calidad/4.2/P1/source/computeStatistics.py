"""
Módulo para calcular estadísticas descriptivas.
"""

# pylint: disable=invalid-name

import sys
import time
import os


def calculate_statistics(numbers):
    """Calcula estadísticas ajustadas a los requerimientos."""
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

    # Moda (Ajustada a referencia: #N/A si no hay repeticiones)
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    max_freq = max(frequency.values())

    if max_freq == 1:
        mode = "#N/A"
    else:
        # Usamos max()
        modes = [key for key, val in frequency.items() if val == max_freq]
        mode = max(modes)

    # Suma de cuadrados para Varianza y SD
    sum_sq_diff = sum((x - mean) ** 2 for x in numbers)

    # Varianza Muestral (N-1) y SD Poblacional (N)
    variance = sum_sq_diff / (count - 1) if count > 1 else 0.0
    std_dev = (sum_sq_diff / count) ** 0.5

    return count, mean, median, mode, std_dev, variance


def format_report(file_name, stats, elapsed):
    """Genera el texto formateado para consola y archivo."""
    count, mean, median, mode, std_dev, variance = stats
    short_name = os.path.basename(file_name)
    report = (
        f"Resultados para: {short_name}\n"
        f"Count: {count}\n"
        f"Mean: {mean}\n"
        f"Median: {median}\n"
        f"Mode: {mode}\n"
        f"SD: {std_dev}\n"
        f"Variance: {variance}\n"
        f"Execution Time: {elapsed:.4f} seconds\n"
        + "-" * 40 + "\n"
    )
    return report


def main():
    """Función principal del programa."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Uso: python computeStatistics.py fileWithData.txt")
        return

    file_path = sys.argv[1]
    numbers = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                clean_line = line.strip()
                if clean_line:
                    try:
                        numbers.append(float(clean_line))
                    except ValueError:
                        print(f"Error: Dato inválido omitido -> {clean_line}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_path}")
        return

    data_stats = calculate_statistics(numbers)
    if not data_stats:
        return

    duration = time.time() - start_time
    final_output = format_report(file_path, data_stats, duration)

    print(final_output)
    with open("../results/StatisticsResults.txt", "a", encoding='utf-8') as f:
        f.write(final_output)


if __name__ == "__main__":
    main()
