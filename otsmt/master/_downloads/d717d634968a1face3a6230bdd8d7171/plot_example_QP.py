"""
Use of Second-order polynomial approximation
--------------------------------------------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.surrogate_models import QP
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
# | Training of smt model for Second-order polynomial approximation

sm_qp = QP()
sm_qp.set_training_values(xt, yt[:,0])
sm_qp.train() 

# %%
# | Creation of OpenTurns PythonFunction for prediction

otqp =  otsmt.smt2ot(sm_qp)
otqpprediction = otqp.getPredictionFunction()
print('Predicted values by QP:',otqpprediction(xv))