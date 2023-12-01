import tensorflow as tf
import numpy as np


class NeuralNetwork:
    def __init__(self):
        self.model = self.get_model()

    def get_model(self):
        model = tf.keras.models.load_model('handwriting.keras')
        return model

    def get_number(self, number):
        number = number.reshape((1, 28, 28))
        prediction = self.model.predict(number)
        return np.argmax(prediction)
    

if __name__ == '__main__':
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    
    # Normalize input data
    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)

    # Get sequantial model
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape=(28,28)))
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dense(10, activation='softmax'))

    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )

    # Train in 10 epochs
    model.fit(x_train, y_train, epochs=10)

    # Save to file for the runner.
    model.save('handwriting.keras')

    # Evaluate
    model = tf.keras.models.load_model('handwriting.keras')
    loss, accuracy = model.evaluate(x_test, y_test)
    print(f'Loss: {loss}, Accuracy: {accuracy}')
