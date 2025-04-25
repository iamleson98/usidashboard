`25/4/2025`

project authors:
Nickson Le - nickson_le@usiglobal.com (core maintainer) <br />Mark Do <br />Mac Pham

### for the backend development, we need

1) FastAPI for backend server
2) sqlalchemy for database interaction
3) Alembic for database migration

### Architecture of this project

This project is based on Clean Architecture, for extensibility, maintainability and decoupling code.

### Setup:
1) setup python3 virtual environment

`python3 -m venv env`

`./env/Scripts/activate.bat` for Windows OR<br />
`source env/bin/activate` for linux

2) install required packages

`pip install -r ./requirements.txt`

3) Do database migration:

Run the following command to migrate your migration file to the latest revision:

`alembic upgrade head`

4) to run:

 `uvicorn main:app --reload`

### Migration overview

The following are a few basic cli commands that will help you have a functional db system.
For basic needs, we need a means to alter (upgrade) and redo (downgrade). That is why each revision files contain dedicated functions for each need.

- to create a new migration:

`alembic revision -m "<migration_name_here>"`

- migrate to your new migration file:

`alembic upgrade <revision_code>`

- downgrade to specific revision:

`alembic downgrade <down_revision_code>`


