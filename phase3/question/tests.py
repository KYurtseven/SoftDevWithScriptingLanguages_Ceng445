from django.test import TestCase
from question.models import Question,Choices,Topics,Embeds
from datetime import datetime, date
# Create your tests here.

class QuestionTestCase(TestCase):
    def setUp(self):
        topics = []
        topics.append(Topics(t_id=1, body="topic_1"))
        
        choices = []
        choices.append(Choices(c_id=0, body="choice_1", pos ="NONE", iscorrect=False))

        embeds=[]
        embeds.append(Embeds(e_id=0,body="embed_1"))

        Question.objects.create(q_id= "1",
                                body="test_question1_body",
                                parent="0",
                                ask_date= date(2007, 12, 5) ,
                                topics = topics,
                                embeds = embeds,
                                choices = choices
                                )

    def test_Question(self):
        """test_Question"""

        q = Question.objects.get(q_id= "1")
        self.assertEqual(q.body, 'test_question1_body')
        self.assertEqual(q.parent, '0')
        self.assertEqual(q.ask_date, date(2007, 12, 5))
        self.assertEqual(q.topics[0].body, "topic_1" )
        self.assertEqual(q.embeds[0].body, "embed_1" )
        self.assertEqual(q.choices[0].body, "choice_1" )
        self.assertEqual(q.choices[0].c_id, 0 )
        self.assertEqual(q.choices[0].pos, "NONE" )
        self.assertEqual(q.choices[0].iscorrect, False )

    def test_updateParent(self):
        """test_updateParent"""

        q = Question.objects.get(q_id= "1")
        q.updateParent(5)
        self.assertEqual(q.parent, 5)

    def test_updateAskDate(self):
        """test_updateAskDate"""

        q = Question.objects.get(q_id= "1")
        q.updateAskDate("2020.1.1")
        self.assertEqual(q.ask_date,"2020.1.1")

    def test_addEmbed(self):
        """test_addEmbed"""

        q = Question.objects.get(q_id= "1")
        q.addEmbed("embed_2")
        self.assertEqual(q.embeds[1].body, "embed_2")

    def test_addTopic(self):
        """test_addTopic"""

        q = Question.objects.get(q_id= "1")
        q.addTopic("topic_2")
        self.assertEqual(q.topics[1].body, "topic_2")

    def test_addChoice(self):
        """test_addChoice"""

        q = Question.objects.get(q_id= "1")
        q.addChoice("choice_2",str(True),"START")
        self.assertEqual(q.choices[1].body, "choice_2")
        self.assertEqual(q.choices[1].pos, "START")
        self.assertEqual(q.choices[1].iscorrect, True)

    def test_updateBody(self):
        """test_updateBody"""

        q = Question.objects.get(q_id= "1")
        q.updateBody("body_2")
        self.assertEqual(q.body, "body_2")

    def test_updateEmbed(self):
        """test_updateEmbed"""

        q = Question.objects.get(q_id= "1")
        q.updateEmbed(0,"embed_0")
        self.assertEqual(q.embeds[0].body, "embed_0")

    def test_updateTopic(self):
        """test_updateTopic"""

        q = Question.objects.get(q_id= "1")
        q.updateTopic(1,"topic_0")
        self.assertEqual(q.topics[0].body, "topic_0")

    def test_updateChoice(self):
        """test_updateChoice"""

        q = Question.objects.get(q_id = "1")
        q.updateChoice(0, "new_choice", str(True), "END")
        self.assertEqual(q.choices[0].body, "new_choice")
        self.assertEqual(q.choices[0].pos, "END")
        self.assertEqual(q.choices[0].iscorrect, True)

    def test_delEmbed(self):
        """test_delEmbed"""

        q= Question.objects.get(q_id = "1")
        q.delEmbed(0)
        self.assertEqual(q.embeds,[])

    def test_delTopic(self):
        """test_delTopic"""

        q= Question.objects.get(q_id = "1")
        q.delTopic(1)
        self.assertEqual(q.topics,[])

    def test_delChoice(self):
        """test_delChoice"""

        q= Question.objects.get(q_id = "1")
        q.delChoice(0)
        self.assertEqual(q.choices,[])

    def test_copyQuestion(self):
        """test_copyQuestion"""

        q= Question.objects.get(q_id = "1")
        new_q = q.copyQuestion()
        self.assertEqual(new_q.body, 'test_question1_body')
        self.assertEqual(new_q.parent, '1')
        self.assertEqual(new_q.topics[0].body, "topic_1" )
        self.assertEqual(new_q.embeds[0].body, "embed_1" )
        self.assertEqual(new_q.choices[0].body, "choice_1" )
        self.assertEqual(new_q.choices[0].c_id, 0 )
        self.assertEqual(new_q.choices[0].pos, "NONE" )
        self.assertEqual(new_q.choices[0].iscorrect, False )