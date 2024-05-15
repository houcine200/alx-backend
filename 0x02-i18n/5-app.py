#!/usr/bin/env python3
"""Mock logging in by creating a user login system"""
from flask import Flask, render_template, g, request
from flask_babel import Babel
from typing import Dict, Union


app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration class for Flask app."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale() -> str:
    """Check if locale parameter is present in the request URL."""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user(user_id: int) -> Dict:
    """
    Function that returns a user dictionary or None
    if the ID cannot be found or if login_as was not passed
    """
    return users.get(int(user_id))


@app.before_request
def before_request():
    """Function and use the app.before_request decorator to
    make it be executed before all other functions. It should use
    get_user to find a user if any, and set it as a global on flask.g.user.
    """
    user_id = (request.args.get('login_as', 0))
    g.user = get_user(user_id)


@app.route('/')
def index() -> str:
    """Render the index HTML file"""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(debug=True)
