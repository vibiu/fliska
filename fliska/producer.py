import pika


class PikaProducer:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self._rabbitmq_config = self.app.config.get('RABBITMQ_CONFIG', None)
        if not self._rabbitmq_config:
            raise ValueError('please set RABBITMQ_CONFIG to app.config')

        self._connection_params = pika.ConnectionParameters(
            host=self._rabbitmq_config['host'],
            port=self._rabbitmq_config['port'])

    def publish(self, queue, body):
        self._connection = pika.BlockingConnection(self._connection_params)
        channel = self._connection.channel()
        channel.queue_declare(queue=queue, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2))
        self._connection.close()


class PurePikaProducer:
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port
        self._connection_params = pika.ConnectionParameters(
            host=self.host, port=self.port)

    def publish(self, queue, body):
        self._connection = pika.BlockingConnection(self._connection_params)
        channel = self._connection.channel()
        channel.queue_declare(queue=queue, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2))
        self._connection.close()
