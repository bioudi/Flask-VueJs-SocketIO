from flask import Flask
from flask_socketio import SocketIO,emit
import pprint
import requests
from bs4 import BeautifulSoup
import re
import schedule
import time
import thread
import threading
from time import gmtime, strftime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['firstConnect'] = False
socketio = SocketIO(app)

class myThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
      while True:
          print "Starting Web Scraping"
          refreshDB()
          time.sleep(120)


def refreshDB():
    societes=[]
    r = requests.get("https://www.wafabourse.com/marches/actions/r")
    soup = BeautifulSoup(r.content,'html.parser')
    data = soup.find_all("td",{"class": "longNameQS"})
    c=0
    for d in data:
        link = "https://www.wafabourse.com/"+str(d.a.get("href"))
        r1 = requests.get(link)
        soup_societe_titles = BeautifulSoup(r1.content,'html.parser')
        data_societe_titles = soup_societe_titles.find_all("div",{"class": "titre"})
        data_societe_codes = soup_societe_titles.find_all("div",{"class": "markettitleisin"})
        data_nbre_actions = soup_societe_titles.find_all("td",{"class": "bidNbOrders"})
        data_qte_actions = soup_societe_titles.find_all("td",{"class": "bidVolume"})
        data_prix_action = soup_societe_titles.find_all("td",{"class": "bidPrice"})
        data_date_ordre = soup_societe_titles.findAll("td",{"class": "lastPriceDateTime"})
        date_ordre = (data_date_ordre[1].text).encode('utf-8').strip()
        societe_ = {
            "code_societe": None,
            "nom_societe": None,
            "ordre_achat": [],
            "ordre_vente": []
        }
        societe_['code_societe'] = (data_societe_codes[0].text).encode('utf-8').strip()
        societe_['nom_societe'] = (data_societe_titles[0].h1.text).encode('utf-8').strip()
        cc=0
        id_ordre = 0
        for d in data_nbre_actions:
            nbre = (d.text).encode('utf-8').strip()
            if(nbre != "-"):
                qte = (data_qte_actions[cc].text).encode('utf-8').strip()
                price = (data_prix_action[cc].text).encode('utf-8').strip()
                id_ordre += 1
                societe_['ordre_achat'].append({"id":id_ordre,"nbre_actions": nbre,"qte": qte,"prix_action": price,"date_ordre": date_ordre,"type_ordre":"Achat"})
            cc+=1
        data_nbre_actions_V = soup_societe_titles.find_all("td",{"class": "askNbOrders"})
        data_qte_actions_V = soup_societe_titles.find_all("td",{"class": "askVolume"})
        data_prix_action_V = soup_societe_titles.find_all("td",{"class": "askPrice"})
        cc = 0
        for d in data_nbre_actions_V:
            nbre_V = (d.text).encode('utf-8').strip()
            if(nbre_V != "-"):
                qte_V = (data_qte_actions_V[cc].text).encode('utf-8').strip()
                price_V = (data_prix_action_V[cc].text).encode('utf-8').strip()
                id_ordre += 1
                societe_['ordre_vente'].append({"nbre_actions": nbre_V,"qte": qte_V,"prix_action": price_V,"date_ordre": date_ordre,"type_ordre":"Vente"})
            cc+=1
        c+=1
        societes.append(societe_)
        print strftime("[ %H:%M:%S ]", gmtime())+" "+societe_['code_societe']+"-"+societe_['nom_societe']
    socketio.emit('data-arrived',societes)
    print "Data sent to client"

@socketio.on('first-connect')
def handleMessage(msg):
    print "# User Connected ..."
    if app.config['firstConnect'] == False :
        try:
            t = myThread(1,"FirstThread")
            t.start()
        except:
            print "Error: unable to start thread"
        app.config['firstConnect'] = True

@socketio.on('ping')
def pongResponse():
    emit('pong')

if __name__ == '__main__':
    socketio.run(app)
