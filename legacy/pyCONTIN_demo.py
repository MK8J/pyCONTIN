#! python3
# ## This example file demonstrates how to use pyCONTIN wrapper

# Load the required packages
import numpy as np
import matplotlib.pyplot as plt
from CONTINWrapper import runCONTINfit

# #### Load example transient file

trans_data = np.loadtxt("demo_input.csv")
x = trans_data[:, 0]
y = trans_data[:, 1]
print(x.shape)

# #### Assign template file

template_file = "paramTemplate.txt"

alldata = runCONTINfit(x, y, template_file)

testxdata = alldata[2][1][:, 2]

testydata = alldata[2][1][:, 0]

plt.figure()
plt.title('test data')
plt.plot(trans_data[:, 0], trans_data[:, 1], 'o')


p0 = np.polyfit(np.log(y),x,1)
tau = p0[0]
y = np.exp(x/tau)
print(1/tau)

plt.plot(x, y ,'--',label='tau = {}'.format(tau))

plt.figure()
plt.plot(testxdata, testydata)

plt.show()
