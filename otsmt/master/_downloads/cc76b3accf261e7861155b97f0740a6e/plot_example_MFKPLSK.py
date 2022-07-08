"""
Use of Multi-Fidelity Kriging Partial Least Squares K
-----------------------------------------------------
"""

# %%

from smt.applications import MFKPLSK,NestedLHS
import numpy as np
import otsmt
import openturns as ot
# %%
# | Definition of Initial data

       
# Construction of the DOE
# low fidelity model
def lf_function(x):

    return (
        0.5 * ((x * 6 - 2) ** 2) * np.sin((x * 6 - 2) * 2)
        + (x - 0.5) * 10.0
        - 5
    )

# high fidelity model
def hf_function(x):

    return ((x * 6 - 2) ** 2) * np.sin((x * 6 - 2) * 2)

# Problem set up
xlimits = np.array([[0.0, 1.0]])
xdoes = NestedLHS(nlevel=2, xlimits=xlimits, random_state=0)
xt_c, xt_e = xdoes(7)

# Evaluate the HF and LF functions
yt_e = hf_function(xt_e)
yt_c = lf_function(xt_c)

xv_e = ot.Sample([[0.1],[0.5]])    
    
# %%
# | Training of smt model for MFKPLSK

# choice of number of PLS components
ncomp = 1
sm_mfkplsk = MFKPLSK(n_comp=ncomp, theta0=ncomp * [1.0])

# low-fidelity dataset names being integers from 0 to level-1
sm_mfkplsk.set_training_values(xt_c, yt_c, name=0)
# high-fidelity dataset without name
sm_mfkplsk.set_training_values(xt_e, yt_e)

# train the model
sm_mfkplsk.train()

# %%
# | Creation of OpenTurns PythonFunction for prediction

otmfkplsk = otsmt.smt2ot(sm_mfkplsk)
otmfkplskprediction = otmfkplsk.getPredictionFunction()
otmfkplskpvariances = otmfkplsk.getConditionalVarianceFunction()
otmfkplskgradient = otmfkplsk.getPredictionDerivativesFunction()

print('Predicted values by MFKPLSK:',otmfkplskprediction(xv_e))    
print('Predicted variances values by MFKPLSK:',otmfkplskpvariances(xv_e))    
print('Predicted mean derivatives by MFKPLSK:',otmfkplskgradient(xv_e)) 