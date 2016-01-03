class Question:
    'This container Class stores information about a single question'
    def __init__(self, dicVal):
        self.answer_time = dicVal['answer_time']
        self.cat_name    = dicVal['cat_name']
        self.question_id = dicVal['q_id']
        self.timestamp   = dicVal['timestamp']
        self.cat_id      = dicVal['cat_id']
        self.question    = dicVal['question']
        self.wrong_1     = dicVal['wrong1']
        self.wrong_2     = dicVal['wrong2']
        self.wrong_3     = dicVal['wrong3']
        self.correct     = dicVal['correct']
        self.wrong_1_p   = dicVal['stats']['wrong1_answer_percent']
        self.wrong_2_p   = dicVal['stats']['wrong2_answer_percent']
        self.wrong_3_p   = dicVal['stats']['wrong1_answer_percent']
        self.correct_p   = dicVal['stats']['correct_answer_percent']

    def dumpToConsole(self):
        print "Dumping Question to Console:"
        print "answer_time: " + str(self.answer_time)
        print "cat_name   : " + str(self.cat_name)
        print "question_id: " + str(self.question_id)
        print "timestamp  : " + str(self.timestamp)
        print "cat_id     : " + str(self.cat_id)
        print "question   : " + str(self.question)
        print "wrong_1    : " + str(self.wrong_1)
        print "wrong_1_p  : " + str(self.wrong_1_p)
        print "wrong_2    : " + str(self.wrong_2)
        print "wrong_2_p  : " + str(self.wrong_2_p)
        print "wrong_3    : " + str(self.wrong_3)
        print "wrong_3_p  : " + str(self.wrong_3_p)
        print "correct    : " + str(self.correct)
        print "correct_1_p: " + str(self.correct_1_p)

    def printDetails(self):
        print "          " + self.cat_name.encode('utf-8') + ": " + self.question.encode('utf-8')
        print "          Answers:"
        print "               [1]: " + self.wrong_1.encode('utf-8') + " ( " + str(self.wrong_1_p) + " )"
        print "               [2]: " + self.wrong_2.encode('utf-8') + " ( " + str(self.wrong_2_p) + " )"
        print "               [3]: " + self.wrong_3.encode('utf-8') + " ( " + str(self.wrong_3_p) + " )"
        print "               [4]: " + self.correct.encode('utf-8') + " ( " + str(self.correct_p) + " )"
    
