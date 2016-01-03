import json
import settings
from gameinfo import GameInfo

class GameState:
    'This container Class stores information about a quizduell game state'
    def __init__(self, dicVal):
        
        # these must be included
        self.your_question_types        = dicVal['your_question_types']
        self.elapsed_min                = dicVal['elapsed_min']
        self.cat_choices                = dicVal['cat_choices']
        self.opponent_answers           = dicVal['opponent_answers']
        self.messages                   = dicVal['messages']
        self.your_answers               = dicVal['your_answers']
        self.state                      = dicVal['state']
        self.mode                       = dicVal['mode']
        self.is_image_question_disabled = dicVal['is_image_question_disabled']
        self.your_turn                  = dicVal['your_turn']
        self.game_id                    = dicVal['game_id']
        self.opponent_question_types    = dicVal['opponent_question_types']
        self.opponent_name              = dicVal['opponent']['name']
        self.opponent_uid               = dicVal['opponent']['user_id']
        
        # this value is lazily being fetched just in time for performance reasons
        self.game_info = GameInfo(self.game_id)
        
        # optional dicVal
        if 'rating_bonus' in dicVal:
            self.rating_bonus = dicVal['rating_bonus']
            
    def getPlayerScore(self):
        counter = 0
        for answer in self.your_answers:
            if answer == 0:
                counter += 1

        return counter
    
    def getOpponentScore(self):
        counter = 0
        for answer in self.opponent_answers:
            if answer == 0:
                counter += 1

        return counter

    def printDetails(self):
        print "Dumping GameState to Console:"
        print "your_question_types       : " + str(self.your_question_types)
        print "elapsed_min               : " + str(self.elapsed_min)
        print "cat_choices               : " + str(self.cat_choices)
        print "opponent_answers          : " + str(self.opponent_answers)
        print "messages                  : " + str(self.messages)
        print "your_asnwers              : " + str(self.your_answers)
        print "state                     : " + str(self.state)
        print "mode                      : " + str(self.mode)
        print "is_image_question_disabled: " + str(self.is_image_question_disabled)
        print "your_turn                 : " + str(self.your_turn)
        print "game_id                   : " + str(self.game_id)
        print "opponent_question_types   : " + str(self.opponent_question_types)
        print "opponent_name             : " + str(self.opponent_name)
        self.game_info.printDetails()
