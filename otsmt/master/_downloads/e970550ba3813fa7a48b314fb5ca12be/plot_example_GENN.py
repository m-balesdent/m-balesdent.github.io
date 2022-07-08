"""
Use of Gradient Enhanced Neural Network Model
---------------------------------------------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.surrogate_models.genn import GENN, load_smt_data

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
# | Training of smt model for Neural Network

genn = GENN()
load_smt_data(
      genn, xt, yt[:,0], yt[:,1:])  # convenience function to read in data that is in SMT format
genn.train()

# %%
# | Creation of OpenTurns PythonFunction for prediction

otgenn =  otsmt.smt2ot(genn)
otgennprediction = otgenn.getPredictionFunction()
otgenngradient = otgenn.getPredictionDerivativesFunction()


print('Predicted values by GENN:',otgennprediction(xv))
print('Predicted mean derivatives by GENN:',otgenngradient(xv))    
