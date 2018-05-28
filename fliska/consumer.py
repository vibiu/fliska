"""
@author: LaiQiang
@contact: vibiu@qq.com
@time: 2018/5/16 11:10
"""

import pika

from .context import RequestContext, AppContext


class Logger:

    def _write_log(self, filename, msg):
        with open(filename, 'a') as f:
            f.write(msg + '\n')

    def log(self, level, msg):
        log_msg = 'LOGGING[{}]: {}'.format(level, msg)
        self._write_log('test.log', log_msg)
        print(log_msg)

    def info(self, msg):
        info_msg = 'INFO: {}'.format(msg)
        self._write_log('test.log', info_msg)
        print(info_msg)

    def error(self, msg):
        error_msg = 'ERROR: {}'.format(msg)
        self._write_log('test.log', error_msg)
        print(error_msg)


class PikaConsumer:

    def __init__(self, host=None, port=None, username=None, password=None):
        self.host = host
        self.port = port
        self._credentials = pika.PlainCredentials(username, password)
        self._conection_parameters = pika.ConnectionParameters(
            host, port, '/', self._credentials)
        self.connection = pika.BlockingConnection(self._conection_parameters)
        self._channel = self.connection.channel()
        self._channel.basic_qos(prefetch_count=1)
        self._logger = Logger()

    def add_callback(self, channel, callback):
        self._channel.queue_declare(queue=channel, durable=True)
        self._channel.basic_consume(callback, queue=channel)

    def add_logger(self, logger):
        self._logger = logger

    def log(self, level, msg):
        self._logger.log(level, msg)

    def info(self, msg):
        self._logger.info(msg)

    def error(self, msg):
        self._logger.error(msg)

    def channel(self, channel, **kwargs):
        def decorator(cb):

            def try_cb(ch, method, properties, body):
                ctx = self.request_context(body)
                ctx.push()
                routing_key = method.routing_key
                msg = "[{}] Received {}".format(routing_key, body)
                self.info(msg)
                try:
                    cb(ch, method, properties, body)
                except Exception as error:
                    errmsg = 'internal error, channel: {}, body: {}, ' \
                        'errmsg: {}'.format(routing_key, body, error)
                    self.error(errmsg)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
            self.add_callback(channel, try_cb)
            return try_cb
        return decorator

    def app_context(self):
        return AppContext(self)

    def request_context(self, channel_body):
        return RequestContext(self, channel_body)

    def run(self):
        self.info('listening to: {}:{}'.format(
            self.host, self.port))
        self.info('Waiting for messages. To exit press CTRL+C')
        self._channel.start_consuming()
