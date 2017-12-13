#!/usr/bin/env python
import pika, json, boto3

sns = boto3.client('sns')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='temp_and_humidity',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='temp_and_humidity',
                   queue=queue_name)

topicArn = sns.create_topic(
    Name='temp_and_humidity'
)['TopicArn']

print topicArn

def callback(ch, method, properties, body):
  print body
  response = sns.publish(
    TargetArn=topicArn,
    Message=body
  )
  print(response['MessageId'])

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
