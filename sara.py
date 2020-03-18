import random

HANGMAN_PICS = ['''
   +---+
       |
       |
       |
      ===''', '''
   +---+
   O   |
       |
       |
      ===''', '''
   +---+
   O   |
   |   |
       |
      ===''', '''
   +---+
   O   |
  /|   |
       |
      ===''', '''
   +---+
   O   |
  /|\  |
       |
      ===''', '''
   +---+
   O   |
  /|\  |
  /    |
      ===''', '''
   +---+
   O   |
  /|\  |
  / \  |
      ===''']

song = ['Beatles', 'Nirvana', 'Coldplay', 'Linkin Park', 'Backstreet Boys', 'Spice Girls']
team = ['Philadelphia Eagles', 'New York Giants', 'Washington Redskins', 'Chicago Bears']
buildings = ['Ross Commons', 'Hagerty Library', 'Urban Eatery']

categories = [song, team, buildings]

play_game = True
guess_count = 0
incorrect_guess = []
guess_list = []
win = False


def ask_name():
    nam = input('Hi there!\nReady to play Hangman? Let''s start with a nickname.\n')
    print("Hello " + nam + "! Lets play Hangman")

    return nam


def retrieve_cat():
    numb = int(input('Pick a category. What looks interesting? (1 [Bands], 2 [Football Teams] or 3 [Drexel University '
                     'Buildings in University City)?\n'))
    if numb == 1:
        word = random.choice(categories[0])
    elif numb == 2:
        word = random.choice(categories[1])
    else:
        word = random.choice(categories[2])

    return word


def make_guess():
    guess = input('Please guess a word?\n').lower()
    while len(guess) > 1:
        guess = input('Please guess a word?\n').lower()

    if guess in guess_list:
        print('You already guess this word')
        make_guess()

    guess_list.append(guess)
    return guess.lower()


def compare_guess(word, guess, ss, rgc, gc):
    word_2 = word.replace(' ', '')
    for a in word_2:
        if a == guess:
            rgc += 1
            ss = ''
            for c in word:
                if guess == c or c in guess_list:
                    ss += c.upper() + ''
                elif c == ' ':
                    ss += ' '
                else:
                    ss += '_ '
            print('You got one right')
            return ss, rgc, gc

    print('Incorrect guesses so far\n')
    incorrect_guess.append(guess)
    for w in incorrect_guess:
        print(w)

    gc = gc + 1

    return ss, rgc, gc


def replay_game():
    reply = input('Do you want to replpay the game? (yes or no)\n').upper()
    while True:
        if reply == 'YES':
            return True
        elif reply == 'NO':
            return False

        reply = input('Please enter yes or no?\n').upper()


while play_game:
    name = ask_name()
    word_chosen = retrieve_cat().lower()
    s = ''
    for i in word_chosen:
        if i == ' ':
            s += ' '
        else:
            s += '_ '
    print('your word is: ' + s)
    word_len = len(set(word_chosen.replace(' ', '')))
    right_guess_count = 0
    print(HANGMAN_PICS[guess_count])
    while guess_count < 7:
        s, right_guess_count, guess_count = compare_guess(word_chosen, make_guess(), s, right_guess_count, guess_count)
        print('Your word is ' + s)
        if right_guess_count == word_len:
            win = True
            break

        try:
            print(HANGMAN_PICS[guess_count])
        except IndexError:
            print(HANGMAN_PICS[guess_count-1])

        win = False

    if not win:
        print("uh oh")
    else:
        print("“you won!”")

    play_game = replay_game()
    guess_count = 0
    guess_list = []
    incorrect_guess = []
