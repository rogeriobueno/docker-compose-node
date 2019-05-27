import psycopg2
import redis
import json
import os
from bottle import Bottle, request

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)

        REDIS_HOST = os.getenv('REDIS_HOST', 'queue')
        self.fila = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

        DB_HOST = os.getenv('DB_HOST', 'db')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_NAME = os.getenv('DB_NAME', 'sender')
        
        dsn = f'dbname={DB_NAME} user={DB_USER} host={DB_HOST}'
        self.conn = psycopg2.connect(dsn)
        
    def register_message(self, assunto, mensagem):
        SQL = 'INSERT INTO emails (assunto, mensagems) VALUES (%s, %s)'
        cur = self.conn.cursor()
        cur.execute(SQL, (assunto, mensagem))
        self.conn.commit()
        cur.close()

        msg = {'assunto': assunto, 'mensagem': mensagem}
        self.fila.rpush('sender', json.dumps(msg))

        print('Mensagem registrada !')

    def send(self):
        assunto = request.forms.get('assunto')
        mensagem = request.forms.get('mensagem')

        self.register_message(assunto, mensagem)
        return 'Mensagem enfileirada ! Assunto: {} Mensagem: {}'.format(
            assunto, mensagem
        )

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)