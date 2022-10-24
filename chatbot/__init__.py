import azure.functions as func
from .chatbotapp import flask_app

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    return func.WsgiMiddleware(flask_app.wsgi_app).handle(req, context)