# coding: utf-8

import Tkinter
from random import sample

class Until10(object):
    question_format = '%d可以分成( %d )和( %s )'

    def __init__(self):
        self.init_form()

    def init_form(self):
        '''Initialize form and its inside controls.'''
        self.form = Tkinter.Tk()
        self.form.title('Until Ten')

        self.question = Tkinter.Text(self.form, width=40, height=1)
        self.history = Tkinter.Listbox(self.form, width=40)
        btn_frame = Tkinter.Frame(self.form)
        btn_list = [
            Tkinter.Button(btn_frame, text=str(i), command=self.receive_answer(i))
            for i in range(10)
        ]

        self.question.pack()
        btn_frame.pack()
        for btn in btn_list:
            btn.pack(side='left')
        self.history.pack(side='top')

    def make_question(self):
        self.total = sample(range(1, 11), 1)[0]
        self.given = sample(range(0, self.total), 1)[0]
        # Paint to form
        self.question.delete(1.0, Tkinter.END)
        self.question.insert(Tkinter.END, self.question_format % (self.total, self.given, ''))

    def receive_answer(self, answer):
        '''Make a handle which handles the user answer.'''
        def answer_handler():
            # Check the answer
            if answer + self.given == self.total:
                his_str = self.question_format % (self.total, self.given, str(answer))
                self.history.insert(0, '⭐️ 答对了！' + his_str)
                self.make_question()
            else:
                self.history.insert(0, '❌ 不对哦！')
        return answer_handler


def start():
    until = Until10()
    until.make_question()
    Tkinter.mainloop()


if __name__ == '__main__':
    start()
