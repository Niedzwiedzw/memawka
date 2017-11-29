import os
try:
    with open('access_token.txt', 'r') as f:
        accessToken = f.read()
except FileNotFoundError as e:
    with open('access_token.txt', 'w') as f:
        token = input("No access token. You can type it here or press [ENTER] to add it manually into\n"
                      f"{os.path.join(os.getcwd(), 'access_token.txt')}\n\n>>")
        if token:
            f.write(token)
        else:
            exit(0)

SETTINGS = {
    'groupID': 987425344635130,
    'postsLimit': 1,
    'accessToken': accessToken
}
