import json

# Custom modules
import settings
from question import Question

class GameInfo:
    'This container Class stores detailed information about a quizduell game'

    def __init__(self, game_id, dicVal=None):
        self.questions = None
        self.image_questions = None
        self.game_id = game_id;

        if dicVal != None:
            self.parseQuestions(dicVal['questions'])
            self.parseImageQuestions(dicVal['image_questions'])

    def fetchQuestions(self):
        if self.questions == None:
            self.questions = []
            self.image_questions = []
        
            self.parseQuestions(json.loads(json.dumps(settings.api.get_game(self.game_id)))['game']['questions'])
            self.parseImageQuestions(json.loads(json.dumps(settings.api.get_game(self.game_id)))['game']['image_questions'])

    def printDetails(self):
        self.fetchQuestions()
        
        for question in self.questions:
            question.printDetails()

        print "Image questions not implemented!"

    def parseQuestions(self, questionsDic):
        for question in questionsDic:
            self.questions.append(Question(question))

    def parseImageQuestions(self, imageQuestionsDic):
        print "Image questions not implemented!"
