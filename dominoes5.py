import random

def display(stock_pieces, computer_pieces, player_pieces, domino_snake, status):
    status_message = ""
    if status == "player":
        status_message = "It's your turn to make a move. Enter your command."
    elif status == "computer":
        status_message = "Computer is about to make a move. Press Enter to continue..."
    else:
        if len(player_pieces) == 0:
            status_message = "The game is over. You won!"
        elif len(computer_pieces) == 0:
            status_message = "The game is over. The computer won!"
        else:
            status_message = "The game is over. It's a draw!"

    snake = ""
    if len(domino_snake) <= 6:
        for domino in domino_snake:
            snake += str(domino)
    else:
        for i in range(0, 3):
            snake += str(domino_snake[i])
        snake += "..."
        for i in range(len(domino_snake) - 3, len(domino_snake)):
            snake += str(domino_snake[i])

    print("======================================================================")
    print("Stock size:", len(stock_pieces))
    print("Computer pieces:", len(computer_pieces))
    print()
    print(snake)
    print()
    print("Your pieces:")
    for i in range(len(player_pieces)):
        print(str(i + 1) + ":" + str(player_pieces[i]))
    print()
    print("Status:", status_message)

def is_legal(index, my_pieces, domino_snake):
    if index > 0:
        snake_domino = domino_snake[len(domino_snake) - 1]
        my_domino = my_pieces[index - 1]
        if snake_domino[1] in my_domino:
            return True
    elif index < 0:
        snake_domino = domino_snake[0]
        my_domino = my_pieces[abs(index) - 1]
        if snake_domino[0] in my_domino:
            return True
    else:
        return True

    return False

def player_input(player_pieces, domino_snake):
    while True:
        number = input()
        if number[0] == "-":
            if not number[1::].isnumeric():
                print("Invalid input. Please try again.")
                continue
        else:
            if not number.isnumeric():
                print("Invalid input. Please try again.")
                continue
        index = int(number)    
        if abs(index) not in range(0, len(player_pieces) + 1):
            print("Invalid input. Please try again.")
            continue
        if not is_legal(index, player_pieces, domino_snake):
            print("Illegal move. Please try again.")
            continue
        return index

def computer_tactics(computer_pieces, domino_snake, stock_pieces_size):
    counts = [0] * 8
    for domino in computer_pieces:
        counts[domino[0]] += 1
        counts[domino[1]] += 1
    for domino in domino_snake:
        counts[domino[0]] += 1
        counts[domino[1]] += 1   

    scores = {}
    for i in range(1, 7):
        for j in range(1, 7):
            if i >= j:
                continue
            scores[(i, j)] = counts[i] + counts[j]

    large_scores = []
    for i in range(0, min(3, stock_pieces_size)):
        maxkey = max(scores, key=scores.get)
        large_scores.append(maxkey)
        del scores[maxkey]

    for score in large_scores:
        scoreL = list(score)
        if scoreL not in computer_pieces:
            continue
        index = computer_pieces.index(scoreL)
        if is_legal(index, computer_pieces, domino_snake):
            return index
        if is_legal(-index, computer_pieces, domino_snake):
            return -index
    return 0

def computer_input(computer_pieces, domino_snake, stock_pieces_size):
    index = computer_tactics(computer_pieces, domino_snake, stock_pieces_size)

    if stock_pieces_size == 0:
        for index in range(1, len(computer_pieces)):
            if is_legal(index, computer_pieces, domino_snake):
                return index
        return 0        
    while True:
        index = random.randint(0, len(computer_pieces))
        if not is_legal(index, computer_pieces, domino_snake):
            continue
        return index

def adjust_last_domino_snake(domino_snake):
    last_domino = domino_snake[len(domino_snake) - 1]
    connect_domino = domino_snake[len(domino_snake) - 2]
    if connect_domino[1] != last_domino[0]:
        temp = last_domino[0]
        last_domino[0] = last_domino[1]
        last_domino[1] = temp
        domino_snake.pop()
        domino_snake.append(last_domino)

def adjust_first_domino_snake(domino_snake):
    first_domino = domino_snake[0]
    connect_domino = domino_snake[1]
    if connect_domino[0] != first_domino[1]:
        temp = first_domino[0]
        first_domino[0] = first_domino[1]
        first_domino[1] = temp
        domino_snake.pop(0)
        domino_snake.insert(0, first_domino)

random.seed(17)

pices = []
stock_pieces = []      # 14 domino elements
computer_pieces = []   # 7 or 6 domino elements
player_pieces = []     # 6 or 7 domino elements
domino_snake = []      # 1 starting domino
status = ""

no_good = True
while no_good:
    pices = []
    while len(pices) < 28:
        p1 = random.randint(0, 6)
        p2 = random.randint(0, 6)
        if p2 < p1:
            continue
        pair = [p1, p2]
        if pair in pices:
            continue
        else:
            pices.append(pair)

    stock_pieces = pices[0:14]      # 14 domino elements
    computer_pieces = pices[14:21]   # 7 or 6 domino elements
    player_pieces = pices[21:28]     # 6 or 7 domino elements
    domino_snake = []      # 1 starting domino
    status = "" 

    no_good = False
    if [6, 6] in computer_pieces:
        computer_pieces.remove([6, 6])
        domino_snake.append([6, 6])
        status = "player"
    elif [5, 5] in computer_pieces:
        computer_pieces.remove([5, 5])
        domino_snake.append([5, 5])
        status = "player"
    elif [6, 6] in player_pieces:
        player_pieces.remove([6, 6])
        domino_snake.append([6, 6])
        status = "computer"
    elif [5, 5] in player_pieces:
        player_pieces.remove([5, 5])
        domino_snake.append([5, 5])
        status = "computer"
    else:
        no_good = True
    
while len(player_pieces) > 0 and len(computer_pieces) > 0:
    display(stock_pieces, computer_pieces, player_pieces, domino_snake, status)
    if status == "player":
        move = player_input(player_pieces, domino_snake)
        if move > 0:
            domino_snake.append(player_pieces.pop(move - 1))
            adjust_last_domino_snake(domino_snake)
        elif move < 0:
            domino_snake.insert(0, player_pieces.pop(abs(move) - 1))
            adjust_first_domino_snake(domino_snake)
        else:
            if len(stock_pieces) == 0:
                break
            player_pieces.append(stock_pieces.pop(0))
        status = "computer"
    else:
        input()
        move = computer_input(computer_pieces, domino_snake, len(stock_pieces))
        if move > 0:
            domino_snake.append(computer_pieces.pop(move - 1))
            adjust_last_domino_snake(domino_snake)
        elif move < 0:
            domino_snake.insert(0, computer_pieces.pop(abs(move) - 1))
            adjust_first_domino_snake(domino_snake)
        else:
            if len(stock_pieces) == 0:
                break
            computer_pieces.append(stock_pieces.pop(0))
        status = "player"

status = "game over"
display(stock_pieces, computer_pieces, player_pieces, domino_snake, status)
   
