# write your code here
from sys import exit

from sqlalchemy import Column, String, Integer, update
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')  #, echo = True for troubleshooting
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'
    question = Column(String)
    answer = Column(String)
    box_number = Column(Integer)
    ID = Column(Integer, primary_key=True, autoincrement=True)

    def add_flashcards(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        bxn = 1
        print('1. Add a new flashcard')
        print('2. Exit')
        user_input = input()
        if user_input == '1':
            print('Question:')
            qst = input().strip()
            while qst == '':
                print('Question:')
                qst = input().strip()
            print('Answer:')
            ans = input().strip()
            while ans == '':
                print('Answer:')
                ans = input().strip()
            query_input = Flashcard(question=qst, answer=ans, box_number=bxn)
            session.add(query_input)
            session.commit()
            self.add_flashcards()
        elif user_input == '2':
            print('Bye!')
            exit()
        else:
            print('{} is not an option'.format(user_input))
            self.add_flashcards()

    def practice_flashcards(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        result_list = session.query(Flashcard).all()
        if result_list == []:
            print('There is no flashcard to practice!')
        else:
            for result in result_list:
                print('Question: ' + result.question)
                print('press "y" to see the answer:')
                print('press "n" to skip:')
                print('press "u" to update:')
                user_input = input()
                if user_input in ['y', 'n']:
                    if user_input == 'y':
                        print('Answer: ' + result.answer)
                    print('press "y" if your answer is correct:')
                    print('press "n" if your answer is wrong:')
                    feedback_ = input()
                    if feedback_ in ['y', 'n']:
                        self.move_flashcards(result.ID, feedback_)
                    else:
                        print('{} is not an option'.format(feedback_))
                elif user_input == 'u':
                    self.update_flashcards(result.ID)


    def move_flashcards(self, id, answer):
        Session = sessionmaker(bind=engine)
        session = Session()
        record = session.query(Flashcard).get(id)
        box_no = record.box_number
        if answer == 'y':
            if box_no in [1, 2]:
                box_no += 1
                stmt = update(Flashcard).where(Flashcard.ID == id).values(box_number = box_no).execution_options(synchronize_session="fetch")
                session.execute(stmt)
            elif box_no == 3:
                session.delete(record)
        elif answer == 'n':
            box_no = 1
            stmt = update(Flashcard).where(Flashcard.ID == id).values(box_number=box_no).execution_options(synchronize_session="fetch")
            session.execute(stmt)
        session.commit()

    def update_flashcards(self, id):
        Session = sessionmaker(bind=engine)
        session = Session()
        record = session.query(Flashcard).get(id)
        print('press "d" to delete the flashcard:')
        print('press "e" to edit the flashcard:')
        user_input = input()
        while user_input not in ['d', 'e']:
            print(user_input+' is not an option')
            print('press "d" to delete the flashcard:')
            print('press "e" to edit the flashcard:')
            user_input = input()
        if user_input == 'd':
            print('you want to delete flashcard')
            session.delete(record)
            print('record deleted')
        elif user_input == 'e':
            print('current question: '+record.question)
            print('please write a new question:')
            qst = input()
            if qst == '':
                qst = record.question
            print('current answer: ' + record.answer)
            print('please write a new answer:')
            ans = input()
            if ans == '':
                ans = record.answer
            stmt = update(Flashcard).where(Flashcard.ID == id).values(question = '{}'.format(qst), answer = '{}'.format(ans)).execution_options(synchronize_session="fetch")
            session.execute(stmt)
        session.commit()


Base.metadata.create_all(engine)


def main():
    f = Flashcard()
    while True:
        print('1. Add flashcards')
        print('2. Practice flashcards')
        print('3. Exit')
        a = input()
        if a in ['1', '2', '3']:
            if a == '1':
                f.add_flashcards()
            elif a == '2':
                f.practice_flashcards()
            else:
                print('Bye!')
                exit()

        else:
            print('{} is not an option'.format(a))


main()
