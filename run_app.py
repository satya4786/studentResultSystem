import optparse
from apps.routes import app
from sys import exit as sys_exit

__AUTHOR__ = 'RAMESH KUMAR'


def run_with_tornado(port, debug_mode):
    """
    Instantiate tornado HTTServer and wrap apps in it and start the IOLoop.
    """
    try:
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        print 'Tornado on port {port} ...'.format(port=port)
        app.debug = debug_mode
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(port)
        IOLoop.instance().start()
    except ImportError:
        print 'ERROR: tornado is not installed in this environment. Please install and try again'
        sys_exit(1)


def run_with_twisted(port, debug_mode):
    """
    Import twisted dependencies, set apps as WSGIResource and start reactor.
    """
    try:
        from twisted.internet import reactor
        from twisted.web.server import Site
        from twisted.web.wsgi import WSGIResource
        print 'Twisted on port {port} ...'.format(port=port)
        app.debug = debug_mode
        resource = WSGIResource(reactor, reactor.getThreadPool(), app)
        site = Site(resource)

        reactor.listenTCP(port, site, interface="0.0.0.0")
        reactor.run()
    except ImportError:
        print 'ERROR: twistd is not installed in this environment. Please install and try again.'
        sys_exit(1)


def run_with_builtin(port, debug_mode):
    """
    Run with default builtin flask/klein/bottle apps
    """
    print 'Built-in development server on port {port} ...'.format(port=port)
    app.run(host="0.0.0.0", port=port, debug=debug_mode)


def main():
    """
    Parse the options to get WSGi container of choice, the debug mode, and the port number"
    """
    parser = optparse.OptionParser(usage="%prog [options]  or type %prog -h (--help)")
    parser.add_option('-p', '--port',
                      help='Port on which to run service, defaults to 5005',
                      dest="app_port",
                      type="int",
                      default=1402)
    parser.add_option('--debug',
                      help='When passed, sets apps in debug mode',
                      dest="debug_mode",
                      action="store_true",
                      default=False)
    parser.add_option('-w', '--with',
                      type='choice',
                      action='store',
                      dest='app_container',
                      choices=['builtin', 'tornado', 'twistd'],
                      default='builtin',
                      help='WSGI used to wrap and run the apps. Valid options - builtin/tornado/twistd. Defaults to builtin')
    (options, args) = parser.parse_args()

    port = options.app_port
    debug_mode = options.debug_mode

    if options.app_container == 'tornado':
        run_with_tornado(port, debug_mode)
    elif options.app_container == 'twistd':
        run_with_twisted(port, debug_mode)
    else:
        run_with_builtin(port, debug_mode)


if __name__ == '__main__':
    main()
