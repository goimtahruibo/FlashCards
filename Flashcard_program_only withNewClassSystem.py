from typing import Set#IDK what this does, i don't want to break the programm so it's here
import random
import pathlib
import os
import sys
import shutil
class Deck_of_questions:
    Decknames = []
    def __init__(self,name,Coursename):
        Deck_of_questions.Decknames.append(name)
        self.name = name
        self.Coursename = Coursename
        self.Questionsfile = os.path.join(Coursename,name+"QU.txt" )#creates path for Questions file
        self.Answerfile =os.path.join(Coursename,name+"AN.txt" )
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
    def AddQandA(self,repetition):
        QNo = repetition +1
        if QNo == 1:
            Question = input("What is your 1st Question?")
            Answer = input("What is your 1st answer")
        elif QNo == 2:
            Question = input("What is your 2nd Question?")
            Answer = input("What is your 2nd answer")  
        elif QNo == 3:
            Question = input("What is your 3rd Question?")
            Answer = input("What is your 3rd answer") 
        elif QNo > 3: 
            Question = input("What is your "+str(QNo)+"th Question?")
            Answer = input("What is your "+str(QNo)+"th answer")        
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
            if "QUESTION" in each.upper() or "ANSWER" in each.upper():
                pass
            else:
                comma = each.find(",")#Finds the index of the comma
                Question = each[:comma]
                Answer = each[comma+1:]
                self.Qlist.append(Question)
                self.Alist.append(Answer)
        self.SaveQandA()
    def DeleteQandA(self,Index):
        self.Qlist.pop(Index)
        self.Alist.pop(Index)
        self.SaveQandA()
    def AddTestQandAlist(self,Answers,Questions):
        for each in self.Qlist:
            Questions.append(each)
        for each in self.Alist:
            Answers.append(each)
        return (Answers,Questions)
    def RenameDeck(self,Newname):
        self.name = Newname   
        NewAnswerFile = os.path.join(self.Coursename,Newname+"AN.txt" ) 
        NewQuestionFile = os.path.join(self.Coursename,Newname+"QU.txt")    
        os.rename(self.Questionsfile,NewQuestionFile)
        os.rename(self.Answerfile,NewAnswerFile)
        self.Questionsfile = NewQuestionFile
        self.Answerfile = NewAnswerFile
class Course:
    AllDecks = []
    def __init__(self,name):
        self.name = name
        self.Foldername = name+"Course"
        self.Decks = []#the saved Deck objects
        try:
            os.makedirs(self.Foldername)#Makes a folder
        except:
            pass
    def CreateNewDeck(self,Deckname):#creates a new Deck object and saves it to the textfile
        self.Decks.append(Deck_of_questions(Deckname,self.Foldername))#adds an object to Decks list of type Deckofquestions
        self.Decks[-1].CreateFiles()
        Course.AllDecks.append(self.Decks[-1])
    def InstantiateSavedSets(self):
        for path in pathlib.Path(self.Foldername).iterdir():
            if "QU" in path.name:
                self.Decks.append(Deck_of_questions(path.name[0:-6],self.Foldername))
                self.Decks[-1].ReadFiles()
                Course.AllDecks.append(self.Decks[-1])
    def GetDeck(self,Deckname):#Gets the Decks list with the name requested from the user
        cont = False
        while cont == False:
            index = 0
            for each in self.Decks:#Checks if the name from Deckname is the same as a name of a Deck within the Course the user already chose
                if each.name.upper() == Deckname.upper():
                    DeckAccessed = self.Decks[index]
                    return(DeckAccessed)
                index += 1
            if index == len(self.Decks):# if the user types in the wrong name this will return false to continue a while loop
                cont = False
                Deckname = input("You spelt the name wrong, please give a new name")
    def RenameCourses(self,Newname):#At this point I decided functions are grreat
        os.rename(self.Foldername,Newname+"Course")#Renames it by making the directory be a new file
        self.name = Newname
        self.Foldername = Newname+"Course"
    def DeleteDeck(self,Deck):
        index = 0
        for each in self.Decks:
            if each == Deck:
                break
            else:
                index +=1
        os.remove(Deck.Questionsfile)#Deletes the file
        os.remove(Deck.Answerfile)
        self.Decks.pop(index)
        index = 0
        for each in Course.AllDecks:
            if each == Deck:
                break
            index += 1
        Course.AllDecks.pop(index)
def GetCourses():#opens the Course file and gets the saved Decks
    CourseObjects = []
    try:#this try and except checks if there is a course file available, if not it makes a new one
        courses = open("CourseList.txt","r")
    except:
        courses = open("CourseList.txt","w")
        courses.close()
        courses = open("CourseList.txt","r")
    Lines = courses.readlines()
    for course in Lines:
        CourseObjects.append(Course(course.strip()))
        CourseObjects[-1].InstantiateSavedSets( )
    courses.close()
    return(CourseObjects)

def CreateNewCourse(Coursename,CourseObjects):
    CourseObjects.append(Course(Coursename))
    SaveCourses(CourseObjects)
    return(CourseObjects)

def SaveCourses(CourseObjects):
    CourseFile = open("CourseList.txt","w")
    for each in CourseObjects:
        CourseFile.write(each.name+"\n")
    CourseFile.close()
    ########################
def Access_Course(AccessSet,CourseObjects):#Returns the Set that the user wants
    cont = False
    while cont == False:
        index = 0
        for each in CourseObjects:#Gets the Course that the user requested by checking each Course
            if AccessSet.upper() == each.name.upper():
                SetAccessed = CourseObjects[index]
                return(SetAccessed)
            index += 1
        if index == len(CourseObjects):#if there are no Course with the name it continues the while loop and returns false
            cont = False
            AccessSet = input("sorry, you typed in the name wrong, try again ")
        
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
        Answer = input("What is the the answer to this question "+Questions[TestQ]+": ")
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
        Seemistake = input("Would you like to see the questions you got wrong? Y/N? ")
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
        if not name:#an empty string is considered False as a boolean
            name = input("Your name can not be nothing")
        else:
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
            number = input("Sorry you have written the number incorrectly, it has to be a whole number > 0 ")
def DisplayCourses(CourseObjects):#this was repeated a lot
    print("Your courses available are.")
    for each in CourseObjects:
        print(each.name)
def CheckFile(Filename,FileType):#I made this to stop errors happening if the file doesn't exist
    cont = False
    while cont == False:
            try:
                FileTest = open(Filename+FileType,"r")
                FileTest.close()
                return(Filename)
            except:
                Filename = input("There are no files in the folder with this name, remember to add it. ")
   
def Ask_one_deck_questions(CourseAccessed,QtoA):
    print("The Decks within "+CourseAccessed.name+" set are")
    for each in CourseAccessed.Decks:
        if each.Qlist != []:
            print(each.name)
    Deckname = input("Which Deck do you want to access? ")
    DeckAccessed = CourseAccessed.GetDeck(Deckname)
    Repeat_Deck = True
    Questions = []
    Answers = []
    QandAData = DeckAccessed.AddTestQandAlist(Answers,Questions)
    if QtoA == "1":
        Questions = QandAData[1]
        Answers = QandAData[0]
    else:
        Questions = QandAData[0]
        Answers = QandAData[1]
    Maxno = len(Questions)
    while Repeat_Deck == True:
        Answer = input("There are "+str(Maxno)+" Questions. How many would you like to be tested on? ")
        Cont = Check_Num_Validity(Answer,Maxno)
        while Cont[0] == False:
            if Cont[1] != "notnum":
                Answer = input("There are "+str(Maxno)+" Questions.Your number was "+Cont[1]+"er than any number between 1-"+str(Maxno)+" ")
            elif Cont[1] == "notnum":
                Answer = input("There are "+str(Maxno)+" Questions.Your number was not a valid number between 1-"+str(Maxno)+" ")
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
            Repeat = input("You can not choose option two as you have answered all the questions choose another option ")
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
            backtostart = False
            return (Repeat_Course,backtostart)
        elif Repeat == "4":
            Repeat_Deck = False
            Repeat_Course = False
            backtostart = False
            return (Repeat_Course,backtostart)
        elif Repeat == "5":
            Repeat_Deck = False
            Repeat_Course = False
            backtostart = True
            return (Repeat_Course,backtostart)  
def Delete_Course(CourseObjects,coursetogo):
    index = 0
    DeckIndex = 0
    for each in CourseObjects:
        if each == coursetogo:
            break
        else:
            index += 1
    for each in coursetogo.Decks:
        for Deck in Course.AllDecks:
            if Deck == each:
                Course.AllDecks.pop(DeckIndex)
            DeckIndex += 1
    shutil.rmtree(coursetogo.Foldername)#deletes all contents of folder and the folder
    CourseObjects.pop(index)
    SaveCourses(CourseObjects)
    return(CourseObjects)
def Check_All_Decks(AllDecks,Deckname): 
    while True:
        index = 0  
        for each in AllDecks:
            if each.name.upper() == Deckname.upper():
                DeckAccessed = each
                AllDecks.pop(index)
                return(DeckAccessed,AllDecks)
            index += 1  
        Deckname = input("What is the name of the Deck you would like to add")        
def main():
    run = True
    index = 0
    CourseObjects = GetCourses()

    while run == True:
        if CourseObjects == []:
            Answer = input("Welcome to Omars Flashcard thing. You currently have no Courses saved , press one to add one, 2 to quit")
            if Answer == "1":
                Coursename = Checkname("Course")
                CreateNewCourse(Coursename,CourseObjects)
                Repetitions = input("How many Decks would you lke to add to this Course(must be greater than 0)?")
                Cont = False
                Repetitions = Check_Repetition_number(Repetitions)
                for i in range(int(Repetitions)):
                    print("Deck "+i)
                    Deckname = Checkname("Deck")
                    CourseObjects[-1].CreateNewDeck(Deckname)
                
            else:
                run == False
        else:
            for each in Course.AllDecks:
                print(each.name)
            print("\n")
            print("""Hello, Welcome to Omars Flashcard file saver.""")
            DisplayCourses(CourseObjects)
            option = input("""Would you like to:
1)Create a new Course or rename a Course
2)Access one of you current Courses and edit the Decks within or add new Decks
3)Open a deck to test yourself on Questions
4)Test yourself on multiple decks
5)Import a file of questions and answers to a new or old deck 
6)Delete Files
7)Quit
press the corrosponding number.
""")

            option = Check_Options(option,7)
            if option == "1":
                backtostart = False
                while backtostart == False:
                    print("\n")
                    Answer = input("""Would you like to:
1)Add a course
2)Rename a Course
3)Quit
""")
                    if Answer == "1":
                        DisplayCourses(CourseObjects)
                        Coursename = Checkname("Course")# you can probablt put this in teh function below
                        CreateNewCourse(Coursename,CourseObjects)
                        Repetitions = input("How many Decks would you lke to add to this Course(must be greater than 0)?")
                        Cont = False
                        Repetitions = Check_Repetition_number(Repetitions)
                        for i in range(int(Repetitions)):
                            print("Deck",i+1)
                            Deckname = Checkname("Deck")
                            CourseObjects[-1].CreateNewDeck(Deckname)
                    elif Answer == "2":
                        DisplayCourses(CourseObjects)
                        AccessSet = input("Which deck would you like to change the name of: ")
                        AccessSet = Access_Course(AccessSet,CourseObjects)
                        Newname = Checkname("Course")
                        AccessSet.RenameCourses(Newname)
                        SaveCourses(CourseObjects)
                    else:
                        backtostart = True

            if option == '2':
                backtostart = False
                print("\n")
                while backtostart == False:
                    DisplayCourses(CourseObjects)
                    AccessCourse = input("Which Course would you like to Access?")
                    CourseAccessed = Access_Course(AccessCourse,CourseObjects)
                    if CourseAccessed.Decks == []:
                        print("That Course is empty")
                        Repetitions = input("How many Decks do you want to add")
                        Repetitions = Check_Repetition_number(Repetitions)
                        for i in range(int(Repetitions)):
                            print("Deck",i+1)
                            Deckname = Checkname("Deck")
                            CourseAccessed.CreateNewDeck(Deckname)                     
                    Samecourse = True
                    while Samecourse == True:
                            
                        print("The Decks within "+CourseAccessed.name+" set are")
                        for each in CourseAccessed.Decks:#shows the Deck within the Course
                            print(each.name)
                        print("\n")
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
                                print("Deck",i+1)
                                Deckname = Checkname("Deck")
                                CourseAccessed.CreateNewDeck(Deckname)
                        elif Answer == '2':
                            backtooptionmenu = False
                            while backtooptionmenu == False:
                                Deckname = input("Which Deck do you want to access?")
                                DeckAccessed = CourseAccessed.GetDeck(Deckname)
                                if DeckAccessed.Alist == []:
                                    Repetitions = input("There are no questions in this Deck, how many do you want to add?(must be >0")
                                    Repetitions = Check_Repetition_number(Repetitions) 
                                    for i in range(int(Repetitions)):
                                        DeckAccessed.AddQandA(i)     
                                    DeckAccessed.SaveQandA()   
                                SameDeck = True
                                while SameDeck == True:
                                    print("The questions and answers within " +DeckAccessed.name +" are:")
                                    index = 0
                                    for each in DeckAccessed.Qlist:
                                        print( str(index+1)+")"+each+"   "+DeckAccessed.Alist[index])
                                        index += 1
                                    print("\n")
                                    Options = input("""Would you like to:
1)Edit a question
2)Edit an answer
3)Add a question and answer
4)Delete a Question and Answer
5)Goback to course menu to edit a different Deck or course
""")
                                    Options = Check_Options(Options,5)
                                    print("\n")
                                    if Options == "1":
                                        Editno = input("which question number would you like to edit? ")
                                        Editno = Get_Answer_or_Question_num(DeckAccessed,Editno)
                                        Edit = input("What would you like to change "+DeckAccessed.Qlist[Editno]+" to? ")
                                        DeckAccessed.Qlist[Editno] = Edit   
                                        DeckAccessed.SaveQandA()
                                    elif Options == "2":
                                        Editno = input("which answer number would you like to edit? ")
                                        Editno = Get_Answer_or_Question_num(DeckAccessed,Editno)
                                        Edit = input("What would you like to change "+DeckAccessed.Alist[Editno]+" to? ")
                                        DeckAccessed.Alist[Editno] = Edit
                                        DeckAccessed.SaveQandA()  
                                    elif Options == "3":
                                        repetitions= input("How many questions and answers would you like to add?")
                                        repetitions = Check_Repetition_number(repetitions)
                                        for i in range(int(repetitions)):
                                            DeckAccessed.AddQandA(i)
                                        DeckAccessed.SaveQandA()
                                    elif Options == "4":
                                        IndextoDelete = input("Which Question number do you want to delete? ")
                                        IndextoDelete = Get_Answer_or_Question_num(DeckAccessed,IndextoDelete)
                                        DeckAccessed.DeleteQandA(int(IndextoDelete))
                                    elif Options == "5":
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
                backtostart = False
                while backtostart == False:
                    chosen = False
                    while chosen == False:
                        DisplayCourses(CourseObjects)
                        print("\n")
                        AccessCourse = input("Which Course would you like to Access? ")
                        CourseAccessed = Access_Course(AccessCourse,CourseObjects)
                        Repeat_Course = True
                        Empty = CheckifCoureseempty(CourseAccessed)
                        if Empty == True:
                            Repeat_Course = False
                            print("\n")
                            Goback = input("""That Course is empty. Would you like to
1)Choose a different course
2)Quit
""")    
                            Check_Options(Goback,2)
                            if Goback == "2":
                                backtostart = True
                                chosen = True
                                cont = False
                        else:
                            chosen = True
                            cont = True
                    if cont == True:
                        print("\n")
                        QtoA = input("""Would you like to test yourself on:
1)Questions to Answers 
2)Answers to Questions
""")
                        QtoA = Check_Options(QtoA,2)
                    while Repeat_Course == True:    
                        RepeatFactors = Ask_one_deck_questions(CourseAccessed,QtoA)
                        Repeat_Course = RepeatFactors[0]
                        backtostart = RepeatFactors[1]
            elif option =="4":
                DecksAvailable = []
                backtostart = False
                while backtostart == False:
                    for each in Course.AllDecks:
                        if each.Qlist != []:
                            DecksAvailable.append(each)
                    TestDecks = []
                    Accessedall = False
                    if DecksAvailable == []:
                        print("")
                        print("There are no Questions to test")
                        backtostart = True
                    else:
                        while Accessedall == False:
                            print("\n")
                            print("Your Decks available to choose from are")
                            for each in DecksAvailable:
                                print(each.name)
                            Deckname = input("Which Deck do you want to add to the list of questions?")
                            DeckAccessed = Check_All_Decks(DecksAvailable,Deckname)
                            TestDecks.append(DeckAccessed[0])
                            DecksAvailable = DeckAccessed[1]
                            if DecksAvailable == []:
                                print("\n")
                                print("You have accessed all the Decks in this course, we will now move on")
                                Accessedall = True
                            else:
                                print("\n")
                                print("You have accessed these Decks")
                                for each in TestDecks:
                                    print(each.name)
                                YorN = input("Would you like to add another Deck Y/N")
                                YorN = CheckYorN(YorN)
                                if YorN.upper() == "N":
                                    Accessedall = True
                        LongQuestions = []
                        LongAnswers = []
                        QtoA = input("""Would you like to:
1) Test your self on Question to answer
2) Test yourself on Answer to Question
""")
                        QtoA = Check_Options(QtoA,2)
                        if QtoA == "1":
                            for each in TestDecks:
                                for Q in each.Qlist:
                                    LongQuestions.append(Q)
                                for A in each.Alist:
                                    LongAnswers.append(A)
                        else:
                            for each in TestDecks:
                                for Q in each.Qlist:
                                    LongAnswers.append(Q)
                                for A in each.Alist:
                                    LongQuestions.append(A)
                        #I will probably turn the next part into a function because it essentially will test questions just like option 3
                        Questions = []
                        Answers = []
                        for each in LongQuestions:
                            Questions.append(each)
                        for each in LongAnswers:
                            Answers.append(each)
                        Repeat_Deck = True
                        while Repeat_Deck == True:
                            Maxno = len(Questions)
                            print("\n")
                            Answer = input("There are "+str(Maxno)+" Questions. How many would you like to be tested on?")
                            Cont = Check_Num_Validity(Answer,Maxno)
                            while Cont[0] == False:
                                if Cont[1] != "notnum":
                                    print("\n")
                                    Answer = input("There are "+str(Maxno)+" Questions.Your number was "+Cont[1]+"er than any number between 1-"+str(Maxno))
                                elif Cont[1] == "notnum":
                                    print("\n")
                                    Answer = input("There are "+str(Maxno)+" Questions.Your number was not a valid number between 1-"+str(Maxno))
                                Cont = Check_Num_Validity(Answer,Maxno)
                            QandAinfo =TestQuestions(Questions,Answers,int(Answer))
                            empty = QandAinfo[2]
                            print("\n")
                            Repeat = input("""Would you like to test yourself again on
    1) The Full set of questions
    2) These questions but without the questions you did this round
    3) Another group of decks 
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
                Answer = input("""Would you like to:
1)Add to an existing Decks questions
2)Create a new Deck and add questions
                                  """)
                Answer = Check_Options(Answer,2)
                DisplayCourses(CourseObjects)
                Accessed_Course = input("Which course would you like to access? ")
                Accessed_Course = Access_Course(Accessed_Course,CourseObjects)
                if Answer == "1":
                    print("the decks within the course are:")
                    for each in Accessed_Course.Decks:
                        print(each.name)
                    ChosenDeck = input("Which deck would you like to access? ")
                    ChosenDeck = Accessed_Course.GetDeck(ChosenDeck)
                else:
                    Deckname = Checkname("Deck")
                    Accessed_Course.CreateNewDeck(Deckname)
                    ChosenDeck = Accessed_Course.Decks[-1]
                FileOption = input("""Would you like to add:
1) A csv file
2) A question and Answer file""")
                FileOption = Check_Options(FileOption,2)
                if FileOption == "1":
                    FileType = ".csv"
                    Filename = input("What's the name of the csv")
                    Filename = CheckFile(Filename,FileType)
                    ChosenDeck.Import_csvQandA(Filename)
                else:
                    FileType = ".txt"
            elif option == "6":
                backtostart = False
                while backtostart == False:
                    Answer = input("""Would you like to delete
1) A deck
2) A course
3) Quit to main menu
""")
                    Answer = Check_Options(Answer,3)
                    DisplayCourses(CourseObjects)
                    if Answer == "1":
                        CourseAccessed = input("What course would you like to access?")     
                        CourseAccessed = Access_Course(CourseAccessed,CourseObjects)
                        print("The decks within "+CourseAccessed.name+" are:") 
                        if CourseAccessed.Decks == []:
                            print("That course has no decks within to begin with")
                        else: 
                            for each in CourseAccessed.Decks:
                                print(each.name)  
                            DeckAccessed = input("which deck wold you like to delete?")   
                            DeckAccessed = CourseAccessed.GetDeck(DeckAccessed) 
                            CourseAccessed.DeleteDeck(DeckAccessed)
                        
                    elif Answer == "2":
                        CourseAccessed = input("What course would you like to Delete?")     
                        CourseAccessed = Access_Course(CourseAccessed,CourseObjects)
                        CourseObjects = Delete_Course(CourseObjects,CourseAccessed)
                    else:
                        backtostart = True
            elif option == "7":
                run = False
main()
