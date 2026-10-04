import io
import os

import mlflow
import numpy as np
from fastapi import FastAPI, File, UploadFile
from PIL import Image


# MLflow setup
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://127.0.0.1:5000"
)

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


# Load the champion model once when the API starts
model = mlflow.pyfunc.load_model(
    "models:/food11@champion"
)


# Food-11 categories
categories = [
    "Bread",
    "Dairy product",
    "Dessert",
    "Egg",
    "Fried food",
    "Meat",
    "Noodles-Pasta",
    "Rice",
    "Seafood",
    "Soup",
    "Vegetable-Fruit",
]


# Create FastAPI app
app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Read uploaded image
    contents = await file.read()

    image = Image.open(
        io.BytesIO(contents)
    ).convert("RGB")


    # Resize image to the size used during training
    image = image.resize((128, 128))


    # Convert image to numpy array
    image_array = np.array(
        image
    ).astype(np.float32) / 255.0


    # Convert from HWC format to CHW format
    image_array = np.transpose(
        image_array,
        (2, 0, 1)
    )


    # Add batch dimension
    image_array = np.expand_dims(
        image_array,
        axis=0
    )


    # Run prediction
    output = model.predict(
        image_array
    )


    # Get raw scores from model output
    scores = np.asarray(output)[0]


    # Convert raw scores to probabilities using softmax
    exp_scores = np.exp(
        scores - np.max(scores)
    )

    probabilities = (
        exp_scores / exp_scores.sum()
    )


    # Get predicted class
    predicted_index = int(
        np.argmax(probabilities)
    )


    # Get confidence score
    confidence = float(
        probabilities[predicted_index]
    )


    # Return prediction
    return {
        "category": categories[predicted_index],
        "confidence": confidence
    }