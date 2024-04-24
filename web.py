from flask import Flask, redirect, url_for, render_template
from flask import Flask,render_template,request
import secrets
import random

app = Flask(__name__, static_url_path='', static_folder='static')

# HOME
@app.route("/")
def home():
    return render_template("index.html")

# HUMAN READABLE TIME
@app.route("/humantime", methods=["GET", "POST"])
def human_time():
    if request.method == 'POST':
        seconds = request.form["text"]
        seconds = int(seconds)
        error = ""
        
        # YEARS
        if seconds >= 1:
            years = seconds // 31536000
            amountleft = years * 31536000
            if years == 1:
                years = (f"{years} year")
            elif years == 0:
                years = ""
            else:
                years = (f"{years} years")

            # DAYS
            days = seconds - amountleft
            days = days // 86400
            amountleft2 = days * 86400
            if days == 1:
                days = (f"{days} day")
            elif days == 0:
                days = ""
            else:
                days = (f"{days} days")

            # HOURS
            hours = seconds - amountleft2 - amountleft
            hours = hours // 3600
            amountleft3 = hours * 3600
            if hours == 1:
                hours = (f"{hours} hour")
            elif hours == 0:
                hours = ""
            else:
                hours = (f"{hours} hours")

            # MINUTES
            minutes = seconds - amountleft3 - amountleft2 - amountleft
            minutes = minutes // 60
            if minutes == 1:
                minutes = (f"{minutes} minute")
            elif minutes == 0:
                minutes = ""
            else:
                minutes = (f"{minutes} minutes")

            # SECONDS
            workout_seconds = seconds - amountleft3 - amountleft2 - amountleft
            workout_seconds = workout_seconds % 60
            if workout_seconds == 1:
                workout_seconds = (f"{workout_seconds} second")
            elif workout_seconds == 0:
                workout_seconds = ""
            else:
                workout_seconds = (f"{workout_seconds} seconds")

            return render_template("humantime.html",error = error, seconds = seconds, years = years, amountleft = amountleft, days = days, amountleft2 = amountleft2, amountleft3 = amountleft3, hours = hours, minutes = minutes, workout_seconds = workout_seconds)
        else:
            error = "Please enter second(s) 1 or greater"
            return render_template("humantime.html", error = error)
    else:
        return render_template("humantime.html")
    
# PASSWORD GENERATOR
@app.route("/passwordgenerator", methods=["GET", "POST"])
def password_generator():
    if request.method == 'POST':

        # DEFAULTS
        length = 14
        join_password = ""
        password = ""
        
        char1 = "abcdefghijklmnopqrstuvwxyz"
        char2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        char3 = "1234567890"
        char4 = "!?£$%*/"

        join_password = char1 + char2

        # NUMBERS IN PASSWORD
        if request.form.get("numbers"):
            numbers = True
            join_password = join_password + char3
        else:
            numbers = False

        # SPECIAL CHARACTERS IN PASSWORD
        if request.form.get("special"):
            specials = True
            join_password = join_password + char4
        else:
            specials = False

        # LENGTH OF PASSWORD
        if request.method == 'POST':
            length = request.form["lenslider"]
            length = int(length)
    
        # LOOP UNTIL PASSWORD REQUIREMENTS ARE MET
        while True:
            password = ''.join(secrets.choice(join_password) for _ in range (length))
            if (numbers == True and specials == False and any(char in char1 for char in password) and any(char in char2 for char in password) and any(char in char3 for char in password)):
                break
            if (specials == True and numbers == False and any(char in char1 for char in password) and any(char in char2 for char in password) and any(char in char4 for char in password)):
                break
            if (numbers and specials == True and any(char in char1 for char in password) and any(char in char2 for char in password) and any(char in char3 for char in password) and any(char in char4 for char in password)):
                break
            if numbers == False and specials == False and any(char in char1 for char in password) and any(char in char2 for char in password):
                break

        return render_template("passwordgenerator.html", join_password = join_password, password = password, char1 = char1, char2 = char2, char3 = char3, char4 = char4, specials = specials, numbers = numbers, length = length)
    else:
        return render_template("passwordgenerator.html")
    
# BITLOCKER GENERATOR
@app.route("/bitlockergenerator", methods=["GET", "POST"])
def bitlocker():
    if request.method == 'POST':

        # DEFAULTS
        bitlockerlength = 8
        bitlockernumbers = "1234567890"

        # START WITH 469 CHECKBOX
        if request.form.get("bitlockerstart"):
            bitlockerstart = True
        else:
            bitlockerstart = False

        # LENGTH OF BITLOCKER PASSWORD
        if request.method == 'POST':
            bitlockerlength = request.form["bitlockerlenslider"]
            bitlockerlength = int(bitlockerlength)

        # IF 469 BOX TICKED ADD THAT TO START OTHERWISE RANDOM NUMBERS
        if bitlockerstart == True:
            bitlocker = "469" + ''.join(secrets.choice(str(bitlockernumbers)) for _ in range (bitlockerlength-3))
        else:
            bitlocker = ''.join(secrets.choice(str(bitlockernumbers[2::])) for _ in range (bitlockerlength))

        return render_template("bitlockergenerator.html", bitlockerstart = bitlockerstart, bitlocker = bitlocker)
    else:
        return render_template("bitlockergenerator.html")

# GUESS THE NUMBER GAME
@app.route("/guessthenumber", methods=["GET", "POST"])
def guessthenumber():
    # DEFAULTS
    if request.method == 'POST':
        player1 = request.form['player1box']
        player2 = request.form['player2box']

        random_number = random.randint(1,100)

        maths_player_1 = abs(int(player1) - random_number)
        maths_player_2 = abs(int(player2) - random_number)

        if maths_player_1 < maths_player_2:
            if player1 == random_number:
                result = f"Player 1 wins the number was {random_number} and guessed it exactly, have 5 points :)!"
            else:
                result = f"Player 1 wins, the number was {random_number} and guessed {maths_player_1} away"
        else:
            if player2 == random_number:
                result = f"Player 2 wins the number was {random_number} and guessed it exactly, have 5 points :)!"
            else:
                result = f"Player 2 wins, the number was {random_number} and guessed {maths_player_2} away"

        '''
        if player1.isdigit() == False:
            result = "Please enter a number player 1"
        elif int(player1) < 1 or int(player1) > 100:
            result = "Please enter a number between 1-100 player 1"

        if player2.isdigit() == False:
            result = "Please enter a number player 2"
        elif int(player2) < 1 or int(player2) > 100:
            result = "Please enter a number between 1-100 player 2"
        '''

        if player1 == player2:
            result = "You must enter different numbers"

        return render_template("guessthenumber.html", random_number = random_number, player1 = player1, player2 = player2, result = result, maths_player_1= maths_player_1, maths_player_2 = maths_player_2)
    else:
        return render_template("guessthenumber.html")
    
# ROCK PAPER SCISSORS
@app.route("/rockpaperscissors", methods=["GET", "POST"])
def rps():
    if request.method == 'POST':

        user_choice_rock = request.form.get('rock')
        user_choice_paper = request.form.get('paper')
        user_choice_scissors = request.form.get('scissors')

        rules_win = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }

        all_choices = ["rock", "paper", "scissors"]
        computer_random_number = random.randint(0,2)
        computer_random_choice = all_choices[computer_random_number]

        rps_result = ""
        if user_choice_rock:
            user_choice_rock = all_choices[0]
            if user_choice_rock == computer_random_choice:
                rps_result = f"Computer chose {computer_random_choice} it's a draw!"
            elif user_choice_rock == rules_win[computer_random_choice]:
                rps_result = f"Computer chose {computer_random_choice} you lose!"
            else:
                rps_result = f"Computer chose {computer_random_choice} you win!"

        if user_choice_paper:
            user_choice_paper = all_choices[1]
            if user_choice_paper == computer_random_choice:
                rps_result = f"Computer chose {computer_random_choice} it's a draw!"
            elif user_choice_paper == rules_win[computer_random_choice]:
                rps_result = f"Computer chose {computer_random_choice} you lose!"
            else:
                rps_result = f"Computer chose {computer_random_choice} you win!"

        if user_choice_scissors:
            user_choice_scissors = all_choices[2]
            if user_choice_scissors == computer_random_choice:
                rps_result = f"Computer chose {computer_random_choice} it's a draw!"
            elif user_choice_scissors == rules_win[computer_random_choice]:
                rps_result = f"Computer chose {computer_random_choice} you lose!"
            else:
                rps_result = f"Computer chose {computer_random_choice} you win!"

        return render_template("rockpaperscissors.html", all_choices = all_choices, user_choice_rock = user_choice_rock, user_choice_paper = user_choice_paper, user_choice_scissors = user_choice_scissors, rules_win = rules_win, computer_random_number = computer_random_number, computer_random_choice = computer_random_choice, rps_result = rps_result)
    else:
        return render_template("rockpaperscissors.html")

# COMMAR SEPERATOR
@app.route("/seperator", methods=["GET", "POST"])
def seperator():

    # DEFAULTS
    user_input = ""
    user_input_split = []
    result = ""
    speechse = '"'
    space = False
    speech = False

    # GET HTML FORM
    if request.method == 'POST':
        user_input = request.form["seperator"]
        user_input_split = user_input.split()

        # GET SPACE CHECKBOX
        if request.form.get("comspace"):
            space = True

        if request.form.get("speechmarks"):
            speech = True

        if space == True:
            result = (", ").join(user_input_split)
        elif speech == True:
            result = (speechse) + ('","').join(user_input_split) + (speechse)
        else:
            result = (",").join(user_input_split)

        if space == True and speech == True:
            result = (speechse) + ('", "').join(user_input_split) + (speechse)

    return render_template("seperator.html", user_input = user_input, result = result, user_input_split = user_input_split, speechse = speechse, space = space, speech = speech)

# ABOUT 
@app.route("/about")
def about():
    return render_template("about.html")

# ERROR 404 PAGE
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)