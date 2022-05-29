from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Yo, it's ya boy"
def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()