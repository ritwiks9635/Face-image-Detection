import tensorflow as tf
import numpy as np
import keras_cv
import cv2
from keras_cv.visualization import plot_bounding_box_gallery
from PIL import Image

# Load Model & Define Backbone
backbone = keras_cv.models.YOLOV8Backbone.from_preset("yolo_v8_s_backbone_coco")

yolo = keras_cv.models.YOLOV8Detector(
    num_classes=2,  # Change based on dataset
    bounding_box_format="xyxy",
    backbone=backbone,
    fpn_depth=1,
)

# Define optimizer
optimizer = tf.keras.optimizers.Adam(learning_rate=0.005, global_clipnorm=1.0)
yolo.compile(
    optimizer=optimizer,
    classification_loss="binary_crossentropy",
    box_loss="ciou",
    jit_compile=False
)

# Load weights (If using saved checkpoints)
checkpoint_path = "backend/model/model.keras"
yolo.load_weights(checkpoint_path)

# Preprocessing
p_resizing = keras_cv.layers.Resizing(640, 640, bounding_box_format="xyxy", pad_to_aspect_ratio=True)

# Define NMS
yolo.prediction_decoder = keras_cv.layers.MultiClassNonMaxSuppression(
    bounding_box_format="xyxy",
    from_logits=True,
    iou_threshold=0.5,
    confidence_threshold=0.65,
)

# Class Mapping
class_mapping = {0: 'eye', 1: 'eyebrow', 2: 'lip', 3: 'mustache-beard', 4: 'nose'}

def detect_objects(image):
    """ Runs inference on the given image and returns results with bounding boxes. """
    # Convert PIL Image to NumPy array
    image_np = np.array(image)

    # Convert to TensorFlow tensor & Resize
    image_tensor = tf.convert_to_tensor(image_np, dtype=tf.uint8)
    image_resized = p_resizing([image_tensor]) / 255.0  # Normalize to [0,1]

    # Run YOLO inference
    y_pred = yolo.predict(image_resized)

    # Extract predictions
    boxes = y_pred["boxes"][0].numpy()  # Extract first batch
    classes = y_pred["classes"][0].numpy()
    scores = y_pred["confidence"][0].numpy()

    # Draw bounding boxes
    for box, cls, score in zip(boxes, classes, scores):
        if score < 0.65:
            continue

        x1, y1, x2, y2 = map(int, box)  # Convert to integers
        label = f"{class_mapping.get(int(cls), 'Unknown')} {score:.2f}"

        # Draw rectangle
        cv2.rectangle(image_np, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image_np, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return Image.fromarray(image_np)  # Convert back to PIL format

if __name__ == "__main__":
