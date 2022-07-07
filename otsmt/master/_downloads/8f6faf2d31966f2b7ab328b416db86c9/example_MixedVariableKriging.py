"""
Use of Mixed Variable Kriging
-----------------------------
"""

# %%

from smt.applications.mixed_integer import MixedIntegerContext, FLOAT, ORD, ENUM
import numpy as np
from smt.surrogate_models import KRG

import otsmt
from smt.sampling_methods import LHS, Random


# %%
# | Definition of Initial data

       
xtypes = [ORD, FLOAT, (ENUM, 4)]
xlimits = [[0, 5], [0.0, 4.0], ["blue", "red", "green", "yellow"]]

def ftest(x):
    return (x[:, 0] * x[:, 0] + x[:, 1] * x[:, 1]) * (x[:, 2] + 1)

# context to create consistent DOEs and surrogate
mixint = MixedIntegerContext(xtypes, xlimits)

# DOE for training
lhs = mixint.build_sampling_method(LHS, criterion="ese")

num = mixint.get_unfolded_dimension() * 5
print("DOE point nb = {}".format(num))
xt = lhs(num)
yt = ftest(xt)

# DOE for validation
rand = mixint.build_sampling_method(Random)
xv = rand(50)
yv = ftest(xv)    
    
# %%
# | Training of smt model for Mixed variables 

sm_mixed = mixint.build_surrogate_model(KRG())
sm_mixed.set_training_values(xt, yt)
sm_mixed.train()

# %%
# | Creation of OpenTurns PythonFunction for prediction

otmixed = otsmt.smt2ot(sm_mixed)
otmixedprediction = otmixed.getPredictionFunction()
otmixedvariances = otmixed.getConditionalVarianceFunction()

print('Predicted values by Mixed Integer:',otmixedprediction(xv))    
print('Predicted variances values by Mixed Intege:',otmixedvariances(xv))  