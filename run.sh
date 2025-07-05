git clone https://github.com/Web4application/RODAAI.git
cd RODAAI
cp .env.example .env
docker-compose up --build


git clone https://github.com/Web4application/project_pilot_ai.git
cd project_pilot_ai
pip install -r requirements.txt

# Format
black . && isort .

# Migrate database
alembic upgrade head

# Run local server
uvicorn app.main:app --reload
