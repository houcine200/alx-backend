#!/usr/bin/env python3
'''Basic Flask application'''
from flask import Flask, render_template, request, g
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


class Config():
    '''Configuration class for the application'''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> dict:
    '''Return user dictionary based on user ID'''
    id = request.args.get('login_as')
    if id and int(id) in users:
        return users.get(int(id))
    return None


@app.before_request
def before_request():
    '''Set user global on flask.g'''
    g.user = get_user()



@babel.localeselector
def get_locale() -> str:
    '''Get the preferred language based on the user's request'''
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    '''Returns the rendered template for index.html page'''
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
