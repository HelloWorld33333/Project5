import time
import Call_API
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


# 동일한 파일 내에 클래스 가져오기
bser = Call_API.BSER_Client()

# 상위권 유저
cache_rancker = ['twitch비즈류', '병원알코올도둑', '화성2', '까메베어', '강태옥', '호란이', '우김']
rancker_num = []

# 상위권 유저의 유저 넘버를 리스트에 저장
# API를 사용할 때 1초당 1개의 명령어만 사용할 수 있기 때문에 time을 사용해 딜레이 적용
for i in cache_rancker :
    rancker_num.append(bser.get_user_num(i))
    time.sleep(1)

# 인게임 데이터프레임의 column이 될 데이터
columns = ['characterLevel', 'gameRank', 'playerKill', 'monsterKill', 'bestWeaponLevel', 'masteryLevel','playTime', 'victory', 'damageToPlayer']

# 현재 시즌의 솔로 랭크 게임 모드 전적 중 특정 캐릭터만 가져와 반환하는 함수 정의
def ingame_data(user_num, columns) :
  games = bser.get_user_games(user_num)['userGames']
  count = 0

  data = []

  for i in games:
        if i['seasonId'] == 9 and i['matchingMode'] == 3 and i['matchingTeamMode'] == 1 and i['characterNum'] == 23 :
            data.append({key : value for key, value in games[count].items() if key in columns})
        
        count += 1

  return data

# 앞서 선별한 상위권 유저의 전적 정보를 담을 리스트 생성
rancker_data = []

for i in rancker_num :
    rancker_data = rancker_data + ingame_data(i, columns)
    time.sleep(1)

df = pd.DataFrame(rancker_data)

# Data 전처리
df['gameRank'] = df['gameRank'].apply(lambda x : int(x)/18)
df['masteryLevel'] = df['masteryLevel'].apply(lambda x : x['102'])

# 데이터 간의 단위의 편차가 커서 label이 될 victory 데이터를 제외하고 데이터 스케일링 적용할 예정이기에 따로 저장
vic = df['victory']

# 다름 아닌 StandardScaler 을 사용하는 이유는 같은 데이터라도 편차가 큰 데이터의 정보를 최대한 저장해야 한다고 생각해서 사용
standard_scaler = StandardScaler()
standard_scaler.fit(df)
scaler_scaled = standard_scaler.transform(df)

df_scaled = pd.DataFrame(scaler_scaled)
df_scaled.columns = columns

df_scaled['victory'] = vic

train = df_scaled.drop('victory', axis = 1)

# 유저 이름을 받아 최근 10개의 게임 전적을 가져와 반환하는 함수 정의
def user_data(user_nickname, columns) :
    user_num = bser.get_user_num(user_nickname)
    
    data = pd.DataFrame(bser.get_user_games(user_num)['userGames'])
    data['masteryLevel'] = data['masteryLevel'].apply(lambda x : x['102'])

    label = data['victory']
    data = data[columns]
    data = data.drop('victory', axis = 1)

    return data, label

model = LogisticRegression().fit(train, vic)

nickname = input("입력 : ")

print('약 ', model.score(user_data(nickname, columns)[0], user_data(nickname, columns)[1])*10, '% 확률로 게임을 승리합니다.')

