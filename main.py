"""
Malt.io
=======
This is the entry point for the Malt.io backend. It creates a new WSGI
application to serve requests.
"""

import logging
import settings
import webapp2

from models.userprefs import UserPrefs
from urls import urls
from util import get_template


def handle_error(request, response, exception, code, msg):
    """
    Render an error template with a code and message.
    """
    logging.exception(exception)

    template = get_template('error.html')
    response.out.write(template.render({
        'user': UserPrefs.get(),
        'code': code,
        'message': msg
    }))


def handle_404(request, response, exception):
    handle_error(request, response, exception,
                 404, 'the page could not be found')


def handle_500(request, response, exception):
    handle_error(request, response, exception,
                 500, 'there was an internal server error')


app = webapp2.WSGIApplication(urls, debug=settings.DEBUG)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500
