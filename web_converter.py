# from app import app
from exercise_converter.helper.exerciseconverterfunctions import get_exercises, render_exercises, change_part_of_markup, get_exercise_meta_information_from_string, write_exercises_to_file 
from io import StringIO

from flask import Flask, request, redirect, url_for, render_template, jsonify



# This class makes it possible to host the flask app 
# under a sub url behind a nginx reverse proxy server.
# Solution from http://flask.pocoo.org/snippets/35/
class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the 
    front-end server to add these headers, to let you quietly bind 
    this to a URL other than / and to an HTTP scheme that is 
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)




app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

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


def convert_exercises_from_tex_to_json(filecontent):
    outfile = StringIO()
    converted_exercise = filecontent
    rendered_exercises = converted_exercise
    exercise_meta_information = get_exercise_meta_information_from_string(converted_exercise.split('\n'))
    exercises = list(get_exercises(change_part_of_markup(converted_exercise.split('\n'))))
    rendered_exercises = render_exercises(exercises)
    write_exercises_to_file(outfile, exercise_meta_information,
            rendered_exercises)
    outfile.seek(0)
    simplified=outfile.read()
    return simplified


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    print("In submit")
    if request.method == 'POST':
        converted_exercise = request.form['exercise_input']
        simplified = convert_exercises_from_tex_to_json(converted_exercise)
        return render_template('index.html',
            converted_exercise=simplified.replace("\r", "\\n"), 
            original_input=converted_exercise)
    else:
        return render_template('index.html')
        

@app.route('/_convert_exercises', methods=['GET'])
def convert_exercises():
    file_contents = request.args.get('file_contents', '', type=str)
    json_representation = convert_exercises_from_tex_to_json(file_contents)
    return jsonify(result=json_representation)
