from typing import List
from falcon.runtime import ONNXRuntime
import numpy as np
from fastapi import FastAPI

app = FastAPI()

rt = ONNXRuntime("model_falcon.onnx")

@app.post("/predict")
def predict(X: List[List]):
    y = rt.run(np.asarray(X, dtype=object))[0].tolist()
    return {"y": y}

