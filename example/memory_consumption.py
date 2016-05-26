import tornado.ioloop
import tornado.web
import tornado.websocket
import pika

settings = {
    url: "amqp://localhost:5672",
    exchange: "simstream",
    queue: "remote_node",
    routing_key: "unique_key",
    exchange_type: "topic"
}


class PlotHandler(tornado.web.RequestHandler):

    def get(self, collector, command):
        pass


class StreamingHandler(tornado.websocket.WebSocketHandler):

    def on_open(self, exchange, queue, routing_key):
        pass

    def on_message(self, collector, command):
        pass

    def on_close(self):
        pass

    def write_message(self):
        pass


if __name__ == "__main__":
    app = tornado.web.Application([
            (r"/plot/(.*)", )
            (r"/stream/(.*)", StreamingHandler)
        ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
