# Use a imagem base oficial do Python
FROM python:3.9-slim-buster

# Instalar dependências do sistema (incluindo ffmpeg)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o backend para o container
COPY backend/ /app/backend/

# Mudar para o diretório do backend
WORKDIR /app/backend

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o frontend estático para o diretório static do backend
# Assumimos que o frontend já foi buildado e copiado para backend/src/static localmente antes do deploy
# Se não, você precisaria de um passo de build do frontend aqui ou garantir que o build do frontend é feito antes do deploy
# Para o Vercel, o ideal é que o frontend já esteja na pasta static do backend

# Expor a porta que o Flask vai usar
EXPOSE 5000

# Comando para iniciar a aplicação Flask
CMD ["python", "src/main.py"]
