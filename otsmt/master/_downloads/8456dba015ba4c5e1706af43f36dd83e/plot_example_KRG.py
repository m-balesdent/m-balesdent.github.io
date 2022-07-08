"""
Use of Kriging
--------------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.surrogate_models import KRG
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
# | Training of smt model for Kriging

sm_krg = KRG(theta0=[1e-2])
sm_krg.set_training_values(xt, yt[:,0])
sm_krg.train()

# %%
# | Creation of OpenTurns PythonFunction for prediction

otkrg =  otsmt.smt2ot(sm_krg)
otkrgprediction = otkrg.getPredictionFunction()
otkrgvariances = otkrg.getConditionalVarianceFunction()
otkrggradient = otkrg.getPredictionDerivativesFunction()

print('Predicted values by KRG:',otkrgprediction(xv))    
print('Predicted variances values by KRG:',otkrgvariances(xv))    
print('Prediction derivatives by KRG:',otkrggradient(xv))    
