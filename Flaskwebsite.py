from flask import Flask, url_for, redirect, render_template
from New_FlashCard_program import GetCourses
courses = GetCourses()

app = Flask(__name__)
@app.route("/AllCourses")
def home():
    return render_template("Decks.html",Courses = courses)

@app.route("/AllCourses/<Coursename>")
def edit(Coursename):
    return render_template("DecksViewer.html",Decklist = courses[0].Decks, name = Coursename)

for each in courses[0].Decks:
    print(each.name)
if  __name__ == "__main__":
    app.run(debug = True)