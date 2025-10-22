#!env python3
import sys
import os
import subprocess

def generar_fichero_dat(n, m, k_d, k_p, distancias, pasajeros, path):
    """
    Genera el fichero de salida (.dat) con el formato que requiere GLPK
    """
    try:
        with open (path, 'w') as f:
            
            # Parámetros escalares
            f.write(f"param n := {n};\n")
            f.write(f"param m := {m};\n")
            f.write(f"param k_d := {k_d};\n")
            f.write(f"param k_p := {k_p};\n\n")

            # Escribir conjuntos
            f.write(f"set FRANJAS := {' '.join(map(str, range(1, n + 1)))};\n")
            f.write(f"set AUTOBUSES := {' '.join(map(str, range(1, m + 1)))};\n\n")

            # Escribir parámetro de distancias (d)
            f.write("param d := \n")
            for i, dist in enumerate(distancias, 1):
                f.write(f"    {i} {dist}\n")
            f.write(";\n\n")

            # Escribir parámetro de pasajeros (p)
            f.write("param p := \n")
            for i, pas in enumerate(pasajeros, 1):
                f.write(f"    {i} {pas}\n")
            f.write(";\n\n")

            f.write("end;\n")

        return True
    
    except IOError as e:
        print(f"Error al escribir el fichero de datos '{path}': {e}", file=sys.stderr)
        return False

def resolver_problema(mod_file, dat_file):
    
    # 1. Ejecuta el solver y captura su salida
    sol_file = "parte-2-1.sol" # Fichero temporal para poder almacenar luego las variables
    command = ["glpsol", "--model", mod_file, "--data", dat_file, "--output", sol_file]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
    
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"Error ejecutando GLPK: {e}", file=sys.stderr)
        return

    # 2. Comprobar que existe solución óptima
    output = result.stdout # Almacena el LOG
    factible = re.compile(r"(INTEGER )?OPTIMAL SOLUTION FOUND", re.IGNORECASE)

    # Comprueba el LOG para ver si hubo éxito
    if not factible.search(output):
        print("Error: El problema es infactible", file=sys.stderr)
        return
    
    try:
        with open(sol_file, 'r') as f:
            solution_text = f.read() # Este texto contiene la tabla de variables y el valor de la función objetivo
    except FileNotFoundError:
        print(f"Error: GLPK no generó el fichero de solución '{sol_file}'", file=sys.stderr)
        return
    
    os.remove(sol_file)

    # 4. Parsear la solución
    obj_val = num_restr = num_vars = ""
    asignados = {} # Diccionario para {bus: franja}
    no_asignados = [] # Lista para [bus]

    if m := re.search(r"Objective:.*?= *([-+]?[\d\.]+(?:[eE][-+]?\d+)?)", solution_text):
        obj_val = m.group(1) 

    if m := re.search(r"(\d+) rows, +(\d+) columns,", output):
        num_restr = m.group(1)
        num_vars = m.group(2)

    pattern = re.compile(
        r"^\s*\d+\s+(x\[(\d+),(\d+)\]|y\[(\d+)\])\s+[A-Z]+\s+([\d\.]+)", 
        re.MULTILINE
    )

    # Itera sobre todas las coincidencias en el fichero .sol
    for m in pattern.finditer(solution_text):
        
        # Si el valor (grupo 5) es menor que 1.0, lo ignora
        if float(m.group(5)) < 1.0:
            continue
            
        # Asigna la variable
        if m.group(2): # Si el grupo 2 (bus de 'x') existe -> asignado
            asignados[int(m.group(2))] = int(m.group(3))
            
        elif m.group(4): # Si el grupo 4 (bus de 'y') existe -> no_asignado
            no_asignados.append(int(m.group(4)))

    # 3. Imprimir la solución
    # 3.1 Imprime la primera línea
    print(f"Valor Objetivo: {obj_val} | Variables de decisión: {num_vars} | Restricciones: {num_restr}\n")

    # 3.2 Imprime los autobuses asignados a una franja
    print("Asignaciones (Autobús -> Franja):")
    if asignados:
        for bus in sorted(asignados.keys()):
            print(f"  - Autobús {bus} asignado a franja {asignados[bus]}")
    else:
        print("  - Ningún autobús asignado.")

    # 3.3 Imprime los autobuses sin asignar a ninguna franja
    print("\nAutobuses No Asignados:")
    if no_asignados:
        for bus in sorted(no_asignados):
            print(f"  - Autobús {bus} no asignado")
    else:
        print("  - Todos los autobuses fueron asignados.")
            
def main():

    # 1. Validación de argumentos de entrada
    if len(sys.argv) != 3:
        print("Error en el formato: ./gen-1.py <fichero-entrada> <fichero-salida.dat>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    dat_file = sys.argv[2]
    mod_file = "parte-2-1.mod"

    if not os.path.exists(mod_file):
        print(f"Error: No existe la ruta del fichero modelo '{mod_file}'", file=sys.stderr)
        sys.exit(1)

    # 2. Leer y procesar el fichero de entrada
    try:
        with open(input_file, 'r') as f:
            # Línea 1: n y m
            n, m = map(int, f.readline().strip().split())

            # Línea 2: k_d y k_p
            k_d, k_p = map(float, f.readline().strip().split())

            # Línea 3: Distancias (d1, ..., dm)
            distancias = list(map(int, f.readline().strip().split()))

            # Línea 4: Pasajeros (p1, ..., pm)
            pasajeros = list(map(int, f.readline().strip().split()))

        if len(distancias) != m or len(pasajeros) != m:
            print(f"Error: El número de autobuses (m={m}) no coincide con los datos (distancias: {len(distancias)}, pasajeros: {len(pasajeros)})", file=sys.stderr)
            sys.exit(1)
    
    except FileNotFoundError:
        print(f"Error: Fichero de entrada '{input_file}' no encontrado", file=sys.stderr)
        sys.exit(1)
    except(ValueError, IndexError):
        print(f"Error: Formato incorrecto en el fichero de entrada '{input_file}'", file=sys.stderr)
        sys.exit(1)
    
    # 3. Generar el fichero de salida (.dat)
    if not generar_fichero_dat(n, m, k_d, k_p, distancias, pasajeros, dat_file):
        sys.exit(1)
    
    # 4. Resolver el problema con GLPK
    resolver_problema(mod_file, dat_file)

if __name__ == "__main__":
    main()

