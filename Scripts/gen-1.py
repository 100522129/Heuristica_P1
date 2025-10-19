import sys
import os
import subprocess

def generar_fichero_dat(n, m, k_d, k_p, distancias, pasajeros, path):
    """
    Genera el fichero de salida (.dat) con el formato que requiere GLPK
    """
    try:
        with open (path, 'w') as f:
            f.write("# Fichero de datos generado por gen-1.py\n\n")

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
        
        print(f"Fichero de datos generado '{path}' correctamente")
        return True
    except IOError as e:
        print(f"Error al escribir el fichero de datos '{path}': {e}", file=sys.stderr)
        return False

def resolver_problema(mod_file, dat_file):
    """
    Invoca al solver GLPK y muestra la salida de la solución
    """
    command = ["glpsol", "--model", mod_file, "--data", dat_file]

    try:
        # Ejecuta el solver y captura su salida
        result = subprocess.run(command, capture_output=True, text=True, check=True)
    
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"Error ejecutando GLPK: {e}", file=sys.stderr)
            
def main():

    # 1. Validación de argumentos de entrada
    if len(sys.argv) != 3:
        print("Error en el formato: ./gen-1.py <fichero-entrada> <fichero-salida.dat>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    mod_file = "parte-2-1.mod"

    if not os.path.exists(mod_file):
        print()
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
            print()
            sys.exit(1)
    
    except FileNotFoundError:
        print()
        sys.exit(1)
    except(ValueError, IndexError):
        print()
        sys.exit(1)
    
    # 3. Generar el fichero de salida (.dat)
    if not generar_fichero_dat(n, m, k_d, k_p, distancias, pasajeros, output_file):
        sys.exit(1)
    
    # 4. Resolver el problema con GLPK
    resolver_problema()

