from typing import Set#IDK what this does, i don't want to break the programm so it's here
import random
class Deck_of_questions:
    Decknames = []
    def __init__(self,name):
        Deck_of_questions.Decknames.append(name)
        self.name = name
        self.Questionsfile = name+" QU.txt"
        self.Answerfile = name +" AN.txt"
    def CreateFiles(self):#creates question and answer files if the Decks do not exist
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
    def Import_QandAtextfile(self,QuestionFile,AnswerFile):#Test if this works when ellis comes and sends the file
        self.ImportedQ = open(QuestionFile+".txt")
        self.Importedlist = self.ImportedQ.readlines()
        for each in self.Importedlist:
            self.Qlist.append(each.strip())
        self.ImportedQ.close()
        self.ImportedA = open(AnswerFile+".txt")
        self.Importedlist = self.ImportedA.readlines()
        for each in self.Importedlist:
            self.Alist.append(each.strip())
        self.ImportedA.close()
        self.SaveQandA()
    def Import_csvQandA(self,Filename):
        File = open(Filename+".csv","r")
        Lines = File.readlines()
        for each in Lines:
            each = each.strip()
            comma = each.find(",")
            Question = each[:comma]
            Answer = each[comma+1:]
            self.Qlist.append(Question)
            self.Alist.append(Answer)
        self.SaveQandA()
    def DeleteQandA(self,Index):
        self.Qlist.pop(Index)
        self.Alist.pop(Index)
        self.SaveQandA()
        
class Course:
    Coursenames = []
    def __init__(self,name):
        Course.Coursenames.append(name)
        self.name = name
        self.Decks = []#the saved Deck objects
    def SaveDecklist(self):#Saves the Course when new Decks are addded
        self.Decknames =[]#self.DEcknames is a list of the Decknames as STRINGS
        for each in self.Decks:
            self.Decknames.append(each.name)
        self.DecksFile = open(self.name+" Set.txt","w")
        for each in self.Decknames:
            self.DecksFile.write(each+"\n")
        self.DecksFile.close()
    def CreateNewDeck(self,Deckname):#creates a new Deck object and saves it to the textfile
        self.Decks.append(Deck_of_questions(Deckname))#adds an object to Decks list of type Deckofquestions
        self.Decks[-1].CreateFiles()
        self.SaveDecklist()
    def CreateDeckList(self):#if this is a new Course, this will be called to create a file to contain all of the Decks
        #that will be put in the set
        self.DecksFile = open(self.name+" Set.txt","w")
        self.DecksFile.close()
    def InstantiateSavedSets(self):# gets all the Deck names from the decksFile and turns them into the class Decks so they can be used
        self.DecksFile = open(self.name+" Set.txt","r")#opens the textfile specific to the course
        self.currentDecklist = self.DecksFile.readlines()#makes the list of the Decks
        for name in self.currentDecklist:
            self.Decks.append(Deck_of_questions(name.strip()))#creates the object and adds it to the list of decks
        for each in self.Decks:
            each.ReadFiles()# Reads the file of the objects so they can automatically get their Q and A list
        self.DecksFile.close()
    def RenameCourse(self,newname):
        self.name = newname
        self.SaveDecklist()

def GetCourse():#opens the Course file and gets the saved Decks
    Sets = []
    try:#this try and except checks if there is a course file available, if not it makes a new one
        courses = open("CourseList.txt","r")
    except:
        courses = open("CourseList.txt","w")
        courses.close()
        courses = open("CourseList.txt","r")
    Lines = courses.readlines()
    for Set in Lines:
        Sets.append(Set.strip())
    courses.close()
    return(Sets)#the second half of this function will get all the names of the Courses

def SaveCourses(Sets):#Saves the names of all the Courses created in this session
    File = open("CourseList.txt","w")
    for each in Sets:#sets is a list of each name of the courses
        File.write(each+"\n")
    File.close()

def CreateNewCourse(Sets,CourseObjects,Coursename):# creates a new course and create and empty list for it to contain its Decks
    Sets.append(Coursename)
    CourseObjects.append(Course(Coursename))#creates a new Courses object with Coursename as the name
    CourseObjects[-1].CreateDeckList()#Creates the Decklist to contain its Decks
    SaveCourses(Sets)

def GetDeck(Deckname,CourseAccessed):#Gets the Decks list with the name requested from the user
    index = 0
    for each in CourseAccessed.Decks:#Checks if the name from Deckname is the same as a name of a Deck within the Course the user already chose
        print(each,Deckname)
        if each.name.upper() == Deckname.upper():
            DeckAccessed = CourseAccessed.Decks[index]
            return(DeckAccessed)
        index += 1
    if index == len(CourseAccessed.Decks):# if the user types in the wrong name this will return false to continue a while loop
        return False

def Access_Decks_in_Courses(AccessSet,Sets,CourseObjects):#Returns the Set that the user wants
    index = 0
    for each in Sets:#Gets the Course that the user requested by checking each Course
        if AccessSet.upper() == each.upper():
            SetAccessed = CourseObjects[index]
            return(SetAccessed)
        index += 1
    if index == len(Sets):#if there are no Course with the name it continues the while loop and returns false
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

def Get_Answer_or_Question_num(DeckAccessed,Editno):#This was repeated twice when checking for the question number to edit so I thought it would be easier
    #to put it into a function
    Cont = Check_Num_Validity(Editno,len(DeckAccessed.Alist))
    while Cont[0] == False:
        if Cont[1] =="High":
            Editno = input("Your number chosen is not valid as it is higher than any question number ")
        elif Cont[1] =="low":
            Editno = input("Your number chosen is not valid as it is less than one ")
        else:
            Editno = input("You did not write a valid number ")
        Cont = Check_Num_Validity(Editno,len(DeckAccessed.Alist))
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
    for each in CourseAccessed.Decks:
        TotalDecks += 1
        if each.Qlist == []:
            EmptyDecks +=1
    if  TotalDecks == EmptyDecks:
        return True
    else:
        return False
def Check_Repetition_number(number):#Used for when I ask for multuple decks to be made
    cont = False
    greaterthan0 = True
    while cont == False:
        if number.isdigit() == True:
            if int(number) > 0:
                cont = True
                return number   
            else:
                greaterthan0 = False
        if greaterthan0 == False or number.isdigit() == False:
            number = input("Sorry you have written the number incorrectly, it has to be a whole number > 0")
def main():
    run = True
    index = 0
    Sets = GetCourse()
    CourseObjects = []
    for each in Sets:
        CourseObjects.append(Course(each.strip()))
        CourseObjects[index].InstantiateSavedSets()
        index+=1
    while run == True:
        if Sets == []:
            Answer = input("Welcome to Omars Flashcard thing. You currently have no Courses saved , press one to add one, 2 to quit")
            if Answer == "1":
                Coursename = Checkname("Course")
                CreateNewCourse(Sets,CourseObjects,Coursename)
                Repetitions = input("How many Decks would you lke to add to this Course(must be greater than 0)?")
                Cont = False
                Repetitions = Check_Repetition_number(Repetitions)
                for i in range(int(Repetitions)):
                    Deckname = Checkname("Deck")
                    CourseObjects[-1].CreateNewDeck(Deckname)
                
            else:
                run == False
        else:
            print("""Hello, Welcome to Omars Flashcard file saver.
                    Your current saved Sets is/are called:""")
            for each in Sets:
                print("             "+each)
            option = input("""Would you like to:
                    1)Create a new Course or rename a Course
                    2)Access one of you current Courses and edit the Decks within or add new Decks
                    3)Open a deck to test yourself on Questions
                    4)Test yourself on multiple decks
                    5)Import a file of questions and answers to a new deck #Work in progress do not press
                    6)Delete Files#Does not work rn
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
                        Coursename = Checkname("Course")# you can probablt put this in teh function below
                        CreateNewCourse(Sets,CourseObjects,Coursename)
                        Repetitions = input("How many Decks would you lke to add to this Course(must be greater than 0)?")
                        Cont = False
                        Repetitions = Check_Repetition_number(Repetitions)
                        for i in range(int(Repetitions)):
                            Deckname = Checkname("Deck")
                            CourseObjects[-1].CreateNewDeck(Deckname)
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
                    CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,CourseObjects)
                    while CourseAccessed == False:
                        AccessCourse = input("You typed in the name wrong")
                        CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,CourseObjects)
                    Samecourse = True
                    while Samecourse == True:
                            
                        print("The Decks within "+CourseAccessed.name+" set are")
                        for each in CourseAccessed.Decks:#shows the Deck within the Course
                            print(each.name)
                        Answer = input("""Would you like to:
                                        1) Add Decks
                                        2) Edit a Decks questions and answers
                                        3) Access a different course
                                        4) Quit to main menu
                                        """)
                        Answer = Check_Options(Answer,4)
                        if Answer == '1':
                            Repetitions = input("How many Decks would you like to add?")
                            Repetitions = Check_Repetition_number(Repetitions)
                            for i in range(int(Repetitions)):
                                Deckname = Checkname("Deck")
                                CourseAccessed.CreateNewDeck(Deckname)
                        elif Answer == '2':
                            backtooptionmenu = False
                            while backtooptionmenu == False:
                                Deckname = input("Which Deck do you want to access?")
                                DeckAccessed = GetDeck(Deckname,CourseAccessed)
                                while DeckAccessed == False:
                                    Deckname = input(("You did not spell the name correctly"))
                                    DeckAccessed = GetDeck(Deckname,CourseAccessed)
                                if DeckAccessed.Alist == []:
                                    Repetitions = input("There are no questions in this Deck, how many do you want to add?(must be >0")
                                    Repetitions = Check_Repetition_number(Repetitions) 
                                    for i in range(int(Repetitions)):
                                        Question = input("What is the question")
                                        Answr = input("What is the Answer") 
                                        DeckAccessed.AddQandA(Question,Answr)     
                                    DeckAccessed.SaveQandA()   
                                SameDeck = True
                                while SameDeck == True:
                                    print("The questions and answers within " +DeckAccessed.name +" are:")
                                    index = 0
                                    for each in DeckAccessed.Qlist:
                                        print( str(index+1)+")"+each+"   "+DeckAccessed.Alist[index])
                                        index += 1
                                    Options = input("""Would you like to:
                                                    1)Edit a question
                                                    2)Edit an answer
                                                    3)Add a question and answer
                                                    4)Delete a Question and Answer
                                                    5)Import a file
                                                    6)Goback to course menu to edit a different Deck or course
                                                    """)
                                    Options = Check_Options(Options,6)
                                    if Options == "1":
                                        Editno = input("which question number would you like to edit?")
                                        Editno = Get_Answer_or_Question_num(DeckAccessed,Editno)
                                        Edit = input("What would you like to change "+DeckAccessed.Qlist[Editno]+" to?")
                                        DeckAccessed.Qlist[Editno] = Edit   
                                        DeckAccessed.SaveQandA()
                                    elif Options == "2":
                                        Editno = input("which answer number would you like to edit?")
                                        Editno = Get_Answer_or_Question_num(DeckAccessed,Editno)
                                        Edit = input("What would you like to change "+DeckAccessed.Alist[Editno]+" to?")
                                        DeckAccessed.Alist[Editno] = Edit
                                        DeckAccessed.SaveQandA()  
                                    elif Options == "3":
                                        repetitions= int(input("How many questions and answers would you like to add?"))
                                        for i in range(repetitions):
                                            Question = input("What is the question")
                                            Answer = input("What is the Answer")
                                            DeckAccessed.AddQandA(Question,Answer)
                                        DeckAccessed.SaveQandA()
                                    elif Options == "4":
                                        IndextoDelete = input("Which Question number do you want to delete?")
                                        IndextoDelete = Get_Answer_or_Question_num(DeckAccessed,IndextoDelete)
                                        DeckAccessed.DeleteQandA(int(IndextoDelete))
                                    elif Options == "5":
                                        print("This is in the works")
                                        pass
                                    elif Options == "6":
                                        SameDeck = False
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
                    CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,CourseObjects)
                    while CourseAccessed == False:
                        AccessCourse = input("You typed in the name wrong lol")
                        CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,CourseObjects)
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
                        print("The Decks within "+CourseAccessed.name+" set are")
                        for each in CourseAccessed.Decks:
                            if each.Qlist != []:
                                print(each.name)
                        Deckname = input("Which Deck do you want to access?")
                        DeckAccessed = False
                        DeckAccessed = GetDeck(Deckname,CourseAccessed)
                        while DeckAccessed == False:
                            Deckname = input(("You did not spell the name correctly"))
                            DeckAccessed = GetDeck(Deckname,CourseAccessed)
                            print(DeckAccessed)
                        Repeat_Deck = True
                        Questions = []
                        Answers = []
                        for each in DeckAccessed.Qlist:
                            Questions.append(each)
                        for each in DeckAccessed.Alist:
                            Answers.append(each)
                        Maxno = len(Questions)
                        while Repeat_Deck == True:
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
                                            1) This Deck
                                            2) This Deck but without the questions you did this round
                                            3) Another Deck within this course
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
                                for each in DeckAccessed.Qlist:
                                    Questions.append(each)
                                for each in DeckAccessed.Alist:
                                    Answers.append(each)
                                Maxno = len(Questions)
                                
                                Repeat_Deck == True
                            elif Repeat == "2":
                                Repeat_Deck = True
                                Questions = QandAinfo[0]
                                Answers = QandAinfo[1]
                                Maxno = len(Questions)
                    
                            elif Repeat == "3":
                                Repeat_Deck = False
                                Repeat_Course = True
                            elif Repeat == "4":
                                Repeat_Deck = False
                                Repeat_Course = False
                                backtostart = False
                            elif Repeat == "5":
                                Repeat_Deck = False
                                Repeat_Course = False
                                backtostart = True
            elif option =="4":
                backtostart = False
                AccessedCourse = False
                while backtostart == False:
                    while AccessedCourse == False:#This was added because of the Checkempty as I want the program to come back here
                        # if the course is empty. If I did not have the while loop I could not make RepeatDeck False as it would coninue the program to there (Can you tell I wrote this at 11 pm lol)
                        print("""The Courses saved are""")
                        for each in Sets:
                            print("             "+each) 
                        AccessCourse = input("Which Course would you like to Access?")
                        CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,CourseObjects)
                        while CourseAccessed == False:
                            AccessCourse = input("You typed in the name wrong lol")
                            CourseAccessed = Access_Decks_in_Courses(AccessCourse,Sets,CourseObjects)
                        EmptyCourse = CheckifCoureseempty(CourseAccessed)
                        if EmptyCourse == True:
                            Repeat_Deck = False
                            Accessedall = True
                            Goback = input("""That course is empty. Would you like to:
                                            1)Choose a different course
                                            2)Quit
                                            """)
                            Goback = Check_Options(Goback,2)# you can probably add this and above to the emptycourse function
                            if Goback == "2":
                                AccessedCourse = True
                                backtostart = True
                        else:
                            AccessedCourse = True
                            Accessedall = False
                            Repeat_Deck = True
                        DecksAvailable = CourseAccessed.Decks
                        TestDecks = []
                    
                    while Accessedall == False:
                        print("Your Decks available to choose from are")
                        for each in DecksAvailable:
                            print(each.name)
                        Deckname = input("Which Deck do you want to add to the list of questions?")
                        DeckAccessed = GetDeck(Deckname,CourseAccessed)
                        while DeckAccessed == False:
                            Deckname = input(("You did not spell the name correctly"))
                            DeckAccessed = GetDeck(Deckname,CourseAccessed)
                        TestDecks.append(DeckAccessed)
                        index = 0
                        for each in DecksAvailable:
                            if each.name == DeckAccessed.name:
                                DecksAvailable.pop(index)
                            index += 1
                        if DecksAvailable == []:
                            print("You have accessed all the Decks in this course, we will now move on")
                            Accessedall = True
                        else:
                            print("You have accessed these Decks")
                            for each in TestDecks:
                                print(each.name)
                            YorN = input("Would you like to add another Deck Y/N")
                            YorN = CheckYorN(YorN)
                            if YorN.upper() == "N":
                                Accessedall = True
                    LongQuestions = []
                    LongAnswers = []
                    for each in TestDecks:
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
                    while Repeat_Deck == True:
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
                            Repeat_Deck == True
                        elif Repeat == "2":
                            Repeat_Deck = True
                            Questions = QandAinfo[0]
                            Answers = QandAinfo[1]
                            Maxno = len(Questions)
                        elif Repeat == "3":
                            Repeat_Deck = False
                        elif Repeat == "4":
                            Repeat_Deck = False
                            backtostart = True
                            
            elif option == "5":
                pass
            elif option == "6":#Delete stuff
                ToDelete = input("""What would you like to delete?
                                    1)Course
                                    2)Deck
                                    3)Quit
                                    """)  
                ToDelete =Check_Options(ToDelete,3)         
            else:
                run = False

main()