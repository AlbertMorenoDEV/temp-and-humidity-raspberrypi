#!/usr/bin/env python
import pika, json, smtplib, os

max_temperature = 10
mail_account = os.getenv('MAIL_ACCOUNT')
mail_password = os.getenv('MAIL_PASSWORD')
destination_mail = 'albert.moreno.dev@gmail.com'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='temp_and_humidity',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='temp_and_humidity',
                   queue=queue_name)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.connect("smtp.gmail.com",465)
server.ehlo()
server.starttls()
#server.ehlo()
server.login(mail_account, mail_password)
server.quit()

msg = "\nHello!" # The /n separates the message from the headers
server.sendmail(mail_account, destination_mail, msg)

def callback(ch, method, properties, body):
  print body
  data = json.loads(body)
  if data['temperature'] > max_temperature:
    print('Temperature alert')

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
