import uuid
import datetime
import pymongo
from question import Question
from QBank import QBank

id_1 = "c5f31e1f-7979-4ff3-8b2c-03c24dbd4ab2"
id_2 = "ad050e54-0849-4766-8875-82c2180ada55"
id_3 = "206b3744-c6aa-4f44-80be-4d168789f2f2"
id_4 = "23308972-5b12-4294-a260-f0a730c6b553"

question_1 = Question(id_1)
question_1.constructor('How many siblings do you have?', 					#body
					[{'body':'None', 'iscorrect': 'false', 'pos': 'START' },		#choices
					{'body':'One', 'iscorrect': 'false', 'pos': 'None' },
					{'body':'Two', 'iscorrect': 'false', 'pos': 'None' },
					{'body':'Three', 'iscorrect': 'false', 'pos': 'None' },
					{'body':'Many', 'iscorrect': 'true', 'pos': 'None' }
					], 
					['personal','sample'], 										#topics
					None, 														#parent
					[])															#embeds

question_2 = Question(id_2)
question_2.constructor('Solve the following equation for $x$:\\\n\\[ 2 x^2 + x + 1 = 0 \\]', 					#body
					[{'body':'1, -1', 'iscorrect': 'false', 'pos': 'None' },										#choices
					{'body':'1, 0', 'iscorrect': 'true', 'pos': 'None' },
					{'body':'$x \\rightarrow \\infty$', 'iscorrect': 'false', 'pos': 'None' },
					{'body':'0, 0', 'iscorrect': 'false', 'pos': 'None' },
					{'body':'None of the above', 'iscorrect': 'false', 'pos': 'END' }
					], 
					['math', 'equation'], 										#topics
					None, 														#parent
					[])															#embeds

question_3 = Question(id_3)
question_3.constructor('Whose logo this is:\\newline \n\\includegraphics[height=3em]{metulogo}', 					#body
					[{'body':'Audi', 'iscorrect': 'true', 'pos': 'None' },		#choices
					{'body':'Batman', 'iscorrect': 'false', 'pos': 'None' },
					{'body':'Bayburt', 'iscorrect': 'false', 'pos': 'None' },
					{'body':'THY', 'iscorrect': 'false', 'pos': 'None' },
					{'body':'None of the above', 'iscorrect': 'false', 'pos': 'END' }
					], 
					['logos','sample'], 										#topics
					None, 														#parent
					['metulogo'])												#embeds

question_4 = Question(id_4)
question_4.constructor('Which of the following is for ``no entrance'' sign?', 					#body
					[{'body':'\\includegraphics[height=2em]{metulogo}', 'iscorrect': 'false', 'pos': 'None' },		#choices
					{'body':'\\includegraphics[height=2em]{cenglogo}', 'iscorrect': 'false', 'pos': 'None' },
					{'body':'\\includegraphics[height=2em]{stopsign}', 'iscorrect': 'false', 'pos': 'None' },
					{'body':'\\includegraphics[height=2em]{noentry}', 'iscorrect': 'false', 'pos': 'None' },
					{'body':'None of the above', 'iscorrect': 'true', 'pos': 'END' }
					], 
					['logos'], 										#topics
					None, 														#parent
					['metulogo','cenglogo','stopsign','noentry'])												#embeds

question_1.save()
question_2.save()
question_3.save()
question_4.save()