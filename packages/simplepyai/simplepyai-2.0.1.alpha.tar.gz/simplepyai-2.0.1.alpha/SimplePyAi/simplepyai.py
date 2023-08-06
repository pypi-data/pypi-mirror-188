import pickle
from matplotlib import pyplot as plt
from tqdm import tqdm
import numpy as np

color1 = '\033[92m'
color2 = '\033[94m'
color3 = '\033[0m'

print(
    f"{color1}You use the library SimplePyAI !\n{color2}Credit: LeLaboDuGame on Twitch -> https://twitch.tv/LeLaboDuGame{color3}")


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def derivation_sigmoid(y):
    return y * (1 - y)


def mse(y_true, y_pred):
    return np.square(np.subtract(y_true, y_pred)).mean()


def derivative_mse(y_true, y_pred):
    return 2 * (y_pred - y_true) / len(y_true)


def leakly_relu(x, alpha=0.01):
    return np.where(x > 0, x, x * alpha)


def leakly_relu_derivative(x, alpha=0.01):
    return np.where(x > 0, 1, alpha)


def linear(x):
    return x

def linear_derivative(x):
    return 1


class AdamOptim:
    def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m_w = None
        self.v_w = None
        self.m_b = None
        self.v_b = None
        self.t_w = 0.0001
        self.t_b = 0.0001

    def update(self, w, b, dw, db):
        if self.m_w is None:
            self.m_w = np.zeros_like(w)
            self.v_w = np.zeros_like(w)
            self.m_b = np.zeros_like(b)
            self.v_b = np.zeros_like(b)

        lr_t_w = self.learning_rate * np.sqrt(1.0 - self.beta2 ** self.t_w) / (1.0 - self.beta1 ** self.t_w)
        lr_t_b = self.learning_rate * np.sqrt(1.0 - self.beta2 ** self.t_b) / (1.0 - self.beta1 ** self.t_b)

        self.m_w += (1 - self.beta1) * (dw - self.m_w)
        self.v_w += (1 - self.beta2) * (dw ** 2 - self.v_w)
        self.m_b += (1 - self.beta1) * (db - self.m_b)
        self.v_b += (1 - self.beta2) * (db ** 2 - self.v_b)
        old_w = w
        old_b = b
        w -= lr_t_w * self.m_w / (np.sqrt(self.v_w) + self.epsilon)
        b -= lr_t_b * self.m_b / (np.sqrt(self.v_b) + self.epsilon)
        if np.array_equal(old_w, w):
            self.t_w += 1
        if np.array_equal(old_b, b):
            self.t_b += 1
        return w, b


# Some funtions
# ----------------------------------------------------------------------------------------------------------------------
# AI Models

class Layer:
    def __init__(self, nbr, activation_function=sigmoid, derivation_function=derivation_sigmoid, optimizer=AdamOptim()):
        self.nbr = nbr
        self.activation_function = activation_function
        self.derivation_function = derivation_function
        self.optimizer = optimizer

    def forwardpropagation(self, x, w, b):
        z = np.dot(w, x)
        return self.activation_function(z + b), z

    def backpropagation(self, A, w, grad_z):
        grad_w = np.dot(A[0], grad_z.T)
        grad_b = np.sum(grad_z, axis=1, keepdims=True)

        if A[1] is not None:
            derivate = self.derivation_function(A[1])
            grad_z = np.dot(w.T, grad_z) * derivate

        return grad_w.T, grad_b, grad_z


class Neural_Network:
    """
    SIMPLEPYAI
    ----------
    Hey guy !
    I'm 15 years and a frensh dev !
    I present you my project of neural network !
    Just for the credit : LeLaboDuGame on Twitch -> https://twitch.tv/LeLaboDuGame
    You can use this library on all your project !

    EXAMPLE:
    --------
        x = [[1], [0]]
        y = [[0], [1]]
        nn = Neural_Network(x, y, layers=[1, 64, 32, 64, 1], learning_rate=0.001, activation_function=sigmoid,
                            derivation=derivation_sigmoid, reload_last_session=False)
        nn.train(10000, show=True)
        print(nn.predict([[1], [0]]))  # predict values

    HOW TO USE:
    -----------
        TO START:
            -To init you must send 'x' and 'y' list (or numpy array).
            'x' is your input and 'y' is your output.

            -You must put the 'layers' (default is [2, 3, 1] 2 is the input and 1 the output neurone).
            The 'layers' is a list represent all of your layers with the number of your neurone example:

            [4,                                     3,4,10,1,                                       100]
             ^                                          ^                                             ^
             |                                          |                                             |
            (is for 4 neurone in the first layer)(some layers)(And the number of neurones in the output)

            -You can set the 'learning_rate' more is small more he understands, but it will take more repetition in
            training.

            -'reload_last_session' (default: False) is to reload the last session (if is the first sessions set to False)

        TO TRAIN:
            -'n_iter' is the number of train repetition

            -'show' (default: True) is to show how the graphique of your model

            -'save' (default: False) is to save your model (you can reload your model with the 'reload_last_session'
            in init.

    Now it's possible to choose an activation function, to do that you can refer at the "sigmoid" function and
    the "derivation_sigmoid" function
    Thank you very much to use this library !
    """

    def __init__(self, layers, loss_function=mse, error_function=derivative_mse,
                 learning_rate=0.1, reload_last_session=False):
        self.layers = layers
        self.learning_rate = learning_rate
        self.error_function = error_function
        self.loss_function = loss_function

        self.parametres = {}
        if reload_last_session:
            a_file = open("ia_parametres.pkl", "rb")
            self.parametres = pickle.load(a_file)
            a_file.close()

        else:
            # Initialistaion des dict W (weight) et B (Bias) avec les couches definie
            self.weights = []
            self.biases = []
            # layer = [3, 64, 128, 64, 2]
            for i in range(1, len(layers)):
                self.weights.append(np.random.rand(self.layers[i].nbr, self.layers[i - 1].nbr))
                self.biases.append(np.random.rand(self.layers[i].nbr, 1))

    def accuracy_score(self, y_pred):
        score = 1 - np.sum(np.absolute(self.y.flatten() - y_pred))
        return score

    def forward_propagation(self, x):
        A = [(x.T, None)]

        for c in range(1, len(self.layers)):
            A.append(self.layers[c].forwardpropagation(A[c - 1][0], self.weights[c - 1],
                                                       self.biases[c - 1]))
        return A

    def back_propagation(self, y, A):

        grad_w = []
        grad_b = []
        for i in range(len(A) - 1):
            grad_w.append(np.zeros(1))
            grad_b.append(np.zeros(1))

        # Calcul des gradients de la couche de sortie
        grad_z = self.error_function(self.y, A[-1][0].T).T
        for i in reversed(range(1, len(self.layers))):
            # layer.backpropagation(A, _A, w, grad_z)
            grad_w[i - 1], grad_b[i - 1], grad_z = self.layers[i].backpropagation(A=A[i - 1],
                                                                                  w=self.weights[i - 1],
                                                                                  grad_z=grad_z)

        return grad_w, grad_b

    def predict(self, x):
        A = self.forward_propagation(np.array(x))
        return A[-1][0]

    def show(self, Loss, acc):
        plt.figure(figsize=(14, 4))
        plt.subplot(1, 3, 1)
        plt.plot(Loss)
        plt.title("loss")
        plt.subplot(1, 3, 2)
        plt.plot(acc)
        plt.title("accuracy")

        C = len(self.layers)
        plt.show()

    def log_loss(self, y_pred):
        return np.sum(np.absolute(self.y.flatten() - y_pred))

    def update(self, grad_w, grad_b, episode):
        for i in range(1, len(self.layers)):
            self.weights[i - 1], self.biases[i - 1] = self.layers[i].optimizer.update(self.weights[i - 1],
                                                                                      self.biases[i - 1],
                                                                                      grad_w[i - 1],
                                                                                      grad_b[i - 1])

    def train(self, x, y, n_iter, show=True, save=False):
        acc = []
        Loss = []
        self.x = x
        self.y = y
        for episode in tqdm(range(n_iter)):
            # methode d'activation
            A = self.forward_propagation(self.x)
            grad_w, grad_b = self.back_propagation(self.y, A)
            self.update(grad_w, grad_b, episode)
            if episode % 10 == 0:
                Loss.append(self.loss_function(self.y, A[-1][0]))
                acc.append(self.accuracy_score(A[-1][0].flatten()))

        # prediction
        y_pred = self.predict(self.x)
        print(f"Score de l'entrainement = {self.accuracy_score(y_pred[0].flatten()) * 100}%")

        # montre la courbe de Loss montrant la diminution de la perte du model
        print(f"La perte est de : {Loss[-1]} !")

        if save:
            a_file = open("ia_parametres.pkl", "wb")
            pickle.dump(self.parametres, a_file)
            a_file.close()

        if show:
            self.show(Loss, acc)
        return y_pred


"""
EXEMPLE:
x = [[1, 0,
      1, 0], [1, 0,
              0, 0], [0, 1,
                      0, 1],
     [0, 0,
      1, 0], [0, 0,
              1, 1], [0, 0,
                      0, 1]]

y = [[5], [-5], [5], [-5], [5], [-5]]

nn = Neural_Network(x, y,
                    [Layer(4),  # Input = no function
                     Layer(64, activation_function=leakly_relu, derivation_function=leakly_relu_derivative, optimizer=AdamOptim()),
                     Layer(64, activation_function=leakly_relu, derivation_function=leakly_relu_derivative, optimizer=AdamOptim()),
                     Layer(1, activation_function=linear, derivation_function=linear_derivative, optimizer=AdamOptim())],
                    loss_function=mse,
                    error_function=derivative_mse,
                    learning_rate=0.5)
nn.train(20000, False)
print(nn.predict([[1, 0,
                   1, 0], [1, 0,
                           0, 0]]))
"""
