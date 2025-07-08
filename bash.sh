git clone https://github.com/Web4application/RODAAI.git
cd RODAAI
cp .env.example .env
docker-compose up --build

git clone https://github.com/Web4application/enclov-AI.git
cd enclov-AI

docker-compose up --build
