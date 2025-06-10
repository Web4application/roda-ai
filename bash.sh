/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

npm install @liveblocks/client @liveblocks/react @liveblocks/yjs yjs @monaco-editor/react y-monaco y-protocols
pip install python-dotenv psycopg2

git add .
git commit -m "Added files from phone"
git push origin main

pip install -r requirements.txt

npx create-liveblocks-app@latest --init --framework react

git clone https://github.com/QUBUHUB-repos/RODA-AI-Web.git

git clone https://github.com/Web4application/RODAAI.git

cd RODAAI
cp .env.example .env
docker-compose up --build
