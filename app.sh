#!/bin/bash

alembic revision --autogenerate -m "Database creation"
alembic upgrade head

cd src

uvicorn main:app --reload --host=0.0.0.0 --port=8000