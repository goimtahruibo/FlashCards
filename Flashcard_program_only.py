from typing import Set
import random

class Deck_of_questions:
    Decknames = []
    def __init__(self,name):
        Deck_of_questions.Decknames.append(name)
        self.name = name
        self.Questionsfile = name+" QU.txt"
        self.Answerfile = name +" AN.txt"
    def CreateFiles(self):#creates question and answer files if the Cards do not exist
        self.fileQ = open(self.Questionsfile,'w')
        self.fileQ.close()
        self.fileA = open(self.Answerfile,"w")#creates an empty text file
        self.fileA.close()
        self.ReadFiles()#runs Readfiles to create the question and answer list
    def CreateAnswerandQuestionLists(self):#creates list of answer or Questions from files
        newlist = []
        for line in self.oldlist:
            newlist.append(line.strip())
        return(newlist)
    def ReadFiles(self):#Reads the files
        self.fileQ = open(self.Questionsfile,'r')
        self.oldlist = self.fileQ.readlines()#Saves the text Question file to a list(oldlist: 
        #it is called oldlist as it will be used temporarily to add to the newlist in create questions list)
        self.Qlist = self.CreateAnswerandQuestionLists()#creates a question list from the oldlist but without the \n and
        # adds it to the variable self.Qlist
        self.fileQ.close()
        self.fileA = open(self.Answerfile,"r")
        self.oldlist = self.fileA.readlines()#repeats the same for Answers
        self.Alist = self.CreateAnswerandQuestionLists()#repeats the same for Answers
        self.fileA.close()
    def AddQandA(self,Question,Answer):
        self.Qlist.append(Question)
        self.Alist.append(Answer)
    def SaveQandA(self):#saves changes to answer and question list
        self.fileQ = open(self.Questionsfile,'w')
        for question in self.Qlist:
            self.fileQ.write(question+"\n")
        self.fileQ.close()
        self.fileA = open(self.Answerfile,"w")
        for answer in self.Alist:
            self.fileA.write(answer+"\n")
        self.fileA.close()       

class Course:
    Coursenames = []
    def __init__(self,name):
        Course.Coursenames.append(name)
        self.name = name
        self.cards = []#the saved card objects
    def SaveCardlist(self):#Saves the cardlist when new cards are addded
        self.cardnames =[]#self.cardnames is a list of the cardnames as STRINGS
        for each in self.cards:
            self.cardnames.append(each.name)
        self.CardsFile = open(self.name+" Set.txt","w")
        for each in self.cardnames:
            self.CardsFile.write(each+"\n")
        self.CardsFile.close()
    def CreateNewCard(self,cardname):#creates a new Card object and saves it to the textfile
        self.cards.append(Deck_of_questions(cardname))#adds an object to cards list of type cards
        self.cards[-1].CreateFiles()
        self.SaveCardlist()
    def CreateCardlist(self):#if this is a new cardset, this will be called to create a file to contain all of the cards
        #that will be put in the set
        self.CardsFile = open(self.name+" Set.txt","w")
        self.CardsFile.close()
    def InstantiateSavedCards(self):# gets all the card names from the Cardsfile and turns them into the class cards so they can be used
        self.CardsFile = open(self.name+" Set.txt","r")#opens the textfile specific to the course
        self.currentcardlist = self.CardsFile.readlines()#makes the list of the cards
        for name in self.currentcardlist:
            self.cards.append(Deck_of_questions(name.strip()))#creates the object and adds it to the list of cards
        for each in self.cards:
            each.ReadFiles()# Reads the file of the objects so they can automatically get their Q and A list
        self.CardsFile.close()
    def RenameCourse(self,newname):
        self.name = newname
        self.SaveCardlist()

def GetCardSets():#opens the cardset file and gets the saved cards
    Sets = []
    try:#this try and except checks if there is a cardset file available, if not it makes a new one
        CardSets = open("CardSets.txt","r")
    except:
        CardSets = open("CardSets.txt","w")
        CardSets.close()
        CardSets = open("CardSets.txt","r")
    Lines = CardSets.readlines()
    for Set in Lines:
        Sets.append(Set.strip())
    CardSets.close()
    return(Sets)#the second half of this function will get all the names of the CardSets

def SaveCourses(Sets):#Saves the names of all the cardsets created in this session
    File = open("CardSets.txt","w")
    for each in Sets:#sets is a list of each name of the courses
        File.write(each+"\n")
    File.close()

def CreateNewCourse(Sets,SetObjects,CardSetname):# creates a new course and create and empty list for it to contain its Cards
    Sets.append(CardSetname)
    SetObjects.append(Course(CardSetname))#creates a new cardset object with cardsetname as the name
    SetObjects[-1].CreateCardlist()#Creates the cardlist to contain its cards
    SaveCourses(Sets)

def GetDeck(Cardname,CourseAccessed):#Gets the Cards list with the name requested from the user
    index = 0
    for each in CourseAccessed.cards:#Checks if the name from Cardname is the same as a name of a cardgroup within the Course the user already chose
        if each.name.upper() == Cardname.upper():
            CardAccessed = CourseAccessed.cards[index]
            #print("lol")
            return(CardAccessed)
        index += 1
    if index == len(CourseAccessed.cards):# if the user types in teh wrong name this will return false to continue a while loop
        return False

def Access_Decks_in_Courses(AccessSet,Sets,SetObjects):#Returns the Set that the user wants
    index = 0
    for each in Sets:#Gets the CardSet that the user requested by checking each cardset
        if AccessSet.upper() == each.upper():
            SetAccessed = SetObjects[index]
            return(SetAccessed)
        index += 1
    if index == len(Sets):#if there are no cardsets with the name it continues the while loop and returns false
        return False
#I made this into a function because I realised it would work for questions and options

def Check_Num_Validity(number,Length):# Returns True if the number that the user requested is less than one or greater than a number
    if number.isdigit() == True:#Checks if the user input is an integer
        if int(number) > Length:#this is in teh other if statement as if editno.isdigit() = False then you can't turn Editno into a int
            return (False,"High")
        elif int(number)<1:
            return(False,"low")
        else:
            return (True,"Yay")
    else:
        return (False,"notnum")

def Get_Answer_or_Question_num(CardAccessed,Editno):#This was repeated twice when checking for the question number to edit so I thought it would be easier
    #to put it into a function
    Cont = Check_Num_Validity(Editno,len(CardAccessed.Alist))
    while Cont[0] == False:
        if Cont[1] =="High":
            Editno = input("Your number chosen is not valid as it is higher than any question number ")
        elif Cont[1] =="low":
            Editno = input("Your number chosen is not valid as it is less than one ")
        else:
            Editno = input("You did not write a valid number ")
        Cont = Check_Num_Validity(Editno,len(CardAccessed.Alist))
    Editno = int(Editno)-1
    return(Editno)

def Check_Options(Answer,LenOptions):#made because it will be repeated every single time there are options to choose from
    AccessOptions = Check_Num_Validity(Answer,LenOptions)
    while AccessOptions[0] == False:
        if AccessOptions[1] =="High":
            Answer = input("Your number chosen is not valid as it is higher than any of the options ")
        elif AccessOptions[1] =="low":
            Answer = input("Your number chosen is not valid as it is less than any of the options ")
        else:
            Answer = input("You did not write a valid number ")
        AccessOptions = Check_Num_Validity(Answer,LenOptions)
    return Answer
    
def CheckYorN(answer):#Checks if the user typed in Y or N
    x = True
    while x == True:
        if answer.upper() == "Y"  or answer.upper() == "N":
            return(answer)
        else:
            answer = input("You did not type Y or N. Try again. y = yes, n = no")

def TestQuestions(Questions,Answers,num):#Test Questions
    Questions_asked = []
    WrongQuestions = []
    WrongAnswers = []
    Mistakes =[]
    TestQ = 0
    No_right = 0
    Total = 0
    for i in range (num):
        TestQ = random.randint(0,len(Questions)-1)
        Questions_asked.append(TestQ)
        Answer = input("What is the the answer to this question "+Questions[TestQ])
        Total +=1
        if Answer.upper() != Answers[TestQ].upper():
            print("You answered the question incorrectly, The correct answer was "+Answers[TestQ])
            Correction = input("""If you think:
                                  1)you got this right e.g silly spelling error
                                  2)You just got it wrong
                                  Press the corrosponding number
                                  """)
            Correction = Check_Options(Correction,3)
            if Correction == "1":
                No_right += 1
            else:#adds the wrong questions and answers to a list
                WrongQuestions.append(Questions[TestQ])
                WrongAnswers.append(Answers[TestQ])
                Mistakes.append(Answer)
        else:
            print("You were correct")
            No_right += 1 
        Questions.pop(TestQ)#removes that question from the questions list so that it won't come up again in this set
        Answers.pop(TestQ)
            
    print("You got"+str(No_right)+" out of "+str(Total))
    empty = False
    if Questions == []:
        empty = True
    if WrongAnswers != []:
        Seemistake = input("Would you like to see the questions you got wrong? Y/N?")
        Seemistake = CheckYorN(Seemistake)
        if Seemistake.upper() == "Y":
            for i in range(len(WrongQuestions)):
                print("You got "+str(WrongQuestions[i])+" Wrong. You put " +str(Mistakes[i])+" the answer was "+str(WrongAnswers[i]))
    return Questions,Answers,empty

def Checkname(DeckorCourse):#Made to check that the user does not make a repeated course or Deck
    name = input("What would you like to name this "+DeckorCourse+"?")
    Cont = False
    while Cont == False:
        index = 0
        if DeckorCourse == "Deck":
            for each in Deck_of_questions.Decknames:
                if each.upper() == name.upper():
                    index+=1
        else:       
            for each in Course.Coursenames:
                if each.upper() == name.upper():
                    index+=1
        if index >0:
            name = input("There is already a "+DeckorCourse+" named that. Input a new name")
        else:
            return(name)
def CheckifCoureseempty(CourseAccessed):#Checks if a course is empty when doing the question test
    EmptyDecks = 0
    TotalDecks = 0
    for each in CourseAccessed.cards:
        TotalDecks += 1
        if each.Qlist == []:
            EmptyDecks +=1
    if  TotalDecks == EmptyDecks:
        return True
    else:
        return False
              
def main():
    run = True
    index = 0
    Sets = GetCardSets()
    SetObjects = []
    for each in Sets:
        SetObjects.append(Course(each.strip()))
        SetObjects[index].InstantiateSavedCards()
        index+=1
    while run == True:
        if Sets == []:
            Answer = input("Welcome to Omars Flashcard thing. You currently have no Courses saved , press one to add one, 2 to quit")
            if Answer == "1":
                Coursename = Checkname("Course")
                CreateNewCourse(Sets,SetObjects,Coursename)
                Repetitions = input("How many Cards would you lke to add to this Course(must be greater than 0)?")
                Cont = False
                while Cont == False:
                    if Repetitions.isdigit() == False:
                        Repetitions = input("You have not written a number")
                    else:
                        if int(Repetitions)<1:
                            Repetitions = input("You must write a number greater than 0")
                        else:
                            Cont = True
                for i in range(int(Repetitions)):
                    cardname = Checkname("Deck")
                    SetObjects[-1].CreateNewCard(cardname)
                
            else:
                run == False
        else:
            print("""Hello, Welcome to Omars Flashcard file saver.
                    Your current saved Sets is/are called:""")
            for each in Sets:
                print("             "+each)
            option = input("""Would you like to:
                    1)Create a new Course or rename a Course
                    2)Access one of you current Courses and edit the cards within or add new cards
                    3)Open a deck to test yourself on Questions
                    4)Test yourself on multiple decks
                    5)Import a file of questions and answers to a new deck #Work in progress do not press
                    6)Delete Files
                    7)Quit
                    press the corrosponding number.
                    """)

            option = Check_Options(option,7)
            if option == "1":
                backtostart = False
                while backtostart == False:
                    Answer = input("""Would you like to:
                                      1)Add a course
                                      2)Rename a Course
                                      3)Quit
                                      """)
                    if Answer == "1":
                        CardSetname = Checkname("Course")
                        CreateNewCourse(Sets,SetObjects,CardSetname)
                        Repetitions = input("How many Cards would you lke to add to this cardset(must be greater than 0)?")
                        Cont = False
                        while Cont == False:
                            if Repetitions.isdigit() == False:
                                Repetitions = input("You have not written a number")
                            else:
                                if int(Repetitions)<1:
                                    Repetitions = input("You must write a number greater than 0")
                                else:
                                    Cont = True
                        for i in range(int(Repetitions)):
                            cardname = Checkname("Deck")
                            SetObjects[-1].CreateNewCard(cardname)
                    elif Answer == "2":
                        pass
                    else:
                        backtostart = True

            if option == '2':
                backtostart = False
                while backtostart == False:
                    print("the courses available are:")
                    for each in Sets:
                        print(each)
                    AccessCourse = input("Which Course would you like to Access?")
                    CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,SetObjects)
                    while CourseAccessed == False:
                        AccessCourse = input("You typed in the name wrong")
                        CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,SetObjects)
                    Samecourse = True
                    while Samecourse == True:
                            
                        print("The Cards within "+CourseAccessed.name+" set are")
                        for each in CourseAccessed.cards:#shows the cardgroups within the Cardgroup
                            print(each.name)
                        Answer = input("""Would you like to:
                                        1) Add cards
                                        2) Edit a cards questions and answers
                                        3) Access a different course
                                        4) Quit to main menu
                                        """)
                        Answer = Check_Options(Answer,4)
                        if Answer == '1':
                            Repetitions = input("How many cards would you like to add?")
                            for i in range(int(Repetitions)):
                                cardname = Checkname("Deck")
                                CourseAccessed.CreateNewCard(cardname)
                        elif Answer == '2':
                            backtooptionmenu = False
                            while backtooptionmenu == False:
                                Cardname = input("Which Card do you want to access?")
                                CardAccessed = False
                                CardAccessed = GetDeck(Cardname,CourseAccessed)
                                while CardAccessed == False:
                                    Cardname = input(("You did not spell the name correctly"))
                                    CardAccessed = GetDeck(Cardname,CourseAccessed)
                                if CardAccessed.Alist == []:
                                    Repetitions = input("There are no questions in this Deck, how many do you want to add?(must be >0")
                                    Cont = False
                                    while Cont == False:
                                        if Repetitions.isdigit() == False:
                                            Repetitions = input("You have not written a number")
                                        else:
                                            if int(Repetitions)<1:
                                                Repetitions = input("You must write a number greater than 0")
                                            else:
                                                Cont = True   
                                    for i in range(int(Repetitions)):
                                        Question = input("What is the question")
                                        Answr = input("What is the Answer") 
                                        CardAccessed.AddQandA(Question,Answr)     
                                    CardAccessed.SaveQandA()   
                                Samecard = True
                                while Samecard == True:
                                    print("The questions and answers within " +CardAccessed.name +" are:")
                                    index = 0
                                    for each in CardAccessed.Qlist:
                                        print( str(index+1)+")"+each+"   "+CardAccessed.Alist[index])
                                        index += 1
                                    Options = input("""Would you like to:
                                                    1)Edit a question
                                                    2)Edit an answer
                                                    3)Add a question and answer
                                                    4)Goback to course menu to edit a different card or course
                                                    """)
                                    Options = Check_Options(Options,4)
                                    if Options == "1":
                                        Editno = input("which question number would you like to edit?")
                                        Editno = Get_Answer_or_Question_num(CardAccessed,Editno)
                                        Edit = input("What would you like to change "+CardAccessed.Qlist[Editno]+" to?")
                                        CardAccessed.Qlist[Editno] = Edit   
                                        CardAccessed.SaveQandA()
                                    if Options == "2":
                                        Editno = input("which answer number would you like to edit?")
                                        Editno = Get_Answer_or_Question_num(CardAccessed,Editno)
                                        Edit = input("What would you like to change "+CardAccessed.Alist[Editno]+" to?")
                                        CardAccessed.Alist[Editno] = Edit
                                        CardAccessed.SaveQandA()  
                                    if Options == "3":
                                        repetitions= int(input("How many questions and answers would you like to add?"))
                                        for i in range(repetitions):
                                            Question = input("What is the question")
                                            Answer = input("What is the Answer")
                                            CardAccessed.AddQandA(Question,Answer)
                                        CardAccessed.SaveQandA()
                                    if Options == "4":
                                        Samecard = False
                                        backtooptionmenu = True
                        elif Answer == '3':
                            Samecourse = False
                        else:
                            Samecourse = False
                            backtostart = True
                            backtooptionmenu = True

            if option == "3":
                empty = False
                print("""The Courses saved are""")
                for each in Sets:
                    print("             "+each) 
                backtostart = False
                while backtostart == False:
                    AccessCourse = input("Which Course would you like to Access?")
                    CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,SetObjects)
                    while CourseAccessed == False:
                        AccessCourse = input("You typed in the name wrong lol")
                        CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,SetObjects)
                    Repeat_Course = True
                    Empty = CheckifCoureseempty(CourseAccessed)
                    if Empty == True:
                        Repeat_Course = False
                        Goback = input("""That Course is empty. Would you like to
                                          1)Choose a different course
                                          2)Quit
                                          """)    
                    Check_Options(Goback,2)
                    if Goback == "2":
                        backtostart = True    
                    while Repeat_Course == True:
                        print("The Cards within "+CourseAccessed.name+" set are")
                        for each in CourseAccessed.cards:
                            if each.Qlist != []:
                                print(each.name)
                        Cardname = input("Which Card do you want to access?")
                        CardAccessed = False
                        CardAccessed = GetDeck(Cardname,CourseAccessed)
                        while CardAccessed == False:
                            Cardname = input(("You did not spell the name correctly"))
                            CardAccessed = GetDeck(Cardname,CourseAccessed)
                        Repeat_Card = True
                        Questions = []
                        Answers = []
                        for each in CardAccessed.Qlist:
                            Questions.append(each)
                        for each in CardAccessed.Alist:
                            Answers.append(each)
                        Maxno = len(Questions)
                        while Repeat_Card == True:
                            Answer = input("There are "+str(Maxno)+" Questions. How many would you like to be tested on ?")
                            Cont = Check_Num_Validity(Answer,Maxno)
                            while Cont[0] == False:
                                if Cont[1] != "notnum":
                                    Answer = input("There are "+str(Maxno)+" Questions.Your number was "+Cont[1]+"er than any number between 1-"+str(Maxno))
                                elif Cont[1] == "notnum":
                                    Answer = input("There are "+str(Maxno)+" Questions.Your number was not a valid number between 1-"+str(Maxno))
                                Cont = Check_Num_Validity(Answer,Maxno)
                            QandAinfo =TestQuestions(Questions,Answers,int(Answer))
                            empty = QandAinfo[2]
                            Repeat = input("""Would you like to test yourself again on
                                            1) This Card
                                            2) This card but without the questions you did this round
                                            3) Another Card within this course
                                            4) Another Course
                                            5) Quit
                                            """)
                            Repeat = Check_Options(Repeat,5)
                            while empty == True and Repeat == "2":
                                Repeat = input("You can not choose option two as you have answered all the questions choose another option")
                                Repeat = Check_Options(Repeat,4)
                            print(Repeat)
                            if Repeat == "1":
                                Questions = []
                                Answers = []
                                for each in CardAccessed.Qlist:
                                    Questions.append(each)
                                for each in CardAccessed.Alist:
                                    Answers.append(each)
                                Maxno = len(Questions)
                                
                                Repeat_Card == True
                            elif Repeat == "2":
                                Repeat_Card = True
                                Questions = QandAinfo[0]
                                Answers = QandAinfo[1]
                                Maxno = len(Questions)
                    
                            elif Repeat == "3":
                                Repeat_Card = False
                                Repeat_Course = True
                            elif Repeat == "4":
                                Repeat_Card = False
                                Repeat_Course = False
                                backtostart = False
                            elif Repeat == "5":
                                Repeat_Card = False
                                Repeat_Course = False
                                backtostart = True
            elif option =="4":
                backtostart = False
                while backtostart == False:
                    print("""The Courses saved are""")
                    for each in Sets:
                        print("             "+each) 
                    AccessCourse = input("Which set would you like to Access?")
                    CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,SetObjects)
                    while CourseAccessed == False:
                        AccessCourse = input("You typed in the name wrong lol")
                        CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,SetObjects)
                    Accessedall = False
                    DecksAvailable = CourseAccessed.cards
                    TestCards = []
                    while Accessedall == False:
                        print("Your Decks available to choose from are")
                        for each in DecksAvailable:
                            print(each.name)
                        Cardname = input("Which Card do you want to add to the list of questions?")
                        CardAccessed = GetDeck(Cardname,CourseAccessed)
                        while CardAccessed == False:
                            Cardname = input(("You did not spell the name correctly"))
                            CardAccessed = GetDeck(Cardname,CourseAccessed)
                        TestCards.append(CardAccessed)
                        index = 0
                        for each in DecksAvailable:
                            if each.name == CardAccessed.name:
                                DecksAvailable.pop(index)
                            index += 1
                        if DecksAvailable == []:
                            print("You have accessed all the Decks in this course, we will now move on")
                            Accessedall = True
                        else:
                            print("You have accessed these cards")
                            for each in TestCards:
                                print(each.name)
                            YorN = input("Would you like to add another card Y/N")
                            YorN = CheckYorN(YorN)
                            if YorN.upper() == "N":
                                Accessedall = True
                    LongQuestions = []
                    LongAnswers = []
                    for each in TestCards:
                        for Q in each.Qlist:
                            LongQuestions.append(Q)
                        for A in each.Alist:
                            LongAnswers.append(A)
                    #I will probably turn the next part into a function because it essentially will test questions just like option 3
                    Questions = []
                    Answers = []
                    for each in LongQuestions:
                        Questions.append(each)
                    for each in LongAnswers:
                        Answers.append(each)
                    Repeat_Card = True
                    while Repeat_Card == True:
                        Maxno = len(Questions)
                        Answer = input("There are "+str(Maxno)+" Questions. How many would you like to be tested on?")
                        Cont = Check_Num_Validity(Answer,Maxno)
                        while Cont[0] == False:
                            if Cont[1] != "notnum":
                                Answer = input("There are "+str(Maxno)+" Questions.Your number was "+Cont[1]+"er than any number between 1-"+str(Maxno))
                            elif Cont[1] == "notnum":
                                Answer = input("There are "+str(Maxno)+" Questions.Your number was not a valid number between 1-"+str(Maxno))
                            Cont = Check_Num_Validity(Answer,Maxno)
                        QandAinfo =TestQuestions(Questions,Answers,int(Answer))
                        empty = QandAinfo[2]
                        Repeat = input("""Would you like to test yourself again on
                                        1) These questions
                                        2) These questions but without the questions you did this round
                                        3) Another set of decks in other course
                                        4)Quit
                                        """)
                        Repeat = Check_Options(Repeat,4)
                        while empty == True and Repeat == "2":
                            Repeat = input("You can not choose option two as you have answered all the questions choose another option")
                            Repeat = Check_Options(Repeat,4)
                        
                        if Repeat == "1":
                            Questions = []
                            Answers = []
                            for each in LongQuestions:
                                Questions.append(each)
                            for each in LongAnswers:
                                Answers.append(each)
                            Maxno = len(Questions)
                            Repeat_Card == True
                        elif Repeat == "2":
                            Repeat_Card = True
                            Questions = QandAinfo[0]
                            Answers = QandAinfo[1]
                            Maxno = len(Questions)
                        elif Repeat == "3":
                            Repeat_Card = False
                        elif Repeat == "4":
                            Repeat_Card = False
                            backtostart = True
                            
            elif option == "5":
                pass
            elif option == "6":#Delete stuff
                ToDelete = input("""What would you like to delete?
                                    1)Course
                                    2)Card
                                    3)Quit
                                    """)  
                ToDelete =Check_Options(ToDelete,3)  
                     
            else:
                run = False

main()
