import pika
import mysql.connector

import requests

def obter_regiao_cidade(endereco_ip):
    url = f"http://ipapi.co/{endereco_ip}/json"
    resposta = requests.get(url)
    dados = resposta.json()
    regiao = dados.get('region')
    cidade = dados.get('city')
    return regiao, cidade

# Função para verificar e criar a tabela no banco de dados
def verificar_criar_tabela(cursor):
    tabela_existe = False
    cursor.execute("SHOW TABLES LIKE 'mensagens'")
    resultado = cursor.fetchone()
    if resultado:
        tabela_existe = True
    else:
        cursor.execute("CREATE TABLE mensagens (id INT AUTO_INCREMENT PRIMARY KEY, ip VARCHAR(45), regiao VARCHAR(100), cidade VARCHAR(100))")
        tabela_existe = True

    return tabela_existe

# Estabelece a conexão com o RabbitMQ
#connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))

channel = connection.channel()


# Define a fila do consumidor
channel.queue_declare(queue='consumidor')

# Conexão com o banco de dados
cnx = mysql.connector.connect(user='root',password='root', host='db', database='banco_de_ip')
cursor = cnx.cursor()

# Verificar e criar tabela se necessário
tabela_existe = verificar_criar_tabela(cursor)

# Função chamada quando uma mensagem é recebida
def callback(ch, method, properties, body):
    ip = body.decode()
    print("Endereço IP recebido:", ip)

    if tabela_existe:
        # Converter IP em região e cidade
        regiao, cidade = obter_regiao_cidade(ip) #linha dentro do if

        # Salvar mensagem no banco de dados
        insert_query = "INSERT INTO mensagens (ip, regiao, cidade) VALUES (%s, %s, %s)"
        data = (ip, regiao, cidade)
        cursor.execute(insert_query, data)
        cnx.commit()
        print("Mensagem salva no banco de dados: IP =", ip, "Região =", regiao, "Cidade =", cidade) #linha dentro do if

# Define a função de callback para receber mensagens
channel.basic_consume(queue='consumidor', on_message_callback=callback, auto_ack=True)
print('ok')
# Inicia o consumo de mensagens
channel.start_consuming()

# Fecha a conexão com o banco de dados
cursor.close()
cnx.close()
