
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
