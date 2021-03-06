"""
Use of Multi-Fidelity Kriging
-----------------------------
"""

# %%

from smt.applications import MFK,NestedLHS
import numpy as np
import otsmt
import matplotlib.pyplot as plt
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
xt_c, xt_e = xdoes(4)

# Evaluate the HF and LF functions
yt_e = hf_function(xt_e)
yt_c = lf_function(xt_c)

xv_e = np.linspace(xlimits[0][0],xlimits[0][1],50)[:,np.newaxis]
yv_e  = hf_function(xv_e)
# %%
# | Training of smt model for  Multi-Fidelity Kriging

sm_mfk = MFK(theta0=xt_e.shape[1] * [1.0])    

# low-fidelity dataset names being integers from 0 to level-1
sm_mfk.set_training_values(xt_c, yt_c, name=0)
# high-fidelity dataset without name
sm_mfk.set_training_values(xt_e, yt_e)
    
# train the model
sm_mfk.train()

# %%
# | Creation of OpenTurns PythonFunction for prediction

otmfk = otsmt.smt2ot(sm_mfk)
otmfkprediction = otmfk.getPredictionFunction()
otmfkpvariances = otmfk.getConditionalVarianceFunction()
otmfkgradient = otmfk.getPredictionDerivativesFunction()

print('Predicted values by MFK:',otmfkprediction(xv_e))    
print('Predicted variances values by MFK:',otmfkpvariances(xv_e))    
print('Prediction derivatives by MFK:',otmfkgradient(xv_e))  

plt.figure()

plt.plot(xt_c,yt_c,'o',label='low fidelity data')
plt.plot(xt_e,yt_e,'o',label='high fidelity data')

plt.plot(xv_e,otmfkprediction(xv_e),label='high fidelity prediction')
plt.plot(xv_e,yv_e,label='high fidelity true function')
plt.legend()





