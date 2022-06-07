from datetime import datetime, timedelta 
import requests
# Moscow
lat = 55.755826 
lon = 37.617300
api_key = '409a30b2eb5891394ffbdd7ba40f6570' 
t = datetime.now()
min_avg_diff_temp = None 
min_avg_diff_temp_day = None 
max_daylight_duration = None 
max_daylight_duration_day = None 
for i in range(5):
    result_date = t - timedelta(days=i)
    timestamp = int(round(result_date.timestamp()))
    url = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={timestamp}&appid={api_key}&units=metric'
    a = requests.get(url)
    r = a.json()
# Ищем максимальный продолжительный световой день 
    sr = datetime.fromtimestamp(r['current']['sunrise'])
    ss = datetime.fromtimestamp(r['current']['sunset'])
    daylight_duration = ss - sr
    if max_daylight_duration is None or daylight_duration > max_daylight_duration:
        max_daylight_duration = daylight_duration 
        max_daylight_duration_day = result_date
# Ищем минимальную разницу температур 
diff_temps = []
for item in r['hourly']:
# Ночь
    if item['dt'] > r['current']['sunset'] or item['dt'] < r['current']['sunrise']:
        diff_temps.append(abs(item['temp'] - item['feels_like'])) 
    avg_diff_temp = sum(diff_temps) / len(diff_temps)
    if min_avg_diff_temp is None or min_avg_diff_temp > avg_diff_temp:
        min_avg_diff_temp = avg_diff_temp 
        min_avg_diff_temp_day = result_date
print(f'Минимальная разница: {round(min_avg_diff_temp, 2)}, {min_avg_diff_temp_day.date()}')
print(f'Максимальная продолжительность светового дня: {max_daylight_duration}, {max_daylight_duration_day.date()}')