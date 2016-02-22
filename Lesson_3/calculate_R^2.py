import numpy as np

def compute_r_squared(data, predictions):
    # Write a function that, given two input numpy arrays, 'data', and 'predictions,'
    # returns the coefficient of determination, R^2, for the model that produced 
    # predictions.
    # 
    # Numpy has a couple of functions -- np.mean() and np.sum() --
    # that you might find useful, but you don't have to use them.

    no = (data.values-predictions)**2
    print no
    deno = (data.values-np.mean(data.values))**2
    print deno
    r_squared = 1 - (np.sum(no)/np.sum(deno))

    return r_squared