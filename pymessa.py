import pika
import time
import argparse


class Connect:
    def __init__(self, host='localhost'):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()

    def start_queue(self, name, msg=' [*] Waiting for messages. '):
        self.channel.queue_declare(queue=name, durable=True)
        print(msg)

    def start_consumer(self, queuename):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self._callback,queue=queuename)
        self.channel.start_consuming()

    def _callback(ch, method, properties, body):
        time.sleep( body.count('.') )
        print (" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pymessa.')
    parser.add_argument('--queuename', help='Set queuename')
    parser.add_argument('--host', help='Set hostname')
    args = parser.parse_args()
    connect = Connect(host=args.host)
    connect.start_consumer(args.queuename)
