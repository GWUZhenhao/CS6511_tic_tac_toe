import requests
import json
import numpy as np

class operation:
    def __init__(self, teamId):
        self.files = [
        ]
        self.headers = {
            'x-api-key': 'ca8eb275449c03fd1f5f',
            'userId': '1111',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'PostmanRuntime/7.29.0'
        }
        self.teamId = teamId

    def get_my_team(self):
        url = 'https://www.notexponential.com/aip2pgaming/api/index.php?type=myTeams'
        payload = {}

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)
        return dict_response

    def create_a_game(self, opponent):
        url = 'https://www.notexponential.com/aip2pgaming/api/index.php'
        payload = {
            'type': 'game',
            'teamId1': self.teamId,
            'teamId2': opponent,
            'gameType': 'TTT'
        }

        response = requests.request("POST", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)
        return dict_response

    def get_my_games(self):
        url = 'https://www.notexponential.com/aip2pgaming/api/index.php?type=myGames'
        payload = {}

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)
        return dict_response

    def make_a_move(self, gameId, move):
        url = 'https://www.notexponential.com/aip2pgaming/api/index.php'
        payload = {
            'teamId': self.teamId,
            'move': move,
            'type': 'move',
            'gameId': gameId
        }

        response = requests.request("POST", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)
        return dict_response

    def get_moves(self, gameId, count):
        url = 'https://www.notexponential.com/aip2pgaming/api/index.php?type=moves&gameId={}&count={}'.format(gameId, count)
        payload = {}

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)

        moveIds = []
        teamIds = []
        symbols = []
        moveXs = []
        moveYs = []
        for i in range(len(dict_response['moves'])):
            moveIds.append(dict_response['moves'][i]['moveId'])
            teamIds.append(dict_response['moves'][i]['teamId'])
            symbols.append(dict_response['moves'][i]['symbol'])
            moveXs.append(dict_response['moves'][i]['moveX'])
            moveYs.append(dict_response['moves'][i]['moveY'])

        moveIds = np.asarray(moveIds)
        teamIds = np.asarray(teamIds)
        symbols = np.asarray(symbols)
        moveXs = np.asarray(moveXs)
        moveYs = np.asarray(moveYs)

        return moveIds, teamIds, symbols, moveXs, moveYs

    def get_board_string(self, gameId):
        url = 'https://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId={}'.format(gameId)
        payload = {}

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)
        return dict_response

    def get_board_map(self, gameId):
        url = 'https://www.notexponential.com/aip2pgaming/api/index.php?type=boardMap&gameId={}'.format(gameId)
        payload = {}

        response = requests.request("GET", url, headers=self.headers, data=payload, files=self.files)
        dict_response = json.loads(response.text)

        output = dict_response['output'].split('"')
        #print(output)
        keys = [] # loaction [x,y]
        values = [] # 1 or 2 or 0
        for i in range(int((len(output) - 1) / 4)):
            keys.append(output[i * 4 + 1])
            if output[i * 4 + 3] == 'O':
                values.append(1)
            else:
                values.append(2)

        loc = []
        for i in range(len(keys)):
            loc.append(keys[i].split(','))
            loc[i][0] = int(loc[i][0])
            loc[i][1] = int(loc[i][1])

        values = np.asarray(values)
        loc = np.asarray(loc)


        return loc, values
