import json
import boto3
import os

from urllib import request
from datetime import datetime, timedelta


yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y/%m/%d')
url = 'http://cowin.cse.cuhk.edu.hk/php/station_data.php?time=' + yesterday +'%20'
schoolName = 'N.T. Heung Yee Kuk Yuen Long District Secondary School'

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
        formatHour = formatHourSec(hour)
        hUrl = url + str(formatHour)  + ':'
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
                if schoolName == json_data[str(x)]['station_name']  :
                    noSchoolNum = 0
                    daynum = 0
                    inputtime = 0
                    airTemperature = 0
                    maximumAirTemperature = 0
                    minimumAirTemperature = 0
                    relativeHumidity = 0
                    windSpeed = 0
                    windDirection = "null"
                    past60MinutesRainfall = 0
                    uvIndex = 0
                    maximumUV = 0
                    solarRadiation = 0
                    seaLevelPressure = 0
                    daynum =  str(yesterday)
                    inputtime =  str(hour)  + str(sec)
                    inputtime = int(inputtime)
                    inputtime = str(inputtime)
                    
                    if noSchoolNum != schoolNum:
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
                    
                    item = {
                            'daynum': daynum,'inputtime' : inputtime ,'airTemperature':  (airTemperature),
                            'maximumAirTemperature':(maximumAirTemperature),'minimumAirTemperature':(minimumAirTemperature),
                            'relativeHumidity':(relativeHumidity),'windSpeed':(windSpeed),'windDirection':windDirection,
                            'past60MinutesRainfall':(past60MinutesRainfall),'uvIndex':(uvIndex),'maximumUV':(maximumUV),
                            'solarRadiation':(solarRadiation),'seaLevelPressure':(seaLevelPressure)}
                    table.put_item(Item=item)
                else:
                    noSchoolNum = noSchoolNum + 1

