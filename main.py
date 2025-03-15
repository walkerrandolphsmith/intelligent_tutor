from fastapi import FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
import os
import pickle
from skfuzzy import control as ctrl

def load_model():
    """
    Load the machine learning model from the disk
    """
    global model
    with open("./data/model.pkl", "rb") as file:
        model = pickle.load(file)
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
    soil_level: float = Query(..., description="Soil level in parts per million"),
    load_size: float = Query(..., description="Load size in kilograms"),
    water_temperature: float = Query(..., description="Water temperature in degrees Celsius")
) -> dict[str, str]:
    """
    Predict the wash time based on the soil level, load size, and water temperature
    Accepts soil_level, load_size, and water_temperature as query parameters
    Returns the predicted wash time

    Example: curl "http://127.0.0.1:8000/predict?soil_level=200&load_size=10&water_temperature=50"
    """
    simulation = ctrl.ControlSystemSimulation(model)
    simulation.input['soil_level'] = soil_level
    simulation.input['load_size'] = load_size
    simulation.input['water_temperature'] = water_temperature
    simulation.compute()
    output = simulation.output['wash_time']
    return {"wash_time": str(output) }