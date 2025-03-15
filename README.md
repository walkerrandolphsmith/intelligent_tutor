# Intelligent Tutor

## Project Organization
```
intelligent_tutor/
├── data/
│   └── model.pkl            # Pickle file for the serialized model
├── diagrams/                # D2 diagrams
├── docs/                    # Documentation
├── notebooks/               # Jupyter notebooks for building and training models
├── scripts/
    ├── generate_d2_diagrams # Generate PNGs of diagrams
    ├── generate_openapi.py  # Script to fetch OpenAPI schema
│   └── start_web_server.sh  # start the web server
├── .venv/                   # Virtual environment directory
├── dev-requirements         # Dependencies only required for development
├── main.py                  # Main FastAPI application
├── pyproject.toml           # Build system requirements for python project
├── README.md                # Project documentation
└── requirements.txt         # Dependencies required for production
```

## Development Setup
```
python -m venv .venv

./.venv/Scripts/activate

pip install -r requirements.txt
```

## Build the model
Open `./notebooks/lesson_prediction.ipynb` and use python from the virtual environment as the kernel. Run the notebook and it will serialize and write the model to disk as a pickle file.

## Run Tests
Run the following from a shell
```
pytest
```

If there are errors consider setting the PYTHONPATH to the root of the project

```ps
$env:PYTHONPATH="c:\dev\intelligent_tutor"; pytest
```

```sh
export PYTHONPATH=c:/dev/intelligent_tutor; pytest
```

## Run web server
```
uvicorn main:web_server --host 127.0.0.1 --port 8000
```

## Open API Specification

### Build Time
The Open API spec can be generated at build time by executing the following steps:
1. Run the web server
2. In a separate shell, run the following:
    ```py
    python ./scripts/generate_openapi.py
    ```

### Runtime
The Open API spec can be fetched from the the server at runtime via the `/openapi.json` route.
``` 
curl http://localhost:8000/openapi.json
```