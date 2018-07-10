from fliska import PikaConsumer
from fliska import request

rabbitmq_config = {
    'host': 'localhost',
    'port': 5672
}

URI = 'guest:guest@localhost:5672'

consumer = PikaConsumer(
    host=rabbitmq_config['host'],
    port=rabbitmq_config['port'],
    username='guest',
    password='guest')


@consumer.channel('test')
def test_callback(ch, method, property, body):
    print(request)
    print('hello')
    return ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    consumer.run()


if __name__ == '__main__':
    main()
