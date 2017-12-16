#!/usr/bin/env python
import pika, json, smtplib, os
from subprocess import CalledProcessError, check_call

MAX_TEMPERATURE = float(35)
MIN_TEMPERATURE = float(10)
MAX_HUMIDITY = float(50)
MIN_HUMIDITY = float(20)

telegram_conf_args = ["--config", "/etc/telegram-send.conf"]

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='temp_and_humidity',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='temp_and_humidity',
                   queue=queue_name)

def sendMessage(sensor_name, datetime, temperature, humidity):
  message = 'Anomaly detected! Sensor: ' + sensor_name + ', Time: ' + datetime + ', Temperature: ' + temperature + ', Humidity: ' + humidity
  try:
    check_call(["telegram-send", message] + telegram_conf_args)
  except OSError:     # command not found
    cmd = expanduser("~/.local/bin/telegram-send")
    check_call([cmd, message] + telegram_conf_args)

def callback(ch, method, properties, body):
  data = json.loads(body)
  if float(data['temperature']) > MAX_TEMPERATURE or float(data['temperature']) < MIN_TEMPERATURE or float(data['humidity']) > MAX_HUMIDITY or float(data['humidity']) < MIN_HUMIDITY:
    print 'Anomaly alerted! Sensor: ', data['sensor_name'], ', Time: ', data['datetime'], ', Temperature: ', data['temperature'], ', Humidity:', data['humidity']
    sendMessage(data['sensor_name'],
      data['datetime'],
      data['temperature'],
      data['humidity'])

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
