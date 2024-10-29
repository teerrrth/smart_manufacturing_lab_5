#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/22 18:32
# @Author  : Fred Livingston (fjliving@ncsu.edu)

# Cntr + Shift + P -> Python: Select Interpreter -> Python 3.11.9 64-bit ('smartm': conda) -> Enter
from flask import Flask
from flask import render_template
from flask import request, jsonify
import paho.mqtt.client as mqtt_client
import json
from flask_classful import FlaskView

app = Flask(__name__)

class ClientApp(FlaskView):
    def __init__(self, mqtt_host_address):
        # instantiate an object:
        self.mqtt_host = mqtt_host_address
        self.mqtt_port = 1883
        self.mqtt_keep_alive = 60

        # Initialize MQTT Client
        self. _init_mqtt()
        print("MQTT Client Initialized")

        @app.route('/control', methods=['GET', 'POST', 'DELETE', 'PATCH'])
        def index():
            # send form to the user
            if request.method == 'GET':
                return render_template('widget_mqtt.html')
    
            if request.method == 'POST':
                action = request.form.get("action") 
                print(action)
        
            if(action == "Start Controller"):
                self._enabled_disable_system(True)
        
            if(action == "Stop Controller"):
                self._enabled_disable_system(False)
            return render_template('widget_mqtt.html') 
        
    def _init_mqtt(self):
        # Initialize MQTT Client
        try:
            self.mqttc = mqtt_client.Client()
            self.mqttc.connect(self.mqtt_host, self.mqtt_port, self.mqtt_keep_alive)
        except Exception as e:
            print("Error in MQTT Client Initialization: ", e)

    def _enabled_disable_system(self, enable):
        mqtt_topic = "FWH/2311/Micro850-2.ie.ncsu.edu/SystemCommand"
        dataObj={}
        dataObj["enable system"] = enable
        jsondata = json.dumps(dataObj)
        self.mqttc.publish(mqtt_topic, jsondata)
        print ("Controller: ", enable)
       
mqtt_host = "10.155.14.88"
app_client = ClientApp(mqtt_host)
ClientApp.register(app) # Register the class with the app
app.run(debug=True)