#\------------------------------------------------------------------/#
import cherrypy

from stun          import get_ip_info
from telebot       import TeleBot
from telebot.types import Update
from back.utility  import logging
#\------------------------------------------------------------------/#

TOKEN = ...

WEBHOOK_HOST   = ...#get_ip_info()[1]
WEBHOOK_PORT   = 8443  
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = f'https://{WEBHOOK_HOST}:{WEBHOOK_PORT}'
WEBHOOK_URL_PATH = f'/{TOKEN}/'

WEBHOOK_CONFIG = {
    'server.socket_host'    : WEBHOOK_LISTEN,
    'server.socket_port'    : WEBHOOK_PORT,
    'server.ssl_module'     : 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV,
    'log.access_file'       : 'access.log',
    'log.error_file'        : 'errors.log',
    'log.screen'            : False
}

WEBHOOK_SET = {
    'url'         : WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, 
    'certificate' : ... #open(WEBHOOK_SSL_CERT, 'r')
}


#\------------------------------------------------------------------/#
#                               WebHook                              #
#\------------------------------------------------------------------/#
class WebhookServer(object):
    """## Webhook Proc Class ##"""
    
    @cherrypy.expose
    def index(self, bot : TeleBot):
        _hdrs = cherrypy.request.headers
        _body = cherrypy.request.body

        if 'content-length' in _hdrs and \
             'content-type' in _hdrs and \
                _hdrs['content-type'] == 'application/json':

            length      = int(_hdrs['content-length'])
            json_string = _body.read(length).decode("utf-8")
            update      = Update.de_json(json_string)

            bot.process_new_updates([update])

            return ''
        else:
            raise cherrypy.HTTPError(403)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def proc_bot(bot : TeleBot) -> bool:

    bot.remove_webhook(); bot.set_webhook(**WEBHOOK_SET)

    cherrypy.config.update(WEBHOOK_CONFIG)

    cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

    return True
#\------------------------------------------------------------------/#
