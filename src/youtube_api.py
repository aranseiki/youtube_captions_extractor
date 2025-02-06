from requests import get, post


def check_token_scopes(access_token):
    import requests

    URL = 'https://www.googleapis.com/oauth2/v1/tokeninfo'
    response = requests.get(URL, params={'access_token': access_token})
    return response.json()


def download_caption(
    url: str,
    access_token: str,
) -> dict:
    import requests

    # Cabeçalhos da requisição
    HEADERS = {
        'Authorization': f'Bearer {access_token}',  # Usa o token OAuth
        'Accept': 'application/x-subrip',  # Define o formato SRT
    }
    # Parâmetros para especificar o formato
    PARAMS = {'tfmt': 'srt'}
    # Faz a requisição GET
    response = requests.get(url, headers=HEADERS, params=PARAMS)
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        captiona_srt = response.text
        status = 'OK'
        status_code = response.status_code
        content = captiona_srt
    else:
        status = 'ERROR'
        status_code = response.status_code
        content = response.text
    return {'status': status, 'status_code': status_code, 'content': content}


def get_caption_url(caption_id: str, api_key: str) -> str:
    host = 'https://www.googleapis.com/youtube/v3/captions/'
    caption_id_parameter = f'{caption_id}?tfmt=srt'
    api_key_parameter = f'key={api_key}'
    url = '&'.join(((host + caption_id_parameter), api_key_parameter))
    return url


def get_id_caption_video(captions_data: dict) -> list[dict[str, str]]:
    caption_list = []
    for current_caption in captions_data['items']:
        caption_id = current_caption['id']
        caption_language = current_caption['snippet']['language']
        caption_track_kind = current_caption['snippet']['trackKind']

        caption_data = {
            'caption_id': str(caption_id),
            'caption_language': caption_language,
            'caption_track_kind': caption_track_kind,
        }

        caption_list.append(caption_data)

    return caption_list


def get_google_oauth_token(
    client_id: str,
    client_secret: str,
    access_token: str,
):
    import requests

    # Substitua pelos seus valores
    TOKEN_URL = 'https://oauth2.googleapis.com/token'
    # Dados da requisição
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': access_token,
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
    }
    # Fazendo a requisição
    response = requests.post(TOKEN_URL, data=payload)
    # Exibir o resultado
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        access_token_dict = {'AccessToken', access_token, 'TokenStatus', 'OK'}
    else:
        access_token_dict = {
            'AccessToken',
            response.text,
            'TokenStatus',
            'ERROR',
        }
    return access_token_dict


def get_google_oauth_token_via_browser_autentication(token_file_path: str):
    from google_auth_oauthlib.flow import InstalledAppFlow

    # Definir os escopos necessários
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    # Inicializar o fluxo de autenticação
    flow = InstalledAppFlow.from_client_secrets_file(token_file_path, SCOPES)
    creds = flow.run_local_server(port=0, authorization_prompt_message=None)
    # Token de acesso
    return {'AccessToken', creds.token}


def get_google_oauth_refresh_token(token_file_path: str):
    from google_auth_oauthlib.flow import InstalledAppFlow

    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    flow = InstalledAppFlow.from_client_secrets_file(token_file_path, SCOPES)
    creds = flow.run_local_server(port=0, authorization_prompt_message=None)
    tokens = {
        'access_token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_expiry': creds.expiry.isoformat(),
    }
    return tokens


def get_url(video_id: str, api_key: str) -> str:
    host = 'https://www.googleapis.com/youtube/v3/captions?part=snippet'
    videoId_parameter = f'videoId={video_id}'
    api_key_parameter = f'key={api_key}'
    url = '&'.join((host, videoId_parameter, api_key_parameter))

    return url


def get_youtube_captions(video_id: str, api_key: str) -> dict:
    url = get_url(video_id, api_key)
    response = get(url)

    return response.json()


def refresh_access_token(
    client_id: str,
    client_secret: str,
    refresh_token: str,
):
    TOKEN_URL = 'https://oauth2.googleapis.com/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }
    response = post(TOKEN_URL, data=payload)
    if response.status_code == 200:
        new_access_token = response.json().get('access_token')
        status = 'OK'
    else:
        status = 'ERROR'
    token_data = {'token_data': response.json(), 'status': status}
    return token_data
