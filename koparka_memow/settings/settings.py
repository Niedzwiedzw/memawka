with open('access_token.txt') as f:
    accessToken = f.read()

SETTINGS = {
    'groupID': 987425344635130,
    'postsLimit': 1,
    'accessToken': accessToken
}
