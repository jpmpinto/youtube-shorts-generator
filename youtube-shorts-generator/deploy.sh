#!/bin/bash

# Script de deployment para YouTube to Shorts Generator

echo "🚀 Iniciando deployment..."

# Verificar se estamos no diretório correto
if [ ! -f "README.md" ]; then
    echo "❌ Erro: Execute este script no diretório raiz do projeto"
    exit 1
fi

# Fazer build do frontend
echo "📦 Fazendo build do frontend..."
cd frontend
pnpm install
pnpm run build

# Copiar ficheiros para o backend
echo "📁 Copiando ficheiros para o backend..."
cp -r dist/* ../backend/src/static/

# Voltar ao diretório raiz
cd ..

# Instalar dependências do backend
echo "🐍 Instalando dependências do backend..."
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Atualizar requirements.txt
pip freeze > requirements.txt

echo "✅ Build concluído com sucesso!"
echo ""
echo "📋 Próximos passos para deployment:"
echo "1. Configurar variáveis de ambiente (copiar .env.example para .env)"
echo "2. Obter credenciais OAuth do Google e TikTok"
echo "3. Fazer deploy usando uma das opções:"
echo "   - Vercel: vercel --prod"
echo "   - Heroku: git push heroku main"
echo "   - Docker: docker build -t youtube-shorts-generator ."
echo ""
echo "🌐 Para testar localmente:"
echo "   cd backend && source venv/bin/activate && python src/main.py"
echo "   Aceder a http://localhost:5000"

