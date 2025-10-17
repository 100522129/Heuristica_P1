set FRANJA;    # Conjunto de franjas s1..sn
set AUTOBUS;   # Conjunto de autobuses a1..am

param k_d;      # coste euros por km si se asigna (constante)
param k_p;      # penalización euros por pasajero si no se asigna (constante)

param DIST{AUTOBUS};   # distancia d_j para cada autobús
param P{AUTOBUS};      # pasajeros p_j para cada autobús

# Variable binaria de decisión:
# x[j,s] = 1 si el autobús j se asigna a la franja s, si no se coge la franja al autobús entonces 0
var x{j in AUTOBUS, s in FRANJA}, binary;

# Restricciones:

#El taller en cada franja solo puede atender a un autobús como mucho
s.t. RFranja {s in FRANJA}: sum {j in AUTOBUS} x[j,s] <= 1;

#Cada autobús puede ocupar como máximo una franja, o puede ser que no ocupe ninguna (pondremos penalización por pasajero)
s.t. RAutobus {j in AUTOBUS}: sum {s in FRANJA} x[j,s] <= 1;

# Función objetivo: minimizar el coste total:
minimize CosteTotal: sum {j in AUTOBUS} (
        k_p * P[j] * (1 - sum {s in FRANJA} x[j,s])
      + k_d * DIST[j] * (sum {s in FRANJA} x[j,s])
    );

# Resolver
solve;

# Mostrar resultados
display x;
display CosteTotal;

end;
