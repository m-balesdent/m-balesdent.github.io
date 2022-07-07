"""
Use of KPLS
-----------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.surrogate_models import KPLS
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
# | Training of smt model for KPLS

sm_kpls = KPLS(theta0=[1e-2])
sm_kpls.set_training_values(xt, yt[:,0])
sm_kpls.train() 

# %%
# | Creation of OpenTurns PythonFunction for prediction

otkpls =  otsmt.smt2ot(sm_kpls)
otkplsprediction = otkpls.getPredictionFunction()
otkplsvariances = otkpls.getConditionalVarianceFunction()
otkplsfirstderivatives = otkpls.getPredictionDerivativesFunction(0)
otkplssecondderivatives = otkpls.getPredictionDerivativesFunction(1)

print('Predicted values by KPLS:',otkplsprediction(xv))    
print('Predicted variances values by KPLS:',otkplsvariances(xv))    
print('Predicted mean first derivatives by KPLS:',otkplsfirstderivatives(xv))    
print('Predicted mean second derivatives by KPLS:',otkplssecondderivatives(xv))      