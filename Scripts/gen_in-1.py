#!/usr/bin/env python3
import subprocess
import time
import os
import random
import matplotlib.pyplot as plt  # <-- 1. Importamos la librería

# --- Configuración ---
SCRIPT_A_PROBAR = "gen-1.py" 

# (n_franjas, m_autobuses)
CASOS_GEN1 = [
    (5, 10),
    (10, 20),
    (15, 30),
    (20, 40),
    (25, 50),
    (50, 100),
    (75, 150),
    (100, 200)
    # Añade más casos si quieres una gráfica más detallada
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
eje_x_tamanos = []  # <-- 2. Lista para el eje X (guardará 'm')
eje_y_tiempos = []  # <-- 3. Lista para el eje Y (guardará el tiempo)

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
        subprocess.run(comando, check=True, capture_output=True, text=True)
        
        end_time = time.perf_counter()
        duracion = end_time - start_time
        
        print(f"Caso (n={n}, m={m}): {duracion:.4f} segundos")

        # --- 4. Guardamos los datos para la gráfica ---
        eje_x_tamanos.append(m)
        eje_y_tiempos.append(duracion)

    except subprocess.CalledProcessError as e:
        print(f"Caso (n={n}, m={m}): FALLÓ")
    except FileNotFoundError:
        print(f"Error: No se encuentra '{SCRIPT_A_PROBAR}'.")
        break
        
    os.remove(input_file)
    if os.path.exists(output_dat):
        os.remove(output_dat)

print("--- Pruebas finalizadas ---")

# -----------------------------------------------------------------
# --- 5. Mostrar la gráfica ---
# -----------------------------------------------------------------
if eje_x_tamanos: # Solo si tenemos datos
    print("Mostrando gráfica...")
    plt.figure(figsize=(8, 5))
    plt.plot(eje_x_tamanos, eje_y_tiempos, 'o-') # 'o-' = puntos y líneas
    
    plt.title(f"Rendimiento de {SCRIPT_A_PROBAR}")
    plt.xlabel("Número de Autobuses (m)")
    plt.ylabel("Tiempo (segundos)")
    plt.grid(True) # Pone una rejilla
    
    plt.show() # <-- ESTO ABRE LA VENTANA
else:
    print("No se generaron datos, no se puede mostrar la gráfica.")