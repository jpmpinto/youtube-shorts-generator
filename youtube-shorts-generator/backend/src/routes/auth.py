from flask import Blueprint, request, jsonify, session, redirect, url_for
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import json

auth_bp = Blueprint('auth', __name__)

# Configurações OAuth do Google
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'your-google-client-id')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'your-google-client-secret')
GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI', 'http://localhost:5000/api/auth/google/callback')

# Configurações OAuth do TikTok
TIKTOK_CLIENT_ID = os.environ.get('TIKTOK_CLIENT_ID', 'your-tiktok-client-id')
TIKTOK_CLIENT_SECRET = os.environ.get('TIKTOK_CLIENT_SECRET', 'your-tiktok-client-secret')
TIKTOK_REDIRECT_URI = os.environ.get('TIKTOK_REDIRECT_URI', 'http://localhost:5000/api/auth/tiktok/callback')

# Scopes necessários
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

TIKTOK_SCOPES = [
    'video.upload',
    'user.info.basic'
]

@auth_bp.route('/google/login', methods=['GET'])
def google_login():
    """Iniciar o fluxo de autenticação do Google"""
    try:
        # Criar o fluxo OAuth
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [GOOGLE_REDIRECT_URI]
                }
            },
            scopes=GOOGLE_SCOPES
        )
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        
        # Gerar URL de autorização
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        # Guardar o state na sessão
        session['state'] = state
        
        return jsonify({
            'authorization_url': authorization_url,
            'state': state
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/google/callback', methods=['GET'])
def google_callback():
    """Callback do Google OAuth"""
    try:
        # Verificar o state
        if request.args.get('state') != session.get('state'):
            return jsonify({'error': 'State inválido'}), 400
        
        # Criar o fluxo OAuth
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [GOOGLE_REDIRECT_URI]
                }
            },
            scopes=GOOGLE_SCOPES,
            state=session['state']
        )
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        
        # Trocar o código de autorização por tokens
        flow.fetch_token(authorization_response=request.url)
        
        # Guardar as credenciais na sessão
        credentials = flow.credentials
        session['google_credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        return redirect('http://localhost:5173?google_auth=success')
        
    except Exception as e:
        return redirect(f'http://localhost:5173?google_auth=error&message={str(e)}')

@auth_bp.route('/tiktok/login', methods=['GET'])
def tiktok_login():
    """Iniciar o fluxo de autenticação do TikTok"""
    try:
        # URL de autorização do TikTok
        authorization_url = (
            f"https://www.tiktok.com/auth/authorize/"
            f"?client_key={TIKTOK_CLIENT_ID}"
            f"&scope={','.join(TIKTOK_SCOPES)}"
            f"&response_type=code"
            f"&redirect_uri={TIKTOK_REDIRECT_URI}"
            f"&state=tiktok_auth"
        )
        
        return jsonify({
            'authorization_url': authorization_url
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/tiktok/callback', methods=['GET'])
def tiktok_callback():
    """Callback do TikTok OAuth"""
    try:
        code = request.args.get('code')
        if not code:
            return redirect('http://localhost:5173?tiktok_auth=error&message=Código não fornecido')
        
        # Trocar o código por token de acesso
        # Nota: Implementação simplificada - em produção, fazer a troca real
        session['tiktok_credentials'] = {
            'access_token': 'tiktok_access_token_placeholder',
            'code': code
        }
        
        return redirect('http://localhost:5173?tiktok_auth=success')
        
    except Exception as e:
        return redirect(f'http://localhost:5173?tiktok_auth=error&message={str(e)}')

@auth_bp.route('/status', methods=['GET'])
def auth_status():
    """Verificar o status de autenticação"""
    try:
        google_authenticated = 'google_credentials' in session
        tiktok_authenticated = 'tiktok_credentials' in session
        
        return jsonify({
            'google_authenticated': google_authenticated,
            'tiktok_authenticated': tiktok_authenticated
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Fazer logout de todas as plataformas"""
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Logout realizado com sucesso'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/user-info', methods=['GET'])
def get_user_info():
    """Obter informações do utilizador autenticado"""
    try:
        user_info = {}
        
        # Informações do Google
        if 'google_credentials' in session:
            try:
                creds = Credentials.from_authorized_user_info(session['google_credentials'])
                service = build('youtube', 'v3', credentials=creds)
                
                # Obter informações do canal
                channels_response = service.channels().list(
                    part='snippet,statistics',
                    mine=True
                ).execute()
                
                if channels_response['items']:
                    channel = channels_response['items'][0]
                    user_info['google'] = {
                        'channel_id': channel['id'],
                        'channel_title': channel['snippet']['title'],
                        'subscriber_count': channel['statistics'].get('subscriberCount', 0)
                    }
            except Exception as e:
                user_info['google'] = {'error': str(e)}
        
        # Informações do TikTok
        if 'tiktok_credentials' in session:
            user_info['tiktok'] = {
                'authenticated': True,
                'note': 'TikTok API requer aprovação para acesso completo'
            }
        
        return jsonify(user_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

