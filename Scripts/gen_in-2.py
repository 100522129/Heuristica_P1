#!/usr/bin/env python3
import subprocess
import time
import os
import random
import matplotlib.pyplot as plt

# --- 1. Configuración (CAMBIADO) ---
SCRIPT_A_PROBAR = "gen-2.py" 

# (n_franjas, m_autobuses, u_talleres)
# Requisito: requiere que n * u >= m
CASOS_GEN2 = [
    # (n = franjas, m = autobuses, u = talleres)
    (20, 1, 4),
    (40, 10, 4),
    (60, 20, 4),
    (80, 30, 4),
    (90, 40, 4),
    (100, 50, 4),
]

# --- 2. Generador de .in (CAMBIADO) ---

def crear_input_gen2(filename, n, m, u):
    """Genera un fichero .in de prueba para gen-2.py"""
    with open(filename, 'w') as f:
        # n, m, u
        f.write(f"{n} {m} {u}\n")
        
        # Matriz C (m x m) - Pasajeros simultáneos (Sigue igual)
        for i in range(m):
            row = [str(random.randint(1, 20)) for _ in range(m)]
            row[i] = "0"
            f.write(" ".join(row) + "\n")
            
        # Matriz O (n x u) - Disponibilidad (0 o 1)
        
        # 1. Crear una lista plana con el mínimo de '1's necesarios
        # Mínimo de slots necesarios = m (autobuses)
        num_slots_totales = n * u
        slots_necesarios = m 
        
        # Rellenar con '1' los slots necesarios y el resto con 0 o 1
        plana = [1] * slots_necesarios + [random.randint(0, 1) for _ in range(num_slots_totales - slots_necesarios)]
        
        # Mezclar la lista para que los '1's no estén siempre al principio
        random.shuffle(plana)
        
        # 2. Escribir la matriz O (n filas de u elementos)
        for s in range(n):
            # Obtener la fila de U elementos de la lista plana
            inicio = s * u
            fin = inicio + u
            row_list = plana[inicio:fin]
            
            f.write(" ".join(map(str, row_list)) + "\n")

# --- Listas para guardar los resultados ---
eje_x_tamanos = []  
eje_y_tiempo = []  

# -----------------------------------------------------------------
# --- 3. Bucle principal de pruebas (CAMBIADO) ---
# -----------------------------------------------------------------
print(f"--- Iniciando pruebas para: {SCRIPT_A_PROBAR} ---")

for n, m, u in CASOS_GEN2: # <-- Cambiado a n, m, u
    
    input_file = f"temp_caso_n{n}_m{m}_u{u}.in" # <-- Nombre de fichero
    output_dat = "temp_caso.dat"

    crear_input_gen2(input_file, n, m, u) # <-- Llamada a la nueva función
    
    start_time = time.perf_counter()
    
   # gen_in-2.py (fragmento del bucle principal)

    try:
        start_time = time.perf_counter()
        
        comando = ["python3", SCRIPT_A_PROBAR, input_file, output_dat]
        
        # Almacena el resultado para poder acceder a la salida (stdout)
        result = subprocess.run(comando, check=True, capture_output=True, text=True)
        
        end_time = time.perf_counter()
        duracion = end_time - start_time
        
        print(f"--- DETALLES DEL CASO (n={n}, m={m}, u={u}) ---")
        
        # AÑADIR ESTO: Imprimir la salida estándar (stdout) del script gen-2.py
        print(result.stdout) 
        
        # AÑADIR ESTO: Si stderr contiene algo, significa un error de gen-2.py
        if result.stderr:
            print("--- ERROR/ADVERTENCIA CAPTURADA (STDERR de gen-2.py) ---")
            print(result.stderr)
        
        print(f"Duración de la resolución: {duracion:.4f} segundos")
        
        eje_x_tamanos.append(m) # Guardamos 'm' (autobuses) para el eje X
        eje_y_tiempo.append(duracion)

    except subprocess.CalledProcessError as e:
        print(f"\nCaso (n={n}, m={m}, u={u}): FALLÓ - Código de error {e.returncode}")
        # Si falla, imprimimos el error de GLPK que está en stderr
        print("ERROR LOG:", e.stderr)
        # ... (resto del except)
        
    os.remove(input_file)
    if os.path.exists(output_dat):
        os.remove(output_dat)

print("--- Pruebas finalizadas ---")

# -----------------------------------------------------------------
# --- 4. Mostrar la gráfica (SIN CAMBIOS) ---
# -----------------------------------------------------------------
if eje_x_tamanos:
    print("Mostrando gráfica...")
    plt.figure(figsize=(8, 5))
    plt.plot(eje_x_tamanos, eje_y_tiempo, 'o-') 
    
    plt.title(f"Rendimiento de {SCRIPT_A_PROBAR}")
    plt.xlabel("Número de Autobuses (m)")
    plt.ylabel("Tiempo (segundos)")
    plt.grid(True)
    
    plt.show()
else:
    print("No se generaron datos, no se puede mostrar la gráfica.")