import string

rating = "0 - Not at all\n1 - Several days\n2 - More than half the days\n3 - Nearly every day"
moods = "0 - Unmotivated\n1 - Lonely\n2 - Sad\n3 - Anxious\n4 - Lost\n5 - Discouraged"

Q1 = "Little interest or pleasure in doing things?\n\n{}".format(rating)
Q2 = "Feeling down, depressed, or hopeless?\n\n{}".format(rating)
Q3 = "Trouble falling or staying asleep, or sleeping too much?\n\n{}".format(rating)
Q4 = "Feeling tired or having little energy?\n\n{}".format(rating)
Q5 = "Poor appetite or overeating?\n\n{}".format(rating)
Q6 = "Feeling bad about yourself — or that you are a failure or have let yourself or your family down?\n\n{}".format(rating)
Q7 = "Trouble concentrating on things, such as reading the newspaper or watching television?\n\n{}".format(rating)
Q8 = "Moving or speaking so slowly that other people could have noticed? Or so fidgety or restless that you have been moving a lot more than usual?\n\n{}".format(rating)
Q9 = "Thoughts that you would be better off dead, or thoughts of hurting yourself in some way?\n\n{}".format(rating)
Q10 = "Which of the following would best describe how you are currently feeling?\n\n{}".format(moods)

questions = [Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10]