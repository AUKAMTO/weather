import json
import boto3
import os

from urllib import request
from datetime import datetime, timedelta


yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y/%m/%d')
url = 'http://cowin.cse.cuhk.edu.hk/php/station_data.php?time=' + yesterday +'%20'

def formatHourSec(val):
    if val < 10:
        val = "0" + str(val)
        return val
    else:
        return val

def checkApiJosnNumNull(json_data,x,JsonVal,val):
    try:
        val = json_data[str(x)]['data'][JsonVal]['value']
        return val
    except:
        val = 0
        return val


def checkApiJosnTextNull(json_data,x,JsonVal,val):
    try:
        val = json_data[str(x)]['data'][JsonVal]['value']
        return val
    except:
        val = "null"
        return val

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table(os.environ["weatherDb"])
    for hour in range(12):
        hour = formatHourSec(hour)
        hUrl = url + str(hour)  + ':'
        for sec in range(60):
            sec = formatHourSec(sec)
            # qUrl ="http://cowin.cse.cuhk.edu.hk/php/station_data.php?time=2020/04/03%2003:32"
            qUrl = hUrl + str(sec)
            json_data = request.urlopen(qUrl).read().decode("utf-8")
            json_data = json.loads(json_data);
            schoolNum=(len(json_data)-1) #get school total number
            noSchoolNum = 0
            print(qUrl)
            for x in range(schoolNum):
                if 'N.T. Heung Yee Kuk Yuen Long District Secondary School' == json_data[str(x)]['station_name']:
                    airTemperature = 0.0
                    maximumAirTemperature = 0.0
                    minimumAirTemperature = 0.0
                    relativeHumidity = 0
                    windSpeed = 0.0
                    windDirection = "null"
                    past60MinutesRainfall = 0.0
                    uvIndex = 0.0
                    maximumUV = 0.0
                    solarRadiation = 0.0
                    seaLevelPressure = 0.0
                    pkey = str(yesterday) +" "+ str(hour) +":" + str(sec)
                    airTemperature = str(checkApiJosnNumNull(json_data,x,'Air Temperature',airTemperature))
                    maximumAirTemperature = str(checkApiJosnNumNull(json_data,x,'Maximum Air Temperature',maximumAirTemperature))
                    minimumAirTemperature = str(checkApiJosnNumNull(json_data,x,'Minimum Air Temperature',minimumAirTemperature))
                    relativeHumidity = str(checkApiJosnNumNull(json_data,x,'Relative Humidity',relativeHumidity))
                    windSpeed = str(checkApiJosnNumNull(json_data,x,'Wind Speed',windSpeed))
                    windDirection = str(checkApiJosnTextNull(json_data,x,'Wind Direction',windDirection))
                    past60MinutesRainfall = str(checkApiJosnNumNull(json_data,x,'Past 60-Minutes Rainfall',past60MinutesRainfall))
                    uvIndex = str(checkApiJosnNumNull(json_data,x,'UV Index',uvIndex))
                    maximumUV = str(checkApiJosnNumNull(json_data,x,'Maximum UV',maximumUV))
                    solarRadiation = str(checkApiJosnNumNull(json_data,x,'Solar Radiation',solarRadiation))
                    seaLevelPressure = str(checkApiJosnNumNull(json_data,x,'Sea-Level Pressure',seaLevelPressure))
                    # print("ss")
                    item = {
                            'daynum': pkey,'airTemperature':  (airTemperature),
                            'maximumAirTemperature':(maximumAirTemperature),'minimumAirTemperature':(minimumAirTemperature),
                            'relativeHumidity':(relativeHumidity),'windSpeed':(windSpeed),'windDirection':windDirection,
                            'past60MinutesRainfall':(past60MinutesRainfall),'uvIndex':(uvIndex),'maximumUV':(maximumUV),
                            'solarRadiation':(solarRadiation),'seaLevelPressure':(seaLevelPressure)}
                    table.put_item(Item=item)
                    # print("pkey" +str(pkey))
                    # print ("airTemperature1" + str(airTemperature))
                    # print("max " + str(maximumAirTemperature))
                    # print("min" + str(minimumAirTemperature))
                    # print("relativeHumidity " + str(relativeHumidity))
                    # print("windSpeed"+str(windSpeed))
                    # print("windDirection"+str(windDirection))
                    # print("past60MinutesRainfall"+ str(past60MinutesRainfall))
                    # print("uvIndex"+ str(uvIndex))
                    # print("maximumUV"+ str(maximumUV))
                    # print("solarRadiation"+str(solarRadiation))
                    # print("seaLevelPressure"+str(seaLevelPressure))
                else:
                    noSchoolNum = noSchoolNum + 1
                    if noSchoolNum == schoolNum:
                        noSchoolNum = 0
                        airTemperature = 0.0
                        maximumAirTemperature = 0.0
                        minimumAirTemperature = 0.0
                        relativeHumidity = 0
                        windSpeed = 0.0
                        windDirection = "null"
                        past60MinutesRainfall = 0.0
                        uvIndex = 0.0
                        maximumUV = 0.0
                        solarRadiation = 0.0
                        seaLevelPressure = 0.0
                        pkey = str(yesterday) +" "+ str(hour) +":" + str(sec)
                        airTemperature = str(airTemperature)
                        maximumAirTemperature = str(maximumAirTemperature)
                        minimumAirTemperature = str(minimumAirTemperature)
                        relativeHumidity = str(relativeHumidity)
                        windSpeed = str(windSpeed)
                        windDirection = str(windDirection)
                        past60MinutesRainfall = str(past60MinutesRainfall)
                        uvIndex = str(uvIndex)
                        maximumUV = str(maximumUV)
                        solarRadiation = str(solarRadiation)
                        seaLevelPressure = str(seaLevelPressure)
                        item = {
                                'daynum': pkey,'airTemperature':  (airTemperature),
                                'maximumAirTemperature':(maximumAirTemperature),'minimumAirTemperature':(minimumAirTemperature),
                                'relativeHumidity':(relativeHumidity),'windSpeed':(windSpeed),'windDirection':windDirection,
                                'past60MinutesRainfall':(past60MinutesRainfall),'uvIndex':(uvIndex),'maximumUV':(maximumUV),
                                'solarRadiation':(solarRadiation),'seaLevelPressure':(seaLevelPressure)}
                        table.put_item(Item=item)
                    # print("pkey" +str(pkey))
                    # print ("airTemperature2" + str(airTemperature))
                    # print("max " + str(maximumAirTemperature))
                    # print("min" + str(minimumAirTemperature))
                    # print("relativeHumidity " + str(relativeHumidity))
                    # print("windSpeed"+str(windSpeed))
                    # print("windDirection"+str(windDirection))
                    # print("past60MinutesRainfall"+ str(past60MinutesRainfall))
                    # print("uvIndex"+ str(uvIndex))
                    # print("maximumUV"+ str(maximumUV))
                    # print("solarRadiation"+str(solarRadiation))
                    # print("seaLevelPressure"+str(seaLevelPressure))

