from django.test import TestCase
from question.models import Question,Choices,Topics,Embeds
from exam.models import Exam, shuffledExams, QuestionId
from datetime import datetime, date

# Create your tests here.
class ExamTestCase(TestCase):
    def setUp(self):
        e_id = "1"
        exam_name = "Test"
        exam_date = date(2007, 12, 5)

        qlist = []
        qlist.append(QuestionId(q_id = 5))
        qlist.append(QuestionId(q_id = 6))


        Exam.objects.create(e_id = e_id, 
                            exam_name = exam_name, 
                            exam_date = exam_date, 
                            question_list = qlist,
                            shuffled_exams = []
                            )

    def test_Exam(self):
        """test_Exam"""

        e = Exam.objects.get(e_id = "1")

        self.assertEqual(e.exam_name, 'Test')
        self.assertEqual(e.exam_date, date(2007, 12, 5))
        self.assertEqual(e.question_list[0].q_id , '5')
        self.assertEqual(e.question_list[1].q_id , '6')

    def test_EditExamName(self):
        """test_editExamName"""

        e = Exam.objects.get(e_id = "1")
        e.editExamName("Newname")
        self.assertEqual(e.exam_name, "Newname")

    def test_UpdateAskDate(self):
        """test_UpdateAskDate"""

        e = Exam.objects.get(e_id = "1")
        e.updateAskDate("2020.1.1")
        self.assertEqual(e.exam_date, "2020.1.1")
