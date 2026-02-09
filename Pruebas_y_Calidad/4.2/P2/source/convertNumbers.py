"""
Módulo para convertir números decimales a binario y hexadecimal.
Incluye manejo de errores y conversión con complemento a 2 para negativos.
"""

# pylint: disable=invalid-name

import sys
import time


def to_binary(n):
    """
    Convierte un número entero a binario.
    Usa una máscara de 10 bits (0x3FF) para representar números negativos
    en complemento a 2, coincidiendo con los resultados de referencia.
    """
    if n == "#VALUE!":
        return "#VALUE!"
    
    val = int(n)
    if val < 0:
        val = val & 0x3FF  # Máscara de 10 bits para negativos
    
    return format(val, 'b').upper()


def to_hexadecimal(n):
    """
    Convierte un número entero a hexadecimal.
    Usa una máscara de 40 bits (0xFFFFFFFFFF) para representar números negativos
    en complemento a 2, coincidiendo con los resultados de referencia.
    """
    if n == "#VALUE!":
        return "#VALUE!"
    
    val = int(n)
    if val < 0:
        val = val & 0xFFFFFFFFFF  # Máscara de 40 bits para negativos
        
    return format(val, 'X').upper()


def format_output(file_name, results, duration):
    """Genera el string con el formato de tabla para los resultados."""
    # Se ajustan los encabezados y el espaciado para mayor legibilidad
    header = f"{'ITEM':<6} {'DECIMAL':<15} {'BINARIO':<25} {'HEX':<20}"
    lines = [f"Resultados para: {file_name}", header, "-" * 68]

    for i, (dec, b, h) in enumerate(results, 1):
        # dec se convierte a string para manejar casos de texto como 'ABC'
        lines.append(f"{i:<6} {str(dec):<15} {b:<25} {h:<20}")

    lines.append("-" * 68)
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
                if not raw_val:
                    continue  # Saltar líneas vacías
                
                try:
                    # Intentar convertir a float y luego a int (para manejar ej. "5.0")
                    val = int(float(raw_val))
                    converted_data.append((val, to_binary(val), to_hexadecimal(val)))
                except ValueError:
                    # Requerimiento: Si falla, se guarda el dato original y #VALUE!
                    converted_data.append((raw_val, "#VALUE!", "#VALUE!"))
                    print(f"Error: Dato inválido -> {raw_val}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_name}")
        return

    total_time = time.time() - start_time
    final_report = format_output(file_name, converted_data, total_time)

    print(final_report)
    
    # Escribir resultados en el archivo de salida
    try:
        with open("../results/ConvertionResults.txt", "a", encoding='utf-8') as f:
            f.write(final_report + "\n")
    except FileNotFoundError:
        # Fallback por si la carpeta ../results/ no existe
        with open("ConvertionResults.txt", "a", encoding='utf-8') as f:
            f.write(final_report + "\n")


if __name__ == "__main__":
    main()