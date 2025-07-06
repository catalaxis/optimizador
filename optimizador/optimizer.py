import pandas as pd
import numpy as np
from scipy.optimize import linprog

class Optimizer:
    ## Solves the optimization problem
    
    ## Target fun: MAX Pa * Xa + Pb * Xb // Maximize profit
    ## SA: 
    #   Ta1 * Xa + Tb1 * Xb <= TM1 // Subject to time constraint for machine 1
    #   Ta2 * Xa + Tb2 * Xb <= TM2 // Subject to time constraint for machine 2
    #   Xa >= 0, Xb >= 0 // Non-negativity constraints

    ## Variables:
    #   Ta1: Amount of product A to produce
    #   Ta2: Amount of product B to produce
    #   TM1: Total time available for machine 1
    #   TM2: Total time available for machine 2
    #   Pa: Price/Profit per unit of product A
    #   Pb: Price/Profit per unit of product B

    ## There is no mention of the granularity of the products, so we assume they can be produced in any amount.
    ## This is a continuous optimization problem.

    ## This can be solved in many ways, but here we will use a simple linear programming approach with Scipy and Numpy.
    ## Most of the time I just use Numpy and POT,
    ## Pytorch or tensorflow for more complex problems.
   
    def __init__(self, Ta1, Ta2,Tb1,Tb2, TM1, TM2, Pa, Pb):

        self.Ta1, self.Ta2 = Ta1, Ta2  # Time required for products A
        self.Tb1, self.Tb2 = Tb1, Tb2  # Time required for products B
        self.TM1, self.TM2 = TM1, TM2  # Total time available for machines 1 and 2
        self.Pa, self.Pb = Pa, Pb  # Prices/Profits per unit of products A and B
        
        self.result = None # Max result of f
        self.Xa, self.Xb = None, None  # Variables to hold the amounts of products A and B produced
    
    def solve(self):
        # Objective function coefficients
        c = np.array([-self.Pa, -self.Pb])

        # Coefficients for the inequality constraints
        A = np.array([
            [self.Ta1, self.Tb1],
            [self.Ta2, self.Tb2]
        ])

        # Right-hand side of the inequality constraints
        b = np.array([self.TM1, self.TM2])

        # Bounds for the variables (Xa, Xb)
        x0_bounds = (0, None)  # Xa >= 0
        x1_bounds = (0, None)  # Xb >= 0

        # Solve the linear programming problem
        self.result = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds], method='highs')
        if self.result.success:
            self.Xa, self.Xb = self.result.x
            return self.Xa, self.Xb, -self.result.fun
        else:
            raise ValueError("Optimization failed: " + self.result.message)
