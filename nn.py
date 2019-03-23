import numpy as np

def NN(X, y):
    def nonlin(x, deriv=False):  # Note: there is a typo on this line in the video
        if (deriv == True):
            return (x * (1 - x))

        return 1 / (1 + np.exp(-x))


    # INPUT X

    # OUTPUT y

    np.random.seed(1)

    # for i in X:
    #     syn0 = 2*np.random.random() - 1
    # for i in y:
    #     syn1 = 2 * np.random.random() - 1
    # syn0 = X
    # syn1 = y
    syn0 = 2*np.random.random((1,1)) - 1  # 3x4 matrix of weights ((2 inputs + 1 bias) x 4 nodes in the hidden layer)
    syn1 = 2*np.random.random((1,1)) - 1  # 4x1 matrix of weights. (4 nodes x 1 output) - no bias term in the hidden layer.

    for j in range(1000):
        # Calculate forward through the network.
        l0 = X
        l1 = nonlin(np.dot(l0, syn0))
        l2 = nonlin(np.dot(l1, syn1))

        # Back propagation of errors using the chain rule.
        l2_error = y - l2
        if (j % 10000) == 0:  # Only print the error every 10000 steps, to save time and limit the amount of output.
            print("Error: " + str(np.mean(np.abs(l2_error))))

        l2_delta = l2_error * nonlin(l2, deriv=True)

        # l1_error = l2_delta.dot(syn1.T)
        l1_error = l2_delta.dot(syn1)

        l1_delta = l1_error * nonlin(l1, deriv=True)

        # update weights (no learning rate term)
        # syn1 += l1.dot(l2_delta)
        # syn0 += l0.dot(l1_delta)
        syn1 += l1 * l2_delta
        syn0 += l0 * l1_delta

        print("Output after training")
        print(l2)
    return l2