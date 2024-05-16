#!/usr/bin/env python3
'''Basic Flask application'''
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz

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


def get_user(user_id) -> dict:
    '''Return user dictionary based on user ID'''
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request():
    '''Set user global on flask.g'''
    id = request.args.get('login_as', None)
    g.user = get_user(id)


@babel.localeselector
def get_locale() -> str:
    '''Get the preferred language based on the user's request'''
    # 1. Locale from URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    # 2. Locale from user settings
    if (
        g.user and 'locale' in g.user and
        g.user['locale'] in app.config['LANGUAGES']
    ):
        return g.user['locale']

    # 3. Locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])

    # 4. Default locale
    # return app.config['BABEL_DEFAULT_LOCALE']


SUPPORTED_TIMEZONES = pytz.all_timezones


@babel.timezoneselector
def get_timezone() -> str:
    '''Get the preferred time zone based on the user's request'''
    timezone = request.args.get('timezone')
    if timezone and timezone in SUPPORTED_TIMEZONES:
        return timezone
    if (
        hasattr(g, 'user') and g.user and 'timezone' in g.user and
        g.user['timezone'] in SUPPORTED_TIMEZONES
    ):
        return g.user['timezone']
    return 'UTC'


@app.route('/')
def index() -> str:
    '''Returns the rendered template for index.html page'''
    from datetime import datetime
    fr_format = "%d %b %Y à %H:%M:%S"
    en_format = '%b %d, %Y, %I:%M:%S %p'
    format = fr_format if get_locale() != 'en' else en_format
    utc_time = datetime.utcnow()
    timezone = pytz.timezone(get_timezone())
    localized_time = utc_time.astimezone(timezone)

    formatted_time = localized_time.strftime(format)
    return render_template('index.html', current_time=formatted_time)


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
