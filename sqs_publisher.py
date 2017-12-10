#!/usr/bin/env python
import pika, json, boto3

sqs = boto3.client('sqs')
queue_url = 'https://sqs.eu-west-1.amazonaws.com/340053764926/temp-and-humidity.fifo'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='temp_and_humidity',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='temp_and_humidity',
                   queue=queue_name)

def callback(ch, method, properties, body):
  data = json.loads(body)
  print body
  response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=body,
    MessageGroupId='temp_and_humidity'
  )
  print(response['MessageId'])

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
