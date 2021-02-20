import question

class Quiz:
    def __init__(self):
        self.questions = []

    def add_question(self):
        self.questions.append(question.Question(len(self.questions)+1))
        return self.questions[-1]

    def num_questions(self):
        return len(self.questions)

    def clear_questions(self):
        self.questions = []

    def find_question(self, n=0):
        return self.questions[n-1]

    def submit_answer(self, member, ans, n=0):
        question = self.questions[n-1]
        
        if question.is_open:

            if member in question.who_answered: return 1

            question.who_answered.append(member)
            return 0

        else: return 2

