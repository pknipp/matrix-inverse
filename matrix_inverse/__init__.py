import cmath
from flask import Flask
from . import helper

app = Flask(__name__)

# The following are used to wrap the html string created for server-side rendering.
top = "<head><title>Matrix inverse</title></head><body>"
bottom = "<span>creator:&nbsp;<a href='https://pknipp.github.io/' target='_blank' rel='noopener noreferrer'>Peter Knipp</a></span></body>"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')


@app.route('/')
def hello():
    html = top + "<h3><p align=center>" + "/".join(helper.instructions) + "</p></h3>" + bottom
    return html

@app.route('/<str_in>')
def return_html(str_in):
    # results = helper.parse_roots(str_in, False)
    results = '<h1>Hello world</h1>'
    if isinstance(results, str):
        return top + results + bottom
    else:
        return '<h1>' + results["error"] + '</h1>'

@app.route('/json/<square_in>')
def json_square(square_in):
    return helper.parse(True, square_in)

@app.route('/json/<square_in>/<rect_in>')
def json_rect(square_in, rect_in):
    return helper.parse(True, square_in, rect_in)
