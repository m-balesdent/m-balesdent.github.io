"""
Use of Regularized minimal-energy tensor-product splines
--------------------------------------------------------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.surrogate_models import RMTB
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
# | Training of smt model for Regularized minimal-energy tensor-product splines

sm_rmtb = RMTB(
xlimits=fun.xlimits,
order=4,
num_ctrl_pts=20,
energy_weight=1e-15,
regularization_weight=0.0,
)
sm_rmtb.set_training_values(xt, yt[:,0])
sm_rmtb.train()

# %%
# | Creation of OpenTurns PythonFunction for prediction

otrmtb =  otsmt.smt2ot(sm_rmtb)
otrmtbprediction = otrmtb.getPredictionFunction()
print('Predicted values by RMTB:',otrmtbprediction(xv))