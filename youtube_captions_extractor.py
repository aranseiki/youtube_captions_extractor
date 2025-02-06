from py_rpautom.python_utils import cls, ler_variavel_ambiente

from src.youtube_api import (
    download_caption,
    get_caption_url,
    get_google_oauth_refresh_token,
    get_id_caption_video,
    get_youtube_captions,
    refresh_access_token,
)

video_id = 'JylmVV2OdJQ'
api_key = ler_variavel_ambiente(
    nome_variavel='YOUTUBECAPTIONSEXTRACTOR_API_KEY',
    variavel_sistema=True,
)
client_id = ler_variavel_ambiente(
    nome_variavel='CLIENT_ID_API_KEY',
    variavel_sistema=True,
)
client_secret = ler_variavel_ambiente(
    nome_variavel='CLIENT_SECRET_API_KEY',
    variavel_sistema=True,
)

# breakpoint()

captions_data = get_youtube_captions(video_id=video_id, api_key=api_key)

caption_list = get_id_caption_video(captions_data=captions_data)

caption_id = caption_list[0]['caption_id']

url_caption = get_caption_url(caption_id=caption_id, api_key=api_key)

token_file_path = r'C:\dev\projects\Users\aoalmeida2\youtube_captions_extractor\docs\client_secret.json'
save_token_file_path = r'C:\dev\projects\Users\aoalmeida2\youtube_captions_extractor\docs\token.json'

token_data = get_google_oauth_refresh_token(token_file_path=token_file_path)

access_token = token_data['access_token']
refresh_token = token_data['refresh_token']
token_expiry = token_data['token_expiry']

print(download_caption(url=url_caption, access_token=access_token))

new_token_data = refresh_access_token(
    client_id=client_id,
    client_secret=client_secret,
    refresh_token=refresh_token,
)

access_token = new_token_data['token_data']['access_token']
expires_in = new_token_data['token_data']['expires_in']
print(download_caption(url=url_caption, access_token=access_token))
