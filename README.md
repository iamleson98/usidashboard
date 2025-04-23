basic DB commands:

- create new migration:

alembic revision -m "<migration_name_here>"

- migrate your new migration file(s):

alembic upgrade <revision_code>

- downgrade your migrations to previous migrations:

alembic downgrade <down_revision_code>

run:
 `uvicorn main:app --reload`
