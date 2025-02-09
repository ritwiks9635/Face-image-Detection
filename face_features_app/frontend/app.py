import gradio as gr
from PIL import Image
import requests
import io

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import backend function
from backend.detect import detect_objects

def detect_and_display(image):
    return detect_objects(image)

# Gradio UI
gr.Interface(
    fn=detect_and_display,
    inputs=gr.Image(type="pil"),
    outputs=gr.Image(type="pil"),
    title="YOLO Object Detection",
    description="Upload an image to detect objects using YOLO.",
).launch(debug=True)
