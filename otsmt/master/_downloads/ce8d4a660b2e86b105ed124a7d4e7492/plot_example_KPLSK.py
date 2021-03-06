"""
Use of KPLSK
------------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.surrogate_models import KPLSK
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
# | Training of smt model for KPLSK

sm_kplsk = KPLSK(theta0=[1e-2])
sm_kplsk.set_training_values(xt, yt[:,0])
sm_kplsk.train() 


# %%
# | Creation of OpenTurns PythonFunction for prediction

otkplsk = otsmt.smt2ot(sm_kplsk)
otkplskprediction = otkplsk.getPredictionFunction()
otkplskvariances = otkplsk.getConditionalVarianceFunction()
otkplskgradient = otkplsk.getPredictionDerivativesFunction()

print('Predicted values by KPLSK:',otkplskprediction(xv))    
print('Predicted variances values by KPLSK:',otkplskvariances(xv))    
print('Prediction derivatives derivatives by KPLSK:',otkplskgradient(xv))
