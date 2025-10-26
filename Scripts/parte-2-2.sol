Problem:    parte
Rows:       36
Columns:    18 (18 integer, 18 binary)
Non-zeros:  76
Status:     INTEGER EMPTY
Objective:  CosteTotal = 0 (MINimum)

   No.   Row name        Activity     Lower bound   Upper bound
------ ------------    ------------- ------------- -------------
     1 RDisponibilidad[1,1,1]
                                   0                           1 
     2 RDisponibilidad[1,1,2]
                                   0                           1 
     3 RDisponibilidad[2,1,1]
                                   0                           1 
     4 RDisponibilidad[2,1,2]
                                   0                           1 
     5 RDisponibilidad[3,1,1]
                                   0                           1 
     6 RDisponibilidad[3,1,2]
                                   0                           1 
     7 Un_autobus_Maximo[1,1]
                                   0                           1 
     8 Un_autobus_Maximo[1,2]
                                   0                           1 
     9 Siempre_Asignado[1]
                                   0             1             = 
    10 Siempre_Asignado[2]
                                   0             1             = 
    11 Siempre_Asignado[3]
                                   0             1             = 
    12 Autobus_Franja[1,1]
                                   0            -0             = 
    13 Autobus_Franja[1,2]
                                   0            -0             = 
    14 Autobus_Franja[2,1]
                                   0            -0             = 
    15 Autobus_Franja[2,2]
                                   0            -0             = 
    16 Autobus_Franja[3,1]
                                   0            -0             = 
    17 Autobus_Franja[3,2]
                                   0            -0             = 
    18 RY1[1,2,1]                  0                          -0 
    19 RY1[1,2,2]                  0                          -0 
    20 RY1[1,3,1]                  0                          -0 
    21 RY1[1,3,2]                  0                          -0 
    22 RY1[2,3,1]                  0                          -0 
    23 RY1[2,3,2]                  0                          -0 
    24 RY2[1,2,1]                  0                          -0 
    25 RY2[1,2,2]                  0                          -0 
    26 RY2[1,3,1]                  0                          -0 
    27 RY2[1,3,2]                  0                          -0 
    28 RY2[2,3,1]                  0                          -0 
    29 RY2[2,3,2]                  0                          -0 
    30 RY3[1,2,1]                  0            -1               
    31 RY3[1,2,2]                  0            -1               
    32 RY3[1,3,1]                  0            -1               
    33 RY3[1,3,2]                  0            -1               
    34 RY3[2,3,1]                  0            -1               
    35 RY3[2,3,2]                  0            -1               
    36 CosteTotal                  0                             

   No. Column name       Activity     Lower bound   Upper bound
------ ------------    ------------- ------------- -------------
     1 x[1,1,1]     *              0             0             1 
     2 x[1,1,2]     *              0             0             1 
     3 x[2,1,1]     *              0             0             1 
     4 x[2,1,2]     *              0             0             1 
     5 x[3,1,1]     *              0             0             1 
     6 x[3,1,2]     *              0             0             1 
     7 z[1,1]       *              0             0             1 
     8 z[1,2]       *              0             0             1 
     9 z[2,1]       *              0             0             1 
    10 z[2,2]       *              0             0             1 
    11 z[3,1]       *              0             0             1 
    12 z[3,2]       *              0             0             1 
    13 y[1,2,1]     *              0             0             1 
    14 y[1,2,2]     *              0             0             1 
    15 y[1,3,1]     *              0             0             1 
    16 y[1,3,2]     *              0             0             1 
    17 y[2,3,1]     *              0             0             1 
    18 y[2,3,2]     *              0             0             1 

Integer feasibility conditions:

KKT.PE: max.abs.err = 0.00e+00 on row 0
        max.rel.err = 0.00e+00 on row 0
        High quality

KKT.PB: max.abs.err = 1.00e+00 on row 9
        max.rel.err = 5.00e-01 on row 9
        SOLUTION IS INFEASIBLE

End of output
