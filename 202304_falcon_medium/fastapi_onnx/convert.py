from typing import List, Dict
import numpy as np 
from constants import CAT_IND, INPUT_NAMES

def convert_input(X: List[List]) -> Dict[str, np.ndarray]:
    X = np.array(X, dtype=object)
    onnx_input = {}
    for i, n in enumerate(INPUT_NAMES):
        if i in CAT_IND:
            onnx_input[n] = X[:, i].astype(str).reshape(-1, 1)
        else:
            onnx_input[n] = X[:, i].astype(np.float32).reshape(-1, 1)
    return onnx_input