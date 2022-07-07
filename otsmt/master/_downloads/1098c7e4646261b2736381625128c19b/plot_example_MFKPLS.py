"""
Use of Multi-Fidelity Kriging Partial Least Squares
---------------------------------------------------
"""

# %%

from smt.applications import MFKPLS,NestedLHS
import numpy as np
import otsmt


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

xv_c, xv_e = xdoes(10)
    
# %%
# | Training of smt model for MFKPLS

ncomp = 1
sm_mfkpls = MFKPLS(n_comp=ncomp, theta0=ncomp * [1.0])

# low-fidelity dataset names being integers from 0 to level-1
sm_mfkpls.set_training_values(xt_c, yt_c, name=0)
# high-fidelity dataset without name
sm_mfkpls.set_training_values(xt_e, yt_e)

# train the model
sm_mfkpls.train()

# %%
# | Creation of OpenTurns PythonFunction for prediction

otmfkpls = otsmt.smt2ot(sm_mfkpls)
otmfkplsprediction = otmfkpls.getPredictionFunction()
otmfkplspvariances = otmfkpls.getConditionalVarianceFunction()
otmfkplsfirstderivatives = otmfkpls.getPredictionDerivativesFunction(0)

print('Predicted values by MFKPLS:',otmfkplsprediction(xv_e))    
print('Predicted variances values by MFKPLS:',otmfkplspvariances(xv_e))    
print('Predicted mean first derivatives by MFKPLS:',otmfkplsfirstderivatives(xv_e)) 