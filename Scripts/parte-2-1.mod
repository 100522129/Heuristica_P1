set FRANJAS;    # Conjunto de franjas s1..sn
set AUTOBUSES;   # Conjunto de autobuses a1..am

param k_d;      # coste euros por km si se asigna (constante)
param k_p;      # penalización euros por pasajero si no se asigna (constante)

param d{AUTOBUSES};   # distancia d_j para cada autobús
param p{AUTOBUSES};      # pasajeros p_j para cada autobús

# Variable binaria de decisión:
# x[j,s] = 1 si el autobús j se asigna a la franja s, si no se coge la franja al autobús entonces 0
var x{j in AUTOBUSES, s in FRANJAS}, binary;

# y[j] = 1 si el autobús j no se asigna a ninguna franja, en caso contrario 0
var y{j in AUTOBUSES}, binary;

# Restricciones:

#El taller en cada franja solo puede atender a un autobús como mucho
s.t. RFranja {s in FRANJAS}: 
        sum {j in AUTOBUSES} x[j,s] <= 1;

#Cada autobús puede ocupar como máximo una franja, o puede ser que no ocupe ninguna (pondremos penalización por pasajero)
s.t. RAutobus {j in AUTOBUSES}: 
        (sum {s in FRANJAS} x[j,s]) + y[j] = 1;

# Función objetivo: minimizar el coste total:
minimize CosteTotal: 
    # 1. Coste total de autobuses ASIGNADOS
    sum {j in AUTOBUSES, s in FRANJAS} (k_d * d[j] * x[j,s])
    
    # 2. Coste total de autobuses NO ASIGNADOS
    + sum {j in AUTOBUSES} (k_p * p[j] * y[j]);

end;