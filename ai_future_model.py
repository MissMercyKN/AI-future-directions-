import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras import layers, models

# Load sample image classification dataset
(ds_train, ds_test), ds_info = tfds.load(
    'rock_paper_scissors',
    split=['train', 'test'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True
)

# Preprocess images: resize and normalize
def format_example(image, label):
    image = tf.image.resize(image, (64, 64)) / 255.0
    return image, label

ds_train = ds_train.map(format_example).batch(32)
ds_test = ds_test.map(format_example).batch(32)

# Build a lightweight CNN model
model = models.Sequential([
    layers.Input(shape=(64, 64, 3)),
    layers.Conv2D(16, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(3, activation='softmax')  # 3 classes: rock, paper, scissors
])

# Compile and train the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

print("🚀 Training model...")
model.fit(ds_train, epochs=5, validation_data=ds_test)

# Evaluate model
loss, accuracy = model.evaluate(ds_test)
print(f"✅ Model test accuracy: {accuracy:.2f}")

# Convert to TensorFlow Lite model
print("🔄 Converting to TensorFlow Lite format...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model
with open('recycle_model.tflite', 'wb') as f:
    f.write(tflite_model)

print("📦 Saved as 'recycle_model.tflite'")
