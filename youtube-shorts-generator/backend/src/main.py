import os
import sys

# Adicionar o diretório 'src' ao PYTHONPATH para resolver ModuleNotFoundError
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from flask import Flask, send_from_directory
from flask_cors import CORS

# Importar blueprints
from routes.youtube import youtube_bp
from routes.video_processing import video_processing_bp
from routes.auth import auth_bp
from routes.upload import upload_bp
from routes.user import user_bp # Assumindo que você tem um blueprint para user

app = Flask(__name__, static_folder=".", static_url_path="/")
CORS(app) # Habilitar CORS para todas as rotas

# Configurações da aplicação
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "supersecretkey") # Use uma chave secreta forte em produção
app.config["GOOGLE_CLIENT_ID"] = os.environ.get("GOOGLE_CLIENT_ID")
app.config["GOOGLE_CLIENT_SECRET"] = os.environ.get("GOOGLE_CLIENT_SECRET")
app.config["TIKTOK_CLIENT_ID"] = os.environ.get("TIKTOK_CLIENT_ID")
app.config["TIKTOK_CLIENT_SECRET"] = os.environ.get("TIKTOK_CLIENT_SECRET")

# Registrar blueprints
app.register_blueprint(youtube_bp, url_prefix="/api/youtube")
app.register_blueprint(video_processing_bp, url_prefix="/api/video")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(upload_bp, url_prefix="/api/upload")
app.register_blueprint(user_bp, url_prefix="/api/user") # Registrar blueprint para user

# Rota para servir o frontend (index.html)
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# Rota para servir outros ficheiros estáticos do frontend
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    # Quando executado localmente, o Vercel não usa este bloco diretamente
    # Mas é útil para testes locais
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))

