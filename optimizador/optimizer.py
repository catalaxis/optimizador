import pandas as pd
import numpy as np
from scipy.optimize import linprog

class Optimizer:
    ## Resuelve el siguiente problema:
    
    ## Función objetivo: MAX Pa * Xa + Pb * Xb // Maximizar utilidad
    ## SA: 
    #   Ta1 * Xa + Tb1 * Xb <= TM1 // Sujeto a la restricción de tiempo para la máquina 1
    #   Ta2 * Xa + Tb2 * Xb <= TM2 // Sujeto a la restricción de tiempo para la máquina 2
    #   Xa >= 0, Xb >= 0 // No negatividad de las variables

    ## Variables:
    #   Ta1: Tiempo requerido para producir una unidad del producto A en la máquina 1
    #   Ta2: Tiempo requerido para producir una unidad del producto A en la máquina 2
    #   TM1: Tiempo total disponible para la máquina 1
    #   TM2: Tiempo total disponible para la máquina 2
    #   Pa: Precio/Utilidad por unidad del producto A
    #   Pb: Precio/Utilidad por unidad del producto B

    ## No se menciona la granularidad de los productos, por lo que asumimos que se pueden producir en cualquier cantidad.
    ## Este es un problema de optimización continua.

    ## Esto se puede resolver de muchas maneras, pero aquí utilizaremos un enfoque simple de programación lineal con Scipy y Numpy.
    ## La mayoría de las veces solo uso Numpy y POT,
    ## Pytorch o Tensorflow para problemas más complejos.
   
    def __init__(self, Ta1, Ta2,Tb1,Tb2, TM1, TM2, Pa, Pb):

        self.Ta1, self.Ta2 = Ta1, Ta2  # Tiempo requerido para productos A
        self.Tb1, self.Tb2 = Tb1, Tb2  # Tiempo requerido para productos B
        self.TM1, self.TM2 = TM1, TM2  # Tiempo total disponible para las máquinas 1 y 2
        self.Pa, self.Pb = Pa, Pb  # Precio/Utilidad por unidad de los productos A y B

        self.result = None  # Máximo resultado de f
        self.Xa, self.Xb = None, None  # Variables para almacenar las cantidades de productos A y B producidas
    
    def solve(self):
        # Coeficientes de la función objetivo
        c = np.array([-self.Pa, -self.Pb])

        # Coeficientes de las restricciones de desigualdad
        # Representamos las restricciones como Ax <= b
        A = np.array([
            [self.Ta1, self.Tb1],
            [self.Ta2, self.Tb2]
        ])

        # Límites de las restricciones
        # TM1 y TM2 son los límites para las máquinas 1 y 2 respectivamente
        b = np.array([self.TM1, self.TM2])

        # Límites para las variables (Xa, Xb)
        x0_bounds = (0, None)  # Xa >= 0
        x1_bounds = (0, None)  # Xb >= 0

        # Resolvemos el problema de programación lineal
        # Usamos linprog de scipy para maximizar la función objetivo
        self.result = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method='highs')
        if self.result.success:
            self.Xa, self.Xb = self.result.x
            return self.Xa, self.Xb, -self.result.fun
        else:
            raise ValueError("Optimization failed: " + self.result.message)
