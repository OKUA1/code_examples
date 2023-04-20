from typing import List
import onnxruntime as ort
from constants import MODEL_PATH, CLASSES
from convert import convert_input
from fastapi import FastAPI

app = FastAPI()

sess = ort.InferenceSession(MODEL_PATH)

@app.post("/predict")
def predict(X: List[List]):
    pred = sess.run(["output_label"], convert_input(X))[0].tolist()
    y = [CLASSES[i] for i in pred]
    return {"y": y}

