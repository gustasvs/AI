import numpy as np

class NeuralNet():
    def __init__(self):
        np.random.seed(1)
        self.synaptic_weights = 2 * np.random.random((3, 1)) - 1
    def sigmod(self, x):
        return 1/ (1 + np.exp(-x))
    def sigmod_derivative(self, x):
        return x + (1-x)
    def train(self, training_inputs, training_outputs, training_iterations):
        for e in range(training_iterations):
            output = self.think(training_inputs)
            error = training_outputs - output
            adjustments = np.dot(training_inputs.T, error * self.sigmod(output))
            self.synaptic_weights += adjustments
    def think(self, inputs):
        inputs = inputs.astype(float)
        output = self.sigmod(np.dot(inputs, self.synaptic_weights))
        return output
if __name__ == "__main__":
    neural_network = NeuralNet()
    print("Random sakumaa: ")
    print(neural_network.synaptic_weights)
    training_inputs = np.array([[0,0,1],
                                [1,1,1],
                                [1,0,1],
                                [0,1,1]])

    training_outputs = np.array([[0,1,1,0]]).T
    neural_network.train(training_inputs, training_outputs, 10000)
    print("Pec trennina: ")
    print(neural_network.synaptic_weights)
    A = str(input("Input 1: "))
    B = str(input("Input 2: "))
    C = str(input("Input 3: "))
    print("Jaunie inputi = ", A, B, C)
    print("izspeeriens: ")
    print(neural_network.think(np.array([A, B, C])))

