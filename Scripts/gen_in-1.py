#!/usr/bin/env python3
import subprocess
import time
import os
import random
import matplotlib.pyplot as plt

# --- Configuración ---
SCRIPT_A_PROBAR = "gen-1.py" 

# (n_franjas, m_autobuses)
CASOS_GEN1 = [
    (5, 20),    # 15 deben ser penalizados
    (10, 40),   # 30 deben ser penalizados
    (15, 60),   # 45 deben ser penalizados
    (20, 80),   # 60 deben ser penalizados
    (50, 150),  # 100 deben ser penalizados
    (100, 300)  # 200 deben ser penalizados
]

# --- Generador de .in simple (para gen-1.py) ---
def crear_input_gen1(filename, n, m):
    """Genera un fichero .in de prueba para gen-1.py"""
    with open(filename, 'w') as f:
        f.write(f"{n} {m}\n")
        f.write("1.5 75.0\n") # kd y kp fijos
        distancias = [str(random.randint(50, 500)) for _ in range(m)]
        f.write(" ".join(distancias) + "\n")
        pasajeros = [str(random.randint(20, 80)) for _ in range(m)]
        f.write(" ".join(pasajeros) + "\n")

# --- Listas para guardar los resultados ---
eje_x_tamanos = [] # Esta lista ahora guardará 'n'
eje_y_tiempos = []

# -----------------------------------------------------------------
# --- Bucle principal de pruebas ---
# -----------------------------------------------------------------
print(f"--- Iniciando pruebas para: {SCRIPT_A_PROBAR} ---")

for n, m in CASOS_GEN1:
    
    input_file = f"temp_caso_n{n}_m{m}.in"
    output_dat = "temp_caso.dat"

    crear_input_gen1(input_file, n, m)
    
    start_time = time.perf_counter()
    
    try:
        comando = ["python3", SCRIPT_A_PROBAR, input_file, output_dat]
        
        # Ejecutamos y capturamos la salida
        result = subprocess.run(comando, check=True, capture_output=True, text=True)
        
        end_time = time.perf_counter()
        duracion = end_time - start_time
        
        # --- NUEVA IMPRESIÓN ---
        print(f"\n--- DETALLES DEL CASO (n={n}, m={m}) ---")
        # Imprimir la solución completa capturada
        print(result.stdout)
        print(f"Duración de la resolución: {duracion:.4f} segundos")
        # -----------------------

        # CAMBIO 1: Guardar 'n' en el eje X
        eje_x_tamanos.append(n)
        eje_y_tiempos.append(duracion)

    except subprocess.CalledProcessError as e:
        print(f"\nCaso (n={n}, m={m}): FALLÓ - Código de error {e.returncode}")
        # Mostrar el error de infactibilidad o parsing de GLPK
        print("ERROR LOG:", e.stderr) 
    except FileNotFoundError:
        print(f"Error: No se encuentra '{SCRIPT_A_PROBAR}'.")
        break
        
    os.remove(input_file)
    if os.path.exists(output_dat):
        os.remove(output_dat)

print("\n--- Pruebas finalizadas ---")

# -----------------------------------------------------------------
# --- 5. Mostrar la gráfica ---
# -----------------------------------------------------------------
if eje_x_tamanos:
    print("Mostrando gráfica...")
    plt.figure(figsize=(8, 5))
    plt.plot(eje_x_tamanos, eje_y_tiempos, 'o-')
    
    plt.title(f"Rendimiento de {SCRIPT_A_PROBAR}")
    
    # CAMBIO 2: Modificar la etiqueta del eje X
    plt.xlabel("Número de Franjas (n)")
    plt.ylabel("Tiempo (segundos)")
    plt.grid(True)
    
    plt.show()
else:
    print("No se generaron datos, no se puede mostrar la gráfica.")