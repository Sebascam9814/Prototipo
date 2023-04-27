import redis
r = redis.Redis(host="localhost",port="6379")

#agrega a un nuevo usario y se asigna la puntuacion de 0
def addPlayer(username):
    player_score = r.zscore('leaderboard', username)
    if player_score is None:
        r.zadd('leaderboard', {username: 0})

# si el usuario gana se le suma la puntuacion
def addScore(username):
    player_score = r.zscore('leaderboard', username)
    player_score+=1
    r.zadd('leaderboard', {username: player_score})



    
# Imprime el tablero del gato

def print_board(board):
    print("-------------")
    print("| " + board[0] + " | " + board[1] + " | " + board[2] + " |")
    print("-------------")
    print("| " + board[3] + " | " + board[4] + " | " + board[5] + " |")
    print("-------------")
    print("| " + board[6] + " | " + board[7] + " | " + board[8] + " |")
    print("-------------")

#Logica para revisar si ya termino el juego 
def check_win(board):
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != ' ':
            return True

    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != ' ':
            return True

    if board[0] == board[4] == board[8] != ' ':
        return True

    if board[2] == board[4] == board[6] != ' ':
        return True

    return False

def play_game():
    board = [' ']*9
    Username1 = input("Player 1 Username: ")
    Username2 = input("Player 2 Username: ")
    addPlayer(Username1)
    addPlayer(Username2)
    top_players = r.zrevrange('leaderboard', 0, 9, withscores=True)
    print("Leaderboard:")
    for index, player in enumerate(top_players):
        print(f"{index+1}. {player[0].decode('utf-8')} - {int(player[1])} Puntos")
    player = 1
    print(Username1+" Jugador 1:X\n"+Username2+" Jugador 2: O")
    while True:
        print_board(board)
        move = int(input(f"Jugador {player}, escoge un numero de 1 a 9: ")) - 1
        if board[move] == ' ':
            if player == 1:
                board[move] = 'X'
            else:
                board[move] = 'O'
            if check_win(board):
                print_board(board)
                print(f"Felicitaciones, Jugador {player} Ganaste!")
                if player == 1:
                    addScore(Username1)
                else:
                    addScore(Username2)
                play_game()
                break
            elif ' ' not in board:
                print_board(board)
                print("Es un empate!")
                break
            player = 2 if player == 1 else 1
        else:
            print("Ya ese espacio esta asignado elige otro!!!!")

play_game()