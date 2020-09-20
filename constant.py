#api_key = "08e5559b9b1105ccbc567378a810671d"
# 유승진 키 
api_key = "806ca36371f3e3d6658c552a76680c4f"
# 장종훈 키
#city name and id 
city_ids = {
	 "Farrukhabad": "1271942",
    "Noida": "7279746",
    "Delhi": "1261481",
    "Mumbai": "1275339",
    "Chennai": "1264527",
    "Guntur": "1270668",
    "Sunnyvale": "5400075",
    "Mountain View": "4122986",
    "New York": "5128638",
    "Seoul-teukbyeolsi":"1835847",
    "Busan":"1838524",
    "Daegu":"1835329"

}

#URLs
url_forecast_api = "http://api.openweathermap.org/data/2.5/forecast?appid=" + api_key + "&mode=json&units=metric&id="
url_weather_api = "http://api.openweathermap.org/data/2.5/weather?q=Seoul,kr&lang=kr&APPID=806ca36371f3e3d6658c552a76680c4f&mode=json&units=metric&id="
#url_weather_api = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&mode=json&units=metric&id="
