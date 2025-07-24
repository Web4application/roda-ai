npm install -r requirements.txt
# Step 1: Build Docker image
docker build -t roda-ai-api .

# Step 2: Run container
docker run -d -p 8000:8000 roda-ai-api

# OR using Compose
docker compose up --build

$ npm install
$ npm run dev
