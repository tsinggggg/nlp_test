import numpy as np


def predict_function_for_huggingface_pipeline(input, pipeline):
    raw_preds = pipeline(input)
    pp = np.array([[p['score'] for p in x] for x in raw_preds])
    preds = np.argmax(pp, axis=1)
    return preds, pp


def predict_function_for_sklearn_pipeline(input, pipeline):
    preds = pipeline.predict(input)
    pp = pipeline.predict_proba(input)
    return preds, pp