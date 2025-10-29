#!/usr/bin/env python3
import subprocess
import time
import os
import random
import matplotlib.pyplot as plt

# --- 1. Configuración (CAMBIADO) ---
SCRIPT_A_PROBAR = "gen-2.py" 

# (n_franjas, m_autobuses, u_talleres)
# ¡¡IMPORTANTE!! El problema gen-2 requiere que n * u >= m
CASOS_GEN2 = [
    # (n, m, u)
    (5, 10, 2),   # n*u = 10 >= 10
    (10, 20, 2),  # n*u = 20 >= 20
    (10, 30, 3),  # n*u = 30 >= 30
    (10, 40, 4),  # n*u = 40 >= 40
    (10, 50, 5),  # n*u = 50 >= 50
    (20, 100, 5), # n*u = 100 >= 100
    # Añade más casos si quieres
]

# --- 2. Generador de .in (CAMBIADO) ---
def crear_input_gen2(filename, n, m, u):
    """Genera un fichero .in de prueba para gen-2.py"""
    with open(filename, 'w') as f:
        # n, m, u
        f.write(f"{n} {m} {u}\n")
        
        # Matriz C (m x m) - Pasajeros simultáneos
        for i in range(m):
            # cii = 0 (asumimos), cij = cji (simétrica)
            row = [str(random.randint(0, 20)) for _ in range(m)]
            row[i] = "0" # Pasajeros compartidos con uno mismo es 0
            f.write(" ".join(row) + "\n")
            
        # Matriz O (u x n) - Disponibilidad (0 o 1)
        for _ in range(u):
            row = [str(random.randint(0, 1)) for _ in range(n)]
            f.write(" ".join(row) + "\n")

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
    
    try:
        comando = ["python3", SCRIPT_A_PROBAR, input_file, output_dat]
        subprocess.run(comando, check=True, capture_output=True, text=True)
        
        end_time = time.perf_counter()
        duracion = end_time - start_time
        
        print(f"Caso (n={n}, m={m}, u={u}): {duracion:.4f} segundos")

        eje_x_tamanos.append(m) # Guardamos 'm' (autobuses) para el eje X
        eje_y_tiempo.append(duracion)

    except subprocess.CalledProcessError as e:
        print(f"Caso (n={n}, m={m}, u={u}): FALLÓ")
    except FileNotFoundError:
        print(f"Error: No se encuentra '{SCRIPT_A_PROBAR}'.")
        break
        
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