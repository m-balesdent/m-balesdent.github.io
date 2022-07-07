"""
Use of Inverse Distance Weighting
---------------------------------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.surrogate_models import IDW
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
# | Training of smt model for Inverse Distance Weighting

sm_idw = IDW(p=2)
sm_idw.set_training_values(xt, yt[:,0])
sm_idw.train()  

# %%
# | Creation of OpenTurns PythonFunction for prediction

otidw =  otsmt.smt2ot(sm_idw)
otidwprediction = otidw.getPredictionFunction()
print('Predicted values by IDW:',otidwprediction(xv))