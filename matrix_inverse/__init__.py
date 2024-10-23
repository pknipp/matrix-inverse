import cmath
from flask import Flask
from . import helper

app = Flask(__name__)

# The following are used to wrap the html string created for server-side rendering.
top = "<head><title>Matrix inverse</title></head><body>"
bottom = "<p align=center>creator:&nbsp;<a href='https://pknipp.github.io/' target='_blank' rel='noopener noreferrer'>Peter Knipp</a><br/>repo:&nbsp;<a href='https://github.com/pknipp/matrix-inverse' target='_blank'  rel='noopener noreferrer'>github.com/pknipp/matrix-inverse</a></p></body>"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')


@app.route('/')
def hello():
    html = top + "<h3><p align=center>Instructions for Matrix Inversion:</p></h3>"
    html += '<p align=center><a href="https://pknipp.github.io/math">Return</a> to the Math APIs page.<ul>'
    for instruction in helper.instructions:
        html += "<li>" + instruction + "</li>"
    return html + "</ul>" + bottom + '</p>'

@app.route('/<square_in>')
def square(square_in):
    results = helper.parse(False, square_in)
    if isinstance(results, str):
        return top + results + '</body>'
    else:
        html = '<h4>' + results["error"]["message"] + '</h4><div>Problematic string(s)</div><ul>'
        print("strings is ", results["error"]["strings"])
        for string in results["error"]["strings"]:
            html += '<li>' + string + '</li>'
        return html + '</ul>'

@app.route('/<square_in>/<rect_in>')
def rect(square_in, rect_in):
    results = helper.parse(False, square_in, rect_in)
    if isinstance(results, str):
        return top + results + "</body>"
    else:
        html = '<h4>' + results["error"]["message"] + '</h4><div>Problematic string(s)</div><ul>'
        for string in results["error"]["strings"]:
            html += '<li>' + string + '</li>'
        return html + '</ul>'

@app.route('/json/<square_in>')
def json_square(square_in):
    return helper.parse(True, square_in)

@app.route('/json/<square_in>/<rect_in>')
def json_rect(square_in, rect_in):
    return helper.parse(True, square_in, rect_in)
