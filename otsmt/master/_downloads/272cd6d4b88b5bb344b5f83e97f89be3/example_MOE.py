"""
Use of Mixture of Experts
-------------------------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.applications import MOE
import numpy as np
import otsmt


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
       
xv= sampling(10)
    
# %%
# | Training of smt model for  Mixture of Experts

moe = MOE(n_clusters=2)
moe.set_training_values(xt, yt[:,0][:,np.newaxis])
moe.train()

# %%
# | Creation of OpenTurns PythonFunction for prediction

otmoe = otsmt.smt2ot(moe)
otmoeprediction = otmoe.getPredictionFunction()
print('Predicted values by MOE:',otmoeprediction(xv))   
