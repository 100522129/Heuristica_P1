import sys
import os
import re
import subprocess

def resolver_problema(mod_file, dat_file):
    """
    Invoca al solver GLPK y muestra la salida de la solución
    """
    command = ["glpsol", "--model", mod_file, "--data", dat_file]

    # 1. Ejecuta el solver y captura su salida
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
    
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"Error ejecutando GLPK: {e}", file=sys.stderr)
        return
    
    # 2. Comprobar que existe solución óptima 
    patron_exito = re.compile(r"(INTEGER )?OPTIMAL SOLUTION FOUND", re.IGNORECASE)

    # "Si no coincide, es porque es infactible"
    if not patron_exito.search(result.stdout):
        print("Error: El problema es infactible", file=sys.stderr)
        return
    
    # 3. Parsear la solución
    obj_val = ""
    num_restr = ""
    num_vars = ""
    asignados = {} # Diccionario para {bus: franja}
    no_asignados = [] # Lista para [bus]

    if m := re.search(r"Objective:.*?= *([\d\.]+)", output):
        obj_val = m.group(1) # group(1) es el número capturado

    if m := re.search(r"(\d+) rows, +(\d+) columns,", output):
        num_restr = m.group(1)
        num_vars = m.group(2)
    
    for line in output.splitlines():
        # 2.3 Busca líneas en las que aparecen variables
        parts = line.split()

        if len(parts) < 4: # Estas líneas que busca tienen mínimo 4 partes, si tienen menos pasa a la siguiente línea
            continue

        col_name = parts[1] # Almacena x[bus, franja]

        if col_name.startswith("x[") or col_name.startswith("y["):
            var_value = float(parts[3])

            if (var_value  < 1.0): # Si la variable no vale 1 no se almacena
                continue

            if col_name.startswith("x["):
                indices = col_name[2:-1].split(',')
                bus = int(indices[0])
                franja = int(indices[1])
                asignados[bus] = franja
                
            
            elif col_name.startswith("y["):
                bus = int(col_name[2:-1])
                no_asignados.append(bus)
        
    # 4. Imprimir la solución
    print(f"Valor Objetivo: {obj_val} | Variables de decisión: {num_vars} | Restricciones: {num_restr}\n")

    print("Asignaciones (Autobús -> Franja):")
    if asignados:
        for bus in sorted(asignados.keys()):
            print(f"  - Autobús {bus} asignado a franja {asignados[bus]}")
    else:
        print("  - Ningún autobús asignado.")

    print("\nAutobuses No Asignados:")
    if no_asignados:
        for bus in sorted(no_asignados):
            print(f"  - Autobús {bus} no asignado")
    else:
        print("  - Todos los autobuses fueron asignados.")