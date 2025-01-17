import numpy as np
from torchy.templates import Activation

class Sigmoid(Activation):
    
    def __init__(self) -> None:
        super().__init__()
        self.cache['y'] = []

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.cache['x'].append(x)
        y = 1 / (1 + np.exp(-x))
        self.cache['y'].append(y)
        return y

    def backward(self, grad: np.ndarray) -> np.ndarray:
        y = self.cache['y'].pop()
        return grad * y * (1 - y)

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.forward(x)

class Tanh(Activation):
        
    def __init__(self) -> None:
        super().__init__()
        self.cache['y'] = []

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.cache['x'].append(x)
        y = np.tanh(x)
        self.cache['y'].append(y)
        return y

    def backward(self, grad: np.ndarray) -> np.ndarray:
        self.cache['x'].pop()
        return grad * (1 - np.square(self.cache['y'].pop()))

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.forward(x)

class ReLU(Activation):
            
    def __init__(self) -> None:
        super().__init__()

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.cache['x'].append(x)
        y = np.maximum(0, x)
        return y

    def backward(self, grad: np.ndarray) -> np.ndarray:
        x = self.cache['x'].pop()
        dx = np.ones_like(x)
        dx[x < 0] = 0
        return grad * dx

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.forward(x)

class Softmax(Activation):
                
    def __init__(self) -> None:
        super().__init__()

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.cache['x'] = x
        exp_x = np.exp(x - np.max(x))
        softmax_output = exp_x / np.sum(exp_x + 1e-12, axis=1, keepdims=True)
        self.cache['y'] = softmax_output
        return softmax_output

    def backward(self, grad: np.ndarray) -> np.ndarray:
        softmax_output = self.cache['y']
        jacobian_matrix = np.zeros((softmax_output.shape[0], softmax_output.shape[1], softmax_output.shape[1]))
        for i in range(softmax_output.shape[0]):
            for j in range(softmax_output.shape[1]):
                for k in range(softmax_output.shape[1]):
                    if j == k:
                        jacobian_matrix[i, j, k] = softmax_output[i, j] * (1 - softmax_output[i, k])
                    else:
                        jacobian_matrix[i, j, k] = -softmax_output[i, j] * softmax_output[i, k]
        grad_input = np.matmul(grad.reshape(grad.shape[0], 1, grad.shape[1]), jacobian_matrix).squeeze()
        return grad_input

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.forward(x)