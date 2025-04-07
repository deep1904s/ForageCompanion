import os
import json
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input

from utils.logger import logger

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "models", "mushroom_classifierV2.keras")
METADATA_PATH = os.path.join(BASE_DIR, "models", "metadata.txt")
DATA_PATH = os.path.join(BASE_DIR, "data.json")

logger.info("Loading model from %s", MODEL_PATH)
MODEL = load_model(MODEL_PATH)

logger.info("Loading class metadata from %s", METADATA_PATH)
with open(METADATA_PATH, "r") as file:
    CLASS_NAMES = [line.strip() for line in file]


def load_mushroom_data():
    try:
        with open(DATA_PATH, "r") as file:
            logger.info("Mushroom data loaded successfully from %s", DATA_PATH)
            return json.load(file)
    except Exception as e:
        logger.error("Error loading mushroom data from JSON: %s", e)
        return {}


MUSHROOM_DATA = load_mushroom_data()


def predict_mushroom_from_stream(image_stream):
    logger.info("Starting prediction from image stream")

    img = Image.open(image_stream).convert("RGB")
    img = img.resize((299, 299))

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    logger.debug("Running model prediction")
    preds = MODEL.predict(img_array)
    top_indices = np.argsort(preds[0])[-5:][::-1]
    top_predictions = []

    for i in top_indices:
        class_name = CLASS_NAMES[i]
        confidence = float(preds[0][i]) * 100

        logger.debug("Prediction: %s (%.2f%%)", class_name, confidence)

        mushroom_info = next(
            (
                m
                for m in MUSHROOM_DATA
                if m.get("name", "").lower().replace(" ", "_") == class_name.lower()
                or m.get("scientific_name", "").lower().replace(" ", "_")
                == class_name.lower()
                or class_name.split()[0].lower().replace(" ", "_")
                in m.get("name", "").lower().replace(" ", "_")
            ),
            None,
        )

        if not mushroom_info:
            logger.warning("Metadata not found for class: %s", class_name)
            mushroom_info = {}

        info = {
            "scientific_name": mushroom_info.get("scientific_name"),
            "edibility": mushroom_info.get("edibility", "Unknown"),
            "description": mushroom_info.get("description", "No description available"),
            "habitat": mushroom_info.get("habitat", "Unknown"),
            "uses": mushroom_info.get("uses", []),
            "toxicity": mushroom_info.get("toxicity", []),
            "effects": mushroom_info.get("effects", []),
        }

        top_predictions.append(
            {"class_name": class_name, "confidence": confidence, "info": info}
        )

    logger.info("Prediction completed with %d results", len(top_predictions))
    return top_predictions
