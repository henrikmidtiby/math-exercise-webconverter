# from app import app
from exercise_converter.helper.exerciseconverterfunctions import get_exercises, render_exercises, change_part_of_markup, get_exercise_meta_information_from_string, write_exercises_to_file 
from io import StringIO

from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', 
            converted_exercise="",
            original_input=r"""\documentclass{article}
\usepackage{tekvideoexercises}

\begin{document}
\exercisename{Gange parenteser sammen}
\tableofcontents
\newpage

\begin{exercise}{Polynomier 1-1}

Reducér $(2+3x)(5-2x)$.

\answerbox{-6x^2 +11x + 10}

\hint

Gang parentesen ud
\[
(2+3x)(5-2x) = 2 \cdot 5 + 2 \cdot (-2x) + 3x \cdot 5 + 3x \cdot (-2x)
\]

\hint

Reducér udtryk
\[
= 10 -4x + 15x-6x^2
\]


\hint

Saml leddene 
\[
= -6x^2 +11x + 10
\]

\end{exercise}


\end{document}""")

@app.route('/name/<name>')
def hello_world_named(name):
    return 'Welcome %s' % name

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    print("In submit")
    if request.method == 'POST':
        outfile = StringIO()
        converted_exercise = request.form['exercise_input']
        rendered_exercises = converted_exercise
        exercise_meta_information = get_exercise_meta_information_from_string(converted_exercise.split('\n'))
        exercises = list(get_exercises(change_part_of_markup(converted_exercise.split('\n'))))
        rendered_exercises = render_exercises(exercises)
        write_exercises_to_file(outfile, exercise_meta_information,
                rendered_exercises)
        outfile.seek(0)
        simplified=outfile.read()
        return render_template('index.html',
                converted_exercise=simplified.replace("\r", "\\n"), 
                original_input=converted_exercise)
    else:
        return render_template('index.html')
        

