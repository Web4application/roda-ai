# Format
black . && isort .

# Migrate database
alembic upgrade head

# Run local server
uvicorn app.main:app --reload
