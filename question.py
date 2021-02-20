from random import sample
import homework

class Question:
    
    def __init__(self, question_number):
        self.who_answered = []
        self.number = question_number
        self.is_open = True
        self.correct = str(sample(['A','B','C','D'],1)[0])
        self.keyterms = homework.get_keyterms()
        self.question = homework.question(self.keyterms)
        self.explanation = homework.explanation(self.keyterms)
        
    def question_string(self):
        return f'Question #{self.number}: {self.question}'

    def get_explanation(self):
        self.is_open = False
        expl = f'The answer to question {self.number} is {self.correct}.\n'
        expl += 'Explanation: ' + self.explanation
        return expl