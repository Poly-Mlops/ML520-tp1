"""Entrypoint for the application server

    gunicorn --worker-class uvicorn.workers.UvicornWorker inferapi.serve:app

It is cleaner to have a single file rather than putting this in app.py.
The job of this file is to create the configuration and instantiate the app;
app.py stays a factory that anybody (a test, another deployment) can call
with something else.

# TODO(LAB): write load_predictor() and the module-level `app`. This is the only
# module allowed to name a concrete Predictor implementation, and the only one that
# builds an InferApiSettings.
"""

from inferapi.app import create_app
from inferapi.config import InferApiSettings
from inferapi.predictor import Predictor


# TODO(LAB): Implement this
def load_predictor(settings: InferApiSettings) -> Predictor: ...


# What gunicorn and uvicorn import
# TODO(LAB): Implement this
app = create_app(...)
