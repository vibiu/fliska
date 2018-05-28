from fliska import PurePikaProducer


def main():
    pure_pika_producer = PurePikaProducer(host='localhost', port=5672)
    import json
    data = {
        'msg': 'success',
        'data': []
    }
    channel = 'test'
    strdata = json.dumps(data)
    print('publish... data: {}'.format(strdata))
    pure_pika_producer.publish(channel, strdata)


if __name__ == '__main__':
    main()
