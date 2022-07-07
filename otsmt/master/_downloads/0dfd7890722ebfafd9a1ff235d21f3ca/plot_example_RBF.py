"""
Use of Radial Basis Function
----------------------------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.surrogate_models import RBF
import numpy as np
import otsmt
import openturns as ot


# %%
# | Definition of Initial data

       
# Construction of the DOE
fun = Sphere(ndim=2)
sampling = LHS(xlimits=fun.xlimits, criterion="m")
xt = sampling(40)
yt = fun(xt)
# Compute the gradient
for i in range(2):
    yd = fun(xt, kx=i)
    yt = np.concatenate((yt, yd), axis=1)
       
xv = ot.Sample([[0.1,1.],[1.,2.]])    
    
# %%
# | Training of smt model for Radial Basis Function

sm_rbf = RBF()
sm_rbf.set_training_values(xt, yt[:,0])
sm_rbf.train()

# %%
# | Creation of OpenTurns PythonFunction for prediction

otrbf =  otsmt.smt2ot(sm_rbf)
otrbfprediction = otrbf.getPredictionFunction()
print('Predicted values by RBF:',otrbfprediction(xv))