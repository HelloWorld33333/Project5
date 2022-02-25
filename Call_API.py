import requests
import json

class BSER_Client:
    def __init__(self):
        self.api_key = 'RVqff0ugtLe0H910f5my7TD1B178Rig8JoYKQurf'
        self.version = 'v1'
        self.api_url = f'https://open-api.bser.io/{self.version}'

    @property
    # Accept와 Api key를 반환하는 인스턴스
    def http_header(self):
        return {
            'Accept': 'application/json',
            'X-API-Key': self.api_key,
        }

    # 사용자 닉네임을 통해 사용자 번호를 반환하는 인스턴스  
    def get_user_num(self, user_nickname):
        url = f'{self.api_url}/user/nickname/'
        r = requests.get(url, headers = self.http_header, params = {('query', user_nickname),})
        r_json = r.json()
        user_num = r_json['user']['userNum']
        return user_num
        
    # 사용자 번호와 시즌 번호를 통해 사용자의 모든 게임 정보를 반환
    def get_user_stats(self, user_num, season_id):
        url = f'{self.api_url}/user/stats/{user_num}/{season_id}'
        r = requests.get(url, headers=self.http_header)
        r_json = r.json()
        return r_json
            
    # 사용자 번호를 통해 사용자의 최근 90일 간의 게임 중 10개의 기록을 반환
    def get_user_games(self, user_num):
        url = f'{self.api_url}/user/games/{user_num}'
        r = requests.get(url, headers=self.http_header)
        r_json = r.json()
        return r_json
            
