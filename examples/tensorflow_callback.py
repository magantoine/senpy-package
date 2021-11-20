"""

Leveraging Callbacks in Tensorflow Keras, we can create custom callbacks 
to track events and variables of interest. Here is a simple example of a
callback that notifies us when training and the evaluations finish including
the model score.

"""

from tensorflow import keras
from senpy import notify_me

# Create a custom Tensorflow Keras callback 
class NotifyMeCallback(keras.callbacks.Callback):
    # More information on custom callbacks: https://www.tensorflow.org/guide/keras/custom_callback
    
    def on_train_end(self, logs=None):
        notify_me(f"Training finished with MSE: {logs['mean_squared_error']:.2f}")
        
    def on_test_end(self, logs=None):
        notify_me(f"Evaluation finished with test MSE: {logs['mean_squared_error']:.2f}")


def main():
    # Load example MNIST data and pre-process it
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train = x_train.reshape(-1, 784).astype("float32") / 255.0
    x_test = x_test.reshape(-1, 784).astype("float32") / 255.0

    # Define the model to add callbacks to
    model = keras.Sequential()
    model.add(keras.layers.Dense(1, input_dim=784))
    model.compile(
        optimizer=keras.optimizers.RMSprop(learning_rate=0.1),
        loss="mean_squared_error",
        metrics=["mean_squared_error"],
    )

    # Fit the model to training data
    model.fit(
        x_train, y_train, batch_size=128, epochs=1, verbose=0,
        callbacks=[NotifyMeCallback()] # Get notified on training end
    )

    # Evaluate the model on test data
    model.evaluate(
        x_test, y_test, batch_size=128, verbose=0, 
        callbacks=[NotifyMeCallback()] # Get notified on evaluation end
    )

if __name__ == '__main__':
    main()