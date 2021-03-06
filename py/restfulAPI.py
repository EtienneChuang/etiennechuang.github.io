from flask import Flask
from flask_restful import Resource, Api
import json
from flask_jsonpify import jsonify
from flask_cors import CORS
import urllib
import ssl
import requests
import csv
import sys
app = Flask(__name__)
CORS(app)
api = Api(app)
encoding = "utf-8"

def fetchCsvData(url):
	try:
		response = requests.get(url, verify=False)
		decoded_content = response.content.decode('utf-8')
		csvData = decoded_content.split('\r\n')
		csvData = csvData[:-1]
		#print(csvData)
		return csvData
	except Exception as e:
		print(e)

def full_2_half(s):
	full_num = '０１２３４５６７８９'
	half_num = '0123456789'
	return s.translate(str.maketrans(full_num, half_num))

def format_phone_num(number):
	return number.replace("(", "").replace(")", "-")

class Maskdata(Resource):
    def get(self):
        try:
        	urlPath = "http://data.nhi.gov.tw/Datasets/Download.ashx?rid=A21030000I-D50001-001&l=https://data.nhi.gov.tw/resource/mask/maskdata.csv"
        	lines = fetchCsvData(urlPath)
        	lines = [line.strip() for line in lines]
        	keys = lines[0].split(',') 
        	line_num = 1
        	total_lines = len(lines)
        	datas = []
        	jsondata = []
        	jsonkeys = ["updatetime", "data"]
        	updatetime = ""
        	while line_num < total_lines:
        		values = lines[line_num].split(",")
        		if(updatetime == ""):
        			updatetime = values[-1]
        			jsondata.append(updatetime)
        		values = values[1:-1] #remove first and last element
        		values[2] = format_phone_num(values[2])
        		datas.append(values)
        		line_num = line_num + 1
        	jsondata.append(datas)
        	json_str = json.dumps(dict(zip(jsonkeys, jsondata)), ensure_ascii=False, indent=0)
        	#print(type(json_str))
        	result_data = json_str.replace('\\N','').replace('\n','')
        	print('size')
        	print(result_data)
        	print(sys.getsizeof(result_data))
        	return result_data
        except Exception as e:
        	return e

class Hello_world(Resource):
	def get(self):
		result = "HELLO!"
		return result
api.add_resource(Hello_world, '/')
api.add_resource(Maskdata, '/Maskdata') # Route_1

if __name__ == '__main__':
	print('app run')
	app.run()