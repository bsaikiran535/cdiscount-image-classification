from keras.applications import InceptionV3
from keras.models import Sequential, Model
from keras.layers import Dropout, Flatten, Dense
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D, GlobalAveragePooling2D

from data_generator import get_generator, NUM_CLASSES, NUM_TRAIN_SAMPLES, BATCH_SIZE, IMG_X, IMG_Y, NUM_CHANNELS


def get_model():
    model = Sequential()
    model.add(Conv2D(32, 3, padding="same", activation="relu", input_shape=(IMG_X, IMG_Y, NUM_CHANNELS)))
    model.add(MaxPooling2D())
    model.add(Conv2D(64, 3, padding="same", activation="relu"))
    model.add(MaxPooling2D())
    model.add(Conv2D(128, 3, padding="same", activation="relu"))
    model.add(MaxPooling2D())
    model.add(GlobalAveragePooling2D())
    model.add(Dense(NUM_CLASSES, activation="softmax"))

    model.compile(optimizer="adam",
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])

    model.summary()
    return model


def get_inception_model():
    # base pre-trained model
    base_model = InceptionV3(include_top=False, weights='imagenet')

    # Global
    x = base_model.output
    x = GlobalAveragePooling2D()(x)

    # Fully connected layer
    x = Dense(units=NUM_CLASSES * 5, activation='relu')(x)
    # Logistic softmax layer
    predictions = Dense(NUM_CLASSES, activation='sigmoid')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    # Train only the top layers
    for layer in base_model.layers:
        layer.trainable = False

    # Compile the model
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    return model


if __name__ == "__main__":
    model = get_inception_model()
    train_gen, val_gen = get_generator()
    model.fit_generator(train_gen,
                        steps_per_epoch=NUM_TRAIN_SAMPLES // BATCH_SIZE,  # num_train_images // batch_size,
                        epochs=3,
                        validation_data=val_gen,
                        validation_steps=2469026 // BATCH_SIZE,  # num_val_images // batch_size,
                        workers=1)
