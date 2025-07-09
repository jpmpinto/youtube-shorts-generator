# Dockerfile para YouTube to Shorts Generator

FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Instalar pnpm
RUN npm install -g pnpm

# Definir diretório de trabalho
WORKDIR /app

# Copiar ficheiros do projeto
COPY . .

# Instalar dependências do frontend e fazer build
WORKDIR /app/frontend
RUN pnpm install
RUN pnpm run build

# Copiar build para o backend
RUN cp -r dist/* ../backend/src/static/

# Mudar para o diretório backend
WORKDIR /app/backend

# Criar ambiente virtual e instalar dependências
RUN python -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt

# Expor porta
EXPOSE 5000

# Comando para executar a aplicação
CMD ["/bin/bash", "-c", "source venv/bin/activate && python src/main.py"]

