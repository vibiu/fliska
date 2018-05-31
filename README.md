A wrapper of [pika](https://github.com/pika/pika)
To make it's coding like [flask](https://github.com/pallets/flask).

Server Example:
```python
from fliska import PikaConsumer, request


consumer = PikaConsumer(
    host='localhost',
    port=5672,
    username='guest',
    password='guest')

@consumer.channel('test')
def test_callback(ch, method, property, body):
    print(request)
    return ch.basic_ack(deliverty_tag=method.delivery_tag)

consumer.run()
```

Client Example:
```python
from fliska import PurePikaProducer

producer = PurePikaProducer(host='localhost', port=5672)
data = json.dumps({'msg': 'success', 'data': []})
producer.publish('test', data)
```
