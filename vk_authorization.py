import requests


ID = '51816957'
SECRET = '2d7mzlD00uFefjBJH09D'
URL = 'https://web-app-five-rho.vercel.app'


def get_authorization_url():
    return f'https://oauth.vk.com/authorize?client_id={ID}&scope=photos&redirect_uri={URL}/callback&response_type=code'


def get_access_token_url(code):
    return f'https://oauth.vk.com/access_token?client_id={ID}&client_secret={SECRET}&redirect_uri={URL}/callback' \
           f'&code={code}'


def get_api_url(access_token, user_ids):
    return f'https://api.vk.com/method/users.get?access_token={access_token}&user_ids={user_ids}&name_case=nom&v=5.199'


def get_access_token(code):
    access_token_url = get_access_token_url(code)
    data = requests.get(url=access_token_url).json()
    access_token = data.get('access_token')
    user_id = str(data.get('user_id'))
    return access_token, user_id


def get_user_data(access_token, user_ids):
    api_url = get_api_url(access_token, user_ids)
    data = requests.get(url=api_url).json()
    return data.get('response')
