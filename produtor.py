import pika

# Estabelece a conexão com o RabbitMQ
#connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))

channel = connection.channel()

# Declara a fila do consumidor
channel.queue_declare(queue='consumidor')

# Envia endereços IP para a fila
enderecos_ip = ['101.33.24.255', '101.33.9.255', '101.46.167.255', '45.70.227.255']
for ip in enderecos_ip:
    channel.basic_publish(exchange='', routing_key='consumidor', body=ip)
    print("Endereço IP enviado:", ip)

# Fecha a conexão
connection.close()
