
import os
import tornado.httpserver
import tornado.options
import tornado.web
import tornado.ioloop
import tornado.autoreload
import models

from tornado.options import define, options

define('port', default=8888, help="Server Port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    '''
    Class
    '''

    def get(self):
        '''
        Function
        '''
        self.render('index.html')

    def data_received(self, message):
        '''
        Function
        '''
        pass


class FetchPublicRepoHandler(tornado.web.RequestHandler):
    '''
    Class
    '''

    def get(self):
        '''
        Function
        '''
        data = models.get_repos()
        self.write(data)

    def data_received(self, message):
        '''
        Function
        '''
        pass


if __name__ == '__main__':
    tornado.options.parse_command_line()

    for filename in os.listdir(os.getcwd()):
        tornado.autoreload.watch(filename)

    STATIC_PATH = os.path.join(os.path.dirname('__FILE__'), 'static')
    STATICHANDLER = tornado.web.StaticFileHandler
    HANDLERS = [(r'/', IndexHandler),
                (r'/static/(.*)', STATICHANDLER, {'path': STATIC_PATH}),
                (r'/repos', FetchPublicRepoHandler)]

    APP = tornado.web.Application(handlers=HANDLERS,
                                  autoreload=True)

    HTTPSERVER = tornado.httpserver.HTTPServer(APP)
    HTTPSERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
