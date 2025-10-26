# Conjuntos y parámetros
set FRANJA;     # s1..sn
set AUTOBUS;    # a1..am
set TALLER;     # t1..tu

param C{AUTOBUS, AUTOBUS};         # c_ij: pasajeros que usan ambos autobuses i y j
param O{FRANJA, TALLER}, binary;   # o_st: 1 si la franja s está disponible en taller t

# Variables de decisión

# x[i,t,s] = 1 si el autobús i se asigna a la franja s del taller t
var x{i in AUTOBUS, t in TALLER, s in FRANJA}, binary;

# z[i,s] = 1 si el autobús i está asignado a la franja s (en cualquier taller)
var z{i in AUTOBUS, s in FRANJA}, binary;

# y[i,j,s] = 1 si los autobuses i y j están asignados a la misma franja s (aunque en talleres distintos)
var y{i in AUTOBUS, j in AUTOBUS, s in FRANJA}, binary;

# Restricciones

# Disponibilidad: solo se pueden asignar franjas disponibles
s.t. RDisponibilidad {i in AUTOBUS, t in TALLER, s in FRANJA}: x[i,t,s] <= O[s,t];

# Capacidad: cada (taller, franja) solo puede atender a un autobús
s.t. Un_autobus_Maximo {t in TALLER, s in FRANJA}: sum {i in AUTOBUS} x[i,t,s] <= 1;

# Cada autobús se asigna exactamente una vez (a alguna franja de algún taller)
s.t. Siempre_Asignado {i in AUTOBUS}: sum {t in TALLER, s in FRANJA} x[i,t,s] = 1;

# Definición de z[i,s]: se activa si el autobús i usa la franja s en cualquier taller
s.t. Autobus_Franja {i in AUTOBUS, s in FRANJA}: z[i,s] = sum {t in TALLER} x[i,t,s];

# Definición de y[i,j,s]: se activa si ambos autobuses i y j están en la misma franja s
s.t. RY1 {i in AUTOBUS, j in AUTOBUS, s in FRANJA: j > i}: y[i,j,s] <= z[i,s];

s.t. RY2 {i in AUTOBUS, j in AUTOBUS, s in FRANJA: j > i}: y[i,j,s] <= z[j,s];

s.t. RY3 {i in AUTOBUS, j in AUTOBUS, s in FRANJA: j > i}: y[i,j,s] >= z[i,s] + z[j,s] - 1;

# Función objetivo

# Minimizar el número total de pasajeros que se ven afectados
# (es decir, autobuses que coinciden en misma franja pero en talleres distintos)
minimize CosteTotal: sum {i in AUTOBUS, j in AUTOBUS, s in FRANJA: j > i} C[i,j] * y[i,j,s];


