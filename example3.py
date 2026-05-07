import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from matplotlib import pyplot as plt

# Model / data parameters
num_classes = 10
input_shape = (28, 28, 1)

# Load the MNIST dataset, split into training and test sets

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Normalize the pixel values to the [0, 1] range (originally 0-255)
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

# Ensure the images have a shape of (28, 28, 1) by adding an extra dimension for "channels"
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

# Display information about the training set
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")

# Display the first 9 images in the training set to verify the data
for i in range(9):

	plt.subplot(330 + 1 + i)

	plt.imshow(x_train[i], cmap=plt.get_cmap('gray'))
# show the figure
plt.show()


# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# Define a simple Convolutional Neural Network (CNN)

model = keras.Sequential([
	# layers.Dense(64, activation='relu', input_shape=(20, )),
	# layers.Dense(32, activation='relu'),
    # layers.Dense(1, activation='sigmoid'),
    # specifying the dimensions (height, width, channels) of the incoming image data.
    layers.Input(shape=input_shape),

    # Applies 32 distinct filters to scan the image for features
    layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),

    # Reduces the spatial dimensions (width/height) by half by taking the maximum value in 2x2 windows
    layers.MaxPooling2D(pool_size=(2, 2)),

    # A second convolutional layer with 64 filters to detect more complex patterns built on the first layer.
    layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),

    # Down samples the feature maps again, further reducing the number of parameters.
    layers.MaxPooling2D(pool_size=(2, 2)),

    # Converts the 2D maps into a single long 1D vector, so they can be fed into the standard nn.
    layers.Flatten(),

    # Randomly drop 50% of the neurons during training to prevent overfitting
    layers.Dropout(0.5),

    # The final output layer with one node per class
    # 'softmax' turns the output into probabilities that sum to 100% across all categories.
    layers.Dense(num_classes, activation="softmax"),
])

model.summary()

batch_size = 128
epochs = 1

# Compile the model with loss function, optimizer, and metrics

pass

# Fit the model to the training data, with a validation split

pass

# Evaluate the model on the test set

pass

print("Test loss:", score[0])
print("Test accuracy:", score[1])

