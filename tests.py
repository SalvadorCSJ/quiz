import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_valid_title():
    question1 = Question(title='Question 1')
    question2 = Question(title='Question 2')
    question3 = Question(title='S'*200)
    question4 = Question(title='S')
    
    assert question1.title == 'Question 1'
    assert question2.title == 'Question 2'
    assert question3.title == 'S'*200
    assert question4.title == 'S'

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='Q1', points=0)
    with pytest.raises(Exception):
        Question(title='Q2', points=101)
    with pytest.raises(Exception):
        Question(title='Q3', points=-10)
    with pytest.raises(Exception):
        Question(title='Q4', points=110)

def test_get_correct_choice():
    question = Question(title='Q1')  
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.add_choice('c', False)
    question.add_choice('d', True)
    question.add_choice('e', False)

    correct_choice = question._correct_choice_ids()[0]
    assert correct_choice == 4

def test_check_invalid_choice_ids():
    question1 = Question(title='Q1')  
    question1.add_choice('a', True)
    with pytest.raises(Exception):
        question1._check_valid_choice_id(2)

def test_generate_choice_id():
    question1 = Question(title='Q1')
    id1 = question1._generate_choice_id()
    assert id1 == 1

    question1.add_choice('a',True)
    id2 = question1._generate_choice_id()
    assert id2 == 2
    
def test_remove_one_choice():
    question = Question(title='q1')  
    question.add_choice('a', False)
    choice = question.choices[0]

    assert choice.id == 1

    question.remove_choice_by_id(choice.id)

    with pytest.raises(Exception):
        question.choices[0]

def test_remove_all_choices():
    question = Question(title='Q1')  
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', False)

    question.remove_all_choices()

    with pytest.raises(Exception):
        question.choices[0]
    with pytest.raises(Exception):
        question.choices[1]
    with pytest.raises(Exception):
        question.choices[2]

def test_set_correct_choices():
    question = Question(title='Q1')  
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    question.set_correct_choices([3])

    assert question.choices[0].is_correct == False
    assert question.choices[1].is_correct == False
    assert question.choices[2].is_correct == True

def test_choice_by_id():
    question = Question(title='Q1')  
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    assert question._choice_by_id(1).text == 'a'
    assert question._choice_by_id(2).text == 'b'
    assert question._choice_by_id(3).text == 'c'

def test_select_choices():
    question = Question(title='Q1')  
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.add_choice('c', False)
    question.add_choice('d', True)
    question.add_choice('e', False)

    correct_choice = question.select_choices([4])[0]
    assert correct_choice == 4

@pytest.fixture
def data():
    question = Question(title='Q1')  
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.add_choice('c', False)
    question.add_choice('d', True)
    question.add_choice('e', False)
    
    return question

def test_find_correct_choice(data):
    correct_choice = data._correct_choice_ids()[0]
    assert correct_choice == 4

def test_change_correct_choice(data):
    data.choices[3].is_correct = False
    data.set_correct_choices([1])
    correct_choice = data._correct_choice_ids()[0]
    assert correct_choice == 1
