"""
Use of KPLS
-----------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.surrogate_models import KPLSK
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
# | Training of smt model for KPLSK

sm_kplsk = KPLSK(theta0=[1e-2])
sm_kplsk.set_training_values(xt, yt[:,0])
sm_kplsk.train() 


# %%
# | Creation of OpenTurns PythonFunction for prediction

otkplsk = otsmt.smt2ot(sm_kplsk)
otkplskprediction = otkplsk.getPredictionFunction()
otkplskvariances = otkplsk.getConditionalVarianceFunction()
otkplskfirstderivatives = otkplsk.getPredictionDerivativesFunction(0)
otkplsksecondderivatives = otkplsk.getPredictionDerivativesFunction(1)

print('Predicted values by KPLSK:',otkplskprediction(xv))    
print('Predicted variances values by KPLSK:',otkplskvariances(xv))    
print('Predicted mean first derivatives by KPLSK:',otkplskfirstderivatives(xv))    
print('Predicted mean second derivatives by KPLSK:',otkplsksecondderivatives(xv))         