from typing import Union
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import pickle
from skfuzzy import control as ctrl
import skfuzzy as fuzz

def load_model():
    """
    Load the machine learning model from the disk
    """
    global model
    global lesson_difficulty
    global user_level
    global accuracy
    with open("./data/model.pkl", "rb") as file:
        data = pickle.load(file)
        model = data['model']
        lesson_difficulty = data['lesson_difficulty']
        user_level = data['user_level']
        accuracy = data['accuracy']
    print("Model loaded successfully")

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Context manager for the lifespan of the FastAPI application.
    Loads the model on startup and cleans up resources on shutdown.
    """
    load_model()
    yield
    print('Cleaning up the resources on application shutdown')

web_server = FastAPI(lifespan=lifespan)

@web_server.get("/healthcheck")
def healthcheck() -> dict[str, str]:
    """
    Checks if the server is healthy
    """
    return {"status": "healthy"}

@web_server.get("/liveliness")
def liveliness() -> dict[str, str]:
    """
    Checks if the server is currently accepting requests
    """
    return {"status": "alive"}

@web_server.get("/readiness")
def readiness() -> dict[str, str]:
    """
    Checks if the server is ready to accept requests
    """
    try:
        if 'model' in globals():
            return {"status": "ready"}
        else:
            raise HTTPException(status_code=503, detail="Model not loaded")
    except Exception as e:
      raise HTTPException(status_code=503, detail=str(e))

@web_server.get("/version")
def version() -> dict[str, str]:
    """
    Returns the version of the application
    """
    build_version = os.getenv("BUILD_VERSION", "1.0.0-dev")
    return {"version": build_version}

@web_server.get("/predict")
def predict(
    user_level_parameter: str = Query(..., description="User level in terms of number of completed lessons"),
    accuracy_parameter: str = Query(..., description="Accuracy in terms of percentage"),
) -> dict:
    """
    Predict the lesson difficulty based on the user level and accuracy
    Accepts user_level and accuracy as query parameters
    Returns the predicted lesson difficulty

    Example: curl "http://127.0.0.1:8000/predict?user_level=100&accuracy=90"
           : curl "http://127.0.0.1:8000/predict?user_level_parameter=expert&accuracy=high"
           : curl "http://127.0.0.1:8000/predict?user_level_parameter=expert&accuracy=50"
    """
    user_level_value = float(user_level_parameter) if is_float(user_level_parameter) else user_level.terms[user_level_parameter]
    accuracy_value = float(accuracy_parameter) if is_float(accuracy_parameter) else accuracy.terms[accuracy_parameter]
    simulation = ctrl.ControlSystemSimulation(model)
    simulation.input['user_level'] = user_level_value
    simulation.input['accuracy'] = accuracy_value
    simulation.compute()
    output = simulation.output['lesson_difficulty']
    easy_membership = fuzz.interp_membership(lesson_difficulty.universe, lesson_difficulty['easy'].mf, output)
    moderate_membership = fuzz.interp_membership(lesson_difficulty.universe, lesson_difficulty['moderate'].mf, output)
    hard_membership = fuzz.interp_membership(lesson_difficulty.universe, lesson_difficulty['hard'].mf, output)
    return {
        "lesson_difficulty": round(output, 2),
        "fuzzy_membership_degrees": {
            "easy": round(easy_membership, 2),
            "moderate": round(moderate_membership, 2),
            "hard": round(hard_membership, 2)
        }
    }

def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False