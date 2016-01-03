import cookielib
import quizduell
import os
import getpass
import time

# define globals and init those that can be initialized to none None value
api = None
loggedIn = False
clear = lambda: os.system('clear')
cookie_jar = None
allGames = None
openGames = None
finishedGames = None
opponents = {}

# checks result and returns whether or not the user is still authenticated
# reauthenticates if not. Recall api after failed attempt
def validateResult( result ):
    global loggedIn
    if 'access' in result: # TODO: lazy approach that might break in the future
        print "could not log in for reason:"
        print result

        # Session invalid, re-login
        loggedIn = False
        authenticateUser()
        return False
        
    return True

# authenticates user with quizduell api
def authenticateUser( username=None, password=None ):
    global loggedIn
    global api
    global cookie_jar
    global clear
    
    while loggedIn != True:
        # ask for username
        if username == None:
            username = raw_input("Username: ")

        # ask for password
        if password == None:
            password = getpass.getpass()
        
        # try to authenticate with credentials. Retry until login succeeds
        loggedIn = validateResult(api.login_user(username, password))

        if loggedIn == False:
            print("Username and/or password wrong. Please retry!")
            username = None
            password = None
            continue

        # Reload api from cookie_jar
        api = quizduell.QuizduellApi(cookie_jar)

        # Store authenticated session in file
        print("Saving cookie file to hard disk")
        time.sleep(2)
        cookie_jar.save()
        clear()

def init():
    global api
    global cookie_jar

    # Setup globals    
    cookie_jar = cookielib.MozillaCookieJar('cookie.keks')
    api = quizduell.QuizduellApi(cookie_jar)

    # try to load cookie session
    if os.access(cookie_jar.filename, os.F_OK):
        cookie_jar.load()
        loggedIn = True
    else:
        authenticateUser()
    
    
