# "AI for Microscopy" - a micro-service template

This repository contains a template for a 
FastAPI-based microservice. The main goal of the template is too accelerate the development
of a multitude of services that can be used to compute different recognition tasks on microscopy images. **If you implement a service based on this template please change this description and subsequent sections appropiately**. There is also the markdown file ``MODELCARD.md`` that needs to be filled out properly.

Author: *Erik Rodner*, 2024 (change if you use the template)

## Getting started

All requirements are listed in ``requirements.txt``and can be therefore
installed into a fresh python virtual environment:
```bash
pip install -r requirements.txt
```

Running of the service (for testing) is straightforward using uvicorn:
```bash
uvicorn app.main:app --reload
```

## Testing

We also provide a simple template for testing the service:
```bash
PYTHONPATH=. pytest tests/
```

## API

Outline the API implemented. Try to stick to the API of the template as best as possible (it might be not perfect).

## Model documentation

All details about the model and related data can be found in the [model card](MODELCARD.md).