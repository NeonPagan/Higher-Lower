import math
import random


# checks users enter yes (y) or no (n)
def yes_no(question):
    while True:
        response = input(question).lower()

        # checks user response, questions
        # repeats if users don't enter yes / no
        if response == "yes" or response == "y":
            return "yes"
        elif response == "no" or response == "n":
            return "no"
        else:
            print("Please enter yes / no")


def instruction():
    """Displays the instructions and how to play"""
    print(''''

**** Instructions ****

To begin, choose the number of rounds and either customise
the game parameters or go with the default game (where the 
secret number will be between 1 and 100)

Then choose how many rounds you'd like to play <enter>
 for infinite mode. 

Your goal is to try to guess the secret number without 
running out of guesses 

Good Luck!
    ''')


# checks for an integer with optional upper /
# lower limits and an optional exit code for infinite mode
# / quitting game
def int_check(question, low=None, high=None, exit_code=None):
    # if any integer is allowed...
    if low is None and high is None:
        error = "Please enter an integer"

    # if the number needs to be more than an
    # integer (ie: rounds / 'high number')
    elif low is not None and high is None:
        error = (f"Please enter an integer that is "
                 f"more than / equal to {low}")

    # if the number needs to between low & high
    else:
        error = (f"Please enter an integer that"
                 f" is between {low} and {high} (inclusive")

    while True:
        response = input(question).lower()

        # check for infinite mode /exit code
        if response == exit_code:
            return response
        try:
            response = int(response)

            # Check the integer is not too low...
            if low is not None and response < low:
                print(error)

            # check response is more than the low number
            elif high is not None and response > high:
                print(error)

            # if response is valid, return it
            else:
                return response

        except ValueError:
            print(error)


# Main Routine starts here
def calc_guesses(low, high):
    num_range = high - low + 1
    max_raw = math.log2(num_range)
    max_upped = math.ceil(max_raw)
    max_guesses = max_upped + 1
    return max_guesses


# Main Routine Starts here

# Initialise game variables
mode = "regular"
rounds_played = 0
rounds_lost = 0
rounds_tied = 0

end_game = "no"
feedback = ""

game_history = []
all_scores = [0]

print("️🔺🔺🔺 Welcome to the Higher Lower Game 🔻🔻🔻")
print()

want_instructions = yes_no("Do you want to read instructions? ")

# check users enter yes (Y) or no (n)
if want_instructions == "yes":
    instruction()

# Ask user for number of rounds / infinite mode
num_rounds = int_check("Rounds <enter for infinite>: ",
                       low=1, exit_code="")

if num_rounds == "":
    mode = "infinite"
    num_rounds = 5

# ask user if they want to customise the number range
default_params = yes_no("Do you want to use the default game parameters? ")
if default_params == "yes":
    low_num = 0
    high_num = 10

# allow user to choose the high / low number
else:
    low_num = int_check("Low Number? ")
    high_num = int_check("High Number? ", low=low_num + 1)

# calculate the maximum number of guesses based on the low and high number
guesses_allowed = calc_guesses(low_num, high_num)

# Game loop starts here
while rounds_played < num_rounds:

    # if user has entered exit code, end game!!
    if end_game == "yes":
        break

    # Rounds headings (based on mode)
    if mode == "infinite":
        rounds_heading = f"\n♾️♾️♾️ Round {rounds_played + 1} (Infinite Mode)♾️♾️♾️"
    else:
        rounds_heading = f"\n💿💿💿 Round {rounds_played + 1} of {num_rounds} 💿💿💿"

    print(rounds_heading)

    # Round starts here
    # Set guesses used to zero at the start of each round
    guesses_used = 0
    already_guessed = []

    # Choose a 'secret' number between the low and high number
    secret = random.randint(low_num, high_num)
    print("Spoiler Alert", secret)  # remove this line after testing!

    guess = ""
    while guess != secret and guesses_used < guesses_allowed:

        # ask the user to guess the number...
        guess = int_check("Guess: ", low_num, high_num, "xxx")

        # check that they don't want to quit
        if guess == "xxx":
            # set end_game to use so that outer loop can be broken
            end_game = "yes"
            break

        # check that guess is not a duplicate
        if guess in already_guessed:
            print(f"You've already guessed {guess}. You've *still* used")

        if guess < secret:
            feedback = "Please enter a higher number"
        elif guess > secret:
            feedback = "Please enter a lower number"
        else:
            feedback = "Well done! You guessed the secret number"

        # check that guess is not a duplicate
        if guess in already_guessed:
            print(f"You've already guessed {guess}. You've *still* used"
                  f"{guesses_used} / {guesses_allowed} guesses")
            continue

        # if guess is not a duplicate, add it to the 'already guessed' list
        else:
            already_guessed.append(guess)

        # add one to the number of guesses used
        guesses_used += 1

        # compare the user's guess with the secret number set up feedback statement

        # If we have guesses left...
        if guess < secret and guesses_used < guesses_allowed:
            feedback = (f"Too low, please try a higher number."
                        f"You've used {guesses_used} / {guesses_allowed} guesses")
        elif guess > secret and guesses_used < guesses_allowed:
            feedback = (f"Too high, please try a lower number,"
                        f"You've used {guesses_used} / {guesses_allowed} guesses")

        # when the secret number is guessed, we have three different feedback
        # options (lucky / 'phew' / well done)
        elif guess == secret:

            if guesses_used == 1:
                feedback = "🍀🍀 Lucky! You got it on the first guess. 🍀🍀"
            elif guesses_used == guesses_allowed:
                feedback = f"Phew! You got it in {guesses_used} guesses."
            else:
                feedback = f"Well done! You guessed the secret number in {guesses_used} guesses."

         # if there are no guesses left!
        else:
            feedback = "Sorry - you have no more guesses. You lose this round!"

            # print feedback to user
        print(feedback)

        # Additional Feedback (warn user that they are running out of guesses)
        if guesses_used == guesses_allowed - 1:
            print("\n💣💣💣 Careful - you have one guess left! 💣💣💣\n")

    print()

    # Round ends here


    print()

    # Round ends here

    # if user has entered exit code, end game!!
    if end_game == "yes":
        break

    # add score to list...
    all_scores.append(guesses_used)
    rounds_played += 1

    # Add round result to game history
    history_feedback = f"Round {rounds_played}: {feedback}"
    game_history.append(history_feedback)

    # if users are in infinite mode, increase number of rounds!
    if mode == "infinite":
        num_rounds += 1

# check users have played at least one round
# before calculating statistics.
if rounds_played > 0:
    # Game History / Statistics area

    # Calculate statistics
    rounds_won = rounds_played - rounds_tied - rounds_lost
    percent_won = rounds_won / rounds_played * 100
    percent_lost = rounds_lost / rounds_played * 100
    percent_tied = 100 - percent_won - percent_lost

    # Output Game Statistics
    print("📊📊📊 Game Statistics 📊📊📊")
    print(f"👍 Won: {percent_won: 2f} \t"
          f"Lost: {percent_lost: 2f} \t"
          f"Tied: {percent_tied: 2f}")


    # Calculate statistics
    all_scores.sort()
    best_score = all_scores[0]
    worst_score = all_scores[-1]
    average_score = sum(all_scores) / len(all_scores)

    # Output the statistics
    print("\n📊📊📊 Statistics 📊📊📊")
    print(f"Best:{best_score}  |  Worst:{worst_score}  | Average:{average_score:.2f}:")
    print()

    # Display the game history on request
    see_history = yes_no("Do you want to see your game history? ")
    if see_history == "yes":
        for item in game_history:
            print(item)

else:
    print("You chickened out")
