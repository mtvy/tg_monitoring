#/==================================================================\#
# webhook.py                                          (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
import cherrypy

from stun          import get_ip_info
from telebot       import TeleBot
from telebot.types import Update
#------------------------\ project modules /-------------------------#
from back.utility  import logging
from back.vars     import WEBHOOK_SET, \
                          WEBHOOK_CONFIG, \
                          WEBHOOK_URL_PATH
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
#                               WebHook                              #
#\------------------------------------------------------------------/#
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

    #bot.remove_webhook(); bot.set_webhook(**WEBHOOK_SET)

    #cherrypy.config.update(WEBHOOK_CONFIG)

    #cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

    return True
#\------------------------------------------------------------------/#
