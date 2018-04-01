import quizduell
import os
import json
import time
import random
import sys
import getpass

# Own modules
from gamestate import GameState
import settings

#
# ---------------------- Functions --------------------------
#
# fetches all open games and stores them in GameStates each
def getAllGames():
    openGameStates = [] # empty array

    # retrieve open games from api
    openGames = settings.api.current_user_games()

    while settings.validateResult(openGames) != True:
        openGames = settings.api.current_user_games()

    # retrieve games dictionary from json string
    games = json.loads(json.dumps(openGames))['user']['games']

    # iterrate over every game
    
    for key in games:
        # Parse json into GameState object
        gamestate = GameState(key)

        # add new gamestate to openGames
        openGameStates.append(gamestate)

    # return gameStates
    return openGameStates

# Makes gamestates human readable
def convertGameState( gamestate ):
    if gamestate == 0:
        return "(0) Game has not been accepted yet"
    elif gamestate == 1:
        return "(1) Ongoing"
    elif gamestate == 2:
        return "(2) Finished"
    elif gamestate == 6:
        return "(6) Finished, Opponent ran out of time"
    else:
        return "(" + str(gamestate) + ") State unknown"

# Prints detailed info about a single game
def printGameInfo( game, extremlyDetailed=False ):
    print("[" + ('%02d' % settings.allGames.index(game)) + "] Playing against: " + game.opponent_name)
    print("     Elapsed (min)  : " + str(game.elapsed_min))
    print("     Score          : " + ('%02d' % game.getPlayerScore()) + " : " + ('%02d' % game.getOpponentScore()))
    print("     Your Turn      : " + str(game.your_turn))
    print("     State          : " + convertGameState(game.state))

    # Print detailed info if requested about games that are playable
    if game.your_turn == True and extremlyDetailed == True:
        print "     Questions:"
        game.game_info.printDetails()

# Prints game information
def printGamesInfo( onlyPlayable=False, onlyOpen=False ):
    openGameFound = False

    if len(settings.openGames) > 0:
        if onlyPlayable == False:
            print "You have these open games:"
        else:
            print "It's your turn in these games:"
    for openGame in settings.openGames:
        if onlyPlayable == True:
            if openGame.your_turn == False:
                continue
            
        openGameFound = True
        printGameInfo(openGame) 
    
    if openGameFound == False:
        if onlyPlayable == True:
            print("Could not find any playable Games atm. Come back later please")
        else:
            print("Could not find any open Games.")
        
    if onlyPlayable == False and onlyOpen == False:
        if len(settings.finishedGames) > 0:
            print "\n\nYou have these finished games:\n"
            for finishedGame in settings.finishedGames:
                printGameInfo(finishedGame)
        else:
            print "You have no finished games."
        

# Sorts games from settings.allGames into settings.openGames and settings.finishedGames
def sortGamesFromAllGames():
    settings.openGames = []
    settings.finishedGames = []

    for game in settings.allGames:
        if game.state == 2 or game.state == 5 or game.state == 6:
            settings.finishedGames.append(game)
        else:
            settings.openGames.append(game)

# Updates openGames list and prints it to the screen
def fetchGamesInfo():
    # Fetch open and finished games
    settings.allGames = getOpenGames()

    # Store in separate data structures
    sortGamesFromAllGames()


# Hacky line clearing
def clear():
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()
    
# Plays the game. let's user select how many questions should be answered correctly
def agentPlayGame( gameToBePlayed ):
    # Error checking
    if gameToBePlayed.your_turn == False:
        print("Error! It's not my turn!")
        return

    # TODO Get questions that will come up next and categories for decision which category to choose
    # gameToBePlayed.printDetails()

    # TODO: more sophisticated technique for the follwing
    # Calculate amount of answers that need to be given
    answers = gameToBePlayed.your_answers
    answersCount = 0
    if (len(answers) == 0 and len(gameToBePlayed.opponent_answers) == 0) or len(answers) == 5 * 3:
        # First turn or last round
        answersCount = 3
    else:
        # Any other round
        answersCount = 6

    # give answers based on percentage chance
    correctAnswers = 0
    for x in range(0, answersCount):
        # determin whether bot will give correct answer
        chanceCeiling = 55 # default difficulty, TODO: rework
        if gameToBePlayed.opponent_name in settings.opponents:
            chanceCeiling = int(settings.opponents[gameToBePlayed.opponent_name])
        
        chanceNumber = random.randint(0,100)       
        if chanceNumber < chanceCeiling:
            answers.append(0)
            correctAnswers += 1
        else:
            # choose random wrong answer
            answers.append(random.randint(1,3))
    
    # TODO: sophisticated category choice
    cat_choice = 0

    # Output result
    sys.stdout.write("[" + str(gameToBePlayed.opponent_name) + "] will give " + str(correctAnswers) + "/" + str(answersCount) + " correct answers. New Score: " + str(gameToBePlayed.getPlayerScore()) + ":" + str(gameToBePlayed.getOpponentScore()))
    sys.stdout.flush()
    time.sleep(2)
    #clear()
    
    # Upload result
    settings.api.upload_round_answers(gameToBePlayed.game_id, answers, cat_choice)

# Retrieves uid of a given user
def getUID( name ):
    return json.loads(json.dumps(settings.api.find_user(name), indent=3))['u']['user_id']

# Parses requests_file
def readRequestsContent( requests_file ):
    # Load file into list
    with open(requests_file) as f:
        requests_content = f.readlines()
        f.close()

    # Strip requests_content of '\n'
    requests_content = [x.strip('\n') for x in requests_content]

    # Add each player to dictionary with their difficulty setting
    settings.opponents.clear()
    for player in requests_content:
        player = player.split("=",2)
        settings.opponents.update({player[0] : player[1]})

def requestAndAcceptGames():
    # fetch games
    settings.allGames = getAllGames()
    sortGamesFromAllGames()

    # look at all open ones that have not yet been accepted, accept them
    for game in settings.openGames:
        if game.state == 0 and game.your_turn:
            if not 'true' in json.dumps(settings.api.accept_game(game.game_id)):
                print "Could not accept game\n"
                #settings.loggedIn = False
                #settings.authenticateUser()

    # look at all requests that we should make and see whether we already have a game with that player
    for key in settings.opponents:
        hasGame = False
        for game in settings.openGames:
            if game.state == 1: # Ongoing game
               if game.opponent_name == key:
                   hasGame = True
                   break

        if hasGame == False:
            # Request new game with that user
            settings.api.start_game(getUID(key))

    # Wait for REST to catch up
    time.sleep(2)

def printScore( opponent ):
    for game in settings.openGames:
        if game.opponent_name == opponent:
            sys.stdout.write(": " + str(game.getOpponentScore()) + "; Me: " + str(game.getPlayerScore()))
            break

def botLoop():
    while True:
        # Clear log
        sys.stdout.write("new round...")
        #clear()
            
        # Fetch all players that the Bot should request
        readRequestsContent('should_request.bot')

        # Look at requested games and accept them while also sending out request to players that we're not playing with yet
        requestAndAcceptGames()

        # Search through all open games that we can play and play them
        for game in settings.openGames:
            if game.state == 1 and game.your_turn == True:
                agentPlayGame(game)

                # Wait for REST to catch up
                time.sleep(2)
                continue

        # 3 hour Delay to make sure bot does not burn cpu resources. This is handled in this way to make keyboardinterrupts possible
        sys.stdout.write("Sleeping: ")
        delayTime = 60 * 2
        for x in range(0, delayTime):
            clear()
            # Display progress bar
            sys.stdout.write("Sleeping: " + "{:03.2f}".format(100.0 * (float(x) / float(delayTime))) + " %\n")
            for opponent in settings.opponents:
                sys.stdout.write("Request-Opponent: " + opponent + "[" + settings.opponents[opponent] + "]\n")

            for game in settings.openGames:
                sys.stdout.write("OpenGame; " + game.opponent_name)
                printScore(game.opponent_name)
                sys.stdout.write("\n")
            sys.stdout.flush()
            time.sleep(1)

def main():
    print "Welcome to Quizduell bot! Running in background"
    settings.init()

    try:
        botLoop()
    except KeyboardInterrupt:
        print "Exiting..."


#
# ---------------------- Code entry point --------------------------
#
main()
