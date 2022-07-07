"""
Use of GEKPLS
-------------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.surrogate_models import GEKPLS
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
# | Training of smt model for GEKPLS

n_comp = 2
sm_gekpls = GEKPLS(
                    theta0=[1e-2] * n_comp,
                    xlimits=fun.xlimits,
                    extra_points=1,
                    print_prediction=False,
                    n_comp=n_comp,
                    )
sm_gekpls.set_training_values(xt, yt[:, 0][:,np.newaxis])
    
for i in range(2):
   sm_gekpls.set_training_derivatives(xt, yt[:, 1 + i].reshape((yt.shape[0], 1)), i)
sm_gekpls.train()


# %%
# | Creation of OpenTurns PythonFunction for prediction

otgekpls = otsmt.smt2ot(sm_gekpls)
otgekplsprediction = otgekpls.getPredictionFunction()
otgekplsvariances = otgekpls.getConditionalVarianceFunction()
otgekplsfirstderivatives = otgekpls.getPredictionDerivativesFunction(0)
otgekplssecondderivatives = otgekpls.getPredictionDerivativesFunction(1)

print('Predicted values by GEKPLS:',otgekplsprediction(xv))    
print('Predicted variances values by GEKPLS:',otgekplsvariances(xv))    
print('Predicted mean first derivatives by GEKPLS:',otgekplsfirstderivatives(xv))    
print('Predicted mean second derivatives by GEKPLS:',otgekplssecondderivatives(xv))        