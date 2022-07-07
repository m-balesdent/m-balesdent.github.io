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
# | Training of smt model for Kriging

sm_krg = KRG(theta0=[1e-2])
sm_krg.set_training_values(xt, yt[:,0])
sm_krg.train()

# %%
# | Creation of OpenTurns PythonFunction for prediction

otkrg =  otsmt.smt2ot(sm_krg)
otkrgprediction = otkrg.getPredictionFunction()
otkrgvariances = otkrg.getConditionalVarianceFunction()
otkrgfirstderivatives = otkrg.getPredictionDerivativesFunction(0)
otkrgsecondderivatives = otkrg.getPredictionDerivativesFunction(1)

print('Predicted values by KRG:',otkrgprediction(xv))    
print('Predicted variances values by KRG:',otkrgvariances(xv))    
print('Predicted mean first derivatives by KRG:',otkrgfirstderivatives(xv))    
print('Predicted mean second derivatives by KRG:',otkrgsecondderivatives(xv))    