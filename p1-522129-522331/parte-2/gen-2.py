#!/usr/bin/env python3
import sys
import os
import re
import subprocess

def generar_fichero_dat(n, m, u, C, O, path):

    try:
        with open (path, 'w') as f:
            
            # Escribir conjuntos
            f.write(f"set FRANJA := {' '.join(map(str, range(1, n + 1)))};\n")
            f.write(f"set AUTOBUS := {' '.join(map(str, range(1, m + 1)))};\n")
            f.write(f"set TALLER := {' '.join(map(str, range(1, u + 1)))};\n\n")

            # Escribir la matriz C:
            f.write("param C : ")
            f.write(' '.join(map(str, range(1, m + 1))) + " :=\n")
            for i in range(m):
                # Escribe el índice i y la fila de datos
                f.write(f"  {i+1} {' '.join(map(str, C[i]))}\n")
            f.write(";\n\n")

            # Escribir la matriz O
            f.write("param O : ")
            f.write(' '.join(map(str, range(1, u + 1))) + " :=\n")
            for s in range(n):
                fila_franja_s = [str(O[t][s]) for t in range(u)]
                # Escribe el índice s y la fila de datos
                f.write(f"  {s+1} {' '.join(fila_franja_s)}\n")
            f.write(";\n\n")

            f.write("end;\n")

        return True
    
    except IOError as e:
        print(f"Error al escribir el fichero de datos '{path}': {e}", file=sys.stderr)
        return False

def resolver_problema(mod_file, dat_file):
    
    # 1. Ejecuta el solver y captura su salida
    sol_file = "parte-2-2.sol" # Fichero temporal para poder almacenar luego las variables
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
    asignados = {} # Diccionario para {bus: (taller, franja)}

    if m := re.search(r"Objective:.*?= *([-+]?[\d\.]+(?:[eE][-+]?\d+)?)", solution_text):
        obj_val = m.group(1) 

    if m := re.search(r"(\d+) rows, +(\d+) columns,", output):
        num_restr = m.group(1)
        num_vars = m.group(2)

    pattern = re.compile(
        r"^\s*\d+\s+x\[(\d+),(\d+),(\d+)\]\s*(?:[A-Za-z*]+\s*)?(\S+).*",
        re.MULTILINE
    )
    # Itera sobre todas las coincidencias en el fichero .sol
    for m in pattern.finditer(solution_text):
        # Si el valor (grupo 4) es menor que 1.0, lo ignora
        if float(m.group(4)) < 1.0:
            continue
        
        bus_i = int(m.group(1))
        taller_t = int(m.group(2))
        franja_s = int(m.group(3))
        
        asignados[bus_i] = (taller_t, franja_s)

    # 3. Imprimir la solución
    print(f"Valor Objetivo: {obj_val} | Variables: {num_vars} | Restricciones: {num_restr}\n")

    print("Asignaciones (Autobús -> Franja):")
    if asignados:
        for bus in sorted(asignados.keys()):
            taller, franja = asignados[bus]
            print(f"  - Autobús {bus} asignado a franja {franja} del taller {taller}")
    else:
        print("  - Ningún autobús asignado.")
            
def main():

    # 1. Validación de argumentos de entrada
    if len(sys.argv) != 3:
        print("Error en el formato: ./gen-2.py <fichero-entrada> <fichero-salida.dat>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    dat_file = sys.argv[2]
    mod_file = "parte-2-2.mod"

    if not os.path.exists(mod_file):
        print(f"Error: No existe la ruta del fichero modelo '{mod_file}'", file=sys.stderr)
        sys.exit(1)

    # 2. Leer y procesar el fichero de entrada
    try:
        with open(input_file, 'r') as f:
            n, m, u = map(int, f.readline().strip().split())

            C =[]
            for elem in range (m):
                C.append(list(map(int, f.readline().strip().split())))
            
            O = []
            for _ in range(u):
                O.append(list(map(int, f.readline().strip().split())))

        if len(C) != m or any(len(row) != m for row in C):
            raise ValueError(f"Matriz C debe ser {m}x{m}")
        if len(O) != u or any(len(row) != n for row in O):
            raise ValueError(f"Matriz O debe ser {u}x{n}")
    
    except FileNotFoundError:
        print(f"Error: Fichero de entrada '{input_file}' no encontrado", file=sys.stderr)
        sys.exit(1)
    except(ValueError, IndexError):
        print(f"Error: Formato incorrecto en el fichero de entrada '{input_file}'", file=sys.stderr)
        sys.exit(1)
    
    # 3. Generar el fichero de salida (.dat)
    if not generar_fichero_dat(n, m, u, C, O, dat_file):
        sys.exit(1)
    
    # 4. Resolver el problema con GLPK
    resolver_problema(mod_file, dat_file)

if __name__ == "__main__":
    main()

