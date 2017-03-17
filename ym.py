import requests


url_For_Users_OAuth_Check = "https://oauth.yandex.ru/authorize?response_type=code&client_id=2f347debb8df41a0b5d4cf65eacb03ca"
url_For_Chenge_code_to_token_POST = "POST /token HTTP/1.1Host:oauth.yandex.ruContent-type:application/x-www-form-urlencodedContent-Length:64 grant_type=authorization_code&code="
url_Get = "https://api-metrika.yandex.ru/stat/v1/data/drilldown?ids=40922334&metrics=ym:s:pageviews&date1=2016-11-1&date2=2017-1-1&dimensions=ym:s:operatingSystem&oauth_token=AQAAAAAXp8R_AAQSglHF-Xm7XUgBsmdTe-hFJss"

#TO DO
# сделать url_get гибким в этом классе

#############################Части URL GET########################################
# основа
general_url = "https://api-metrika.yandex.ru"
# Метрики
metric_visits = "ym:s:visits" # Визиты
metric_pageviews = "ym:s:pageviews" # Просмотры
metric_users = "ym:s:users" # Поситители

metric_bounceRate = "ym:s:bounceRate" #Отказы
metric_pageDepth = "ym:s:pageDepth" # Глубина просмотра
metric_avgVisitDurationSeconds = "ym:s:avgVisitDurationSeconds" # Время на сайте

metric_visitsPerDay = "ym:s:visitsPerDay" # визитов в день
metric_visitsPerHour = "ym:s:visitsPerHour" # Визитов в час
metric_visitsPerMinute = "ym:s:visitsPerMinute" # Визитов в минуту

metric_manPercentage = "ym:s:manPercentage" # Доля мужчин
metric_womanPercentage = "ym:s:womanPercentage" # Доля женщин
datePeriod = "ym:s:datePeriod"

under18AgePercentage = "ym:s:under18AgePercentage"
upTo24AgePercentage	 = "ym:s:upTo24AgePercentage"
upTo34AgePercentage  = "ym:s:upTo34AgePercentage"
upTo44AgePercentage = "ym:s:upTo44AgePercentage"
over44AgePercentage = "ym:s:over44AgePercentage"

upToDayUserRecencyPercentage = "ym:s:upToDayUserRecencyPercentage"
upToWeekUserRecencyPercentage = "ym:s:upToWeekUserRecencyPercentage"
upToMonthUserRecencyPercentage = "ym:s:upToMonthUserRecencyPercentage"

# Основные пораметры
direct_client_logins = "direct_client_logins="
metric = "metrics="
ids = "ids="
date1 = "date1="
date2 = "date2="
dimensions = "dimensions="
preset = "preset="
timezone = "timezone="
oauth_token = "oauth_token="

# Шаьлоны
sources_search_phrases = "sources_search_phrases"
sources_summary = "sources_summary"
tech_platforms = "tech_platforms"
traffic = "traffic"
geo_country = "geo_country"

# Форматы отчётов
tubl = "/stat/v1/data?" # Таблицы
drill_down = "/stat/v1/data/drilldown?" # Ветви
time = "/stat/v1/data/bytime?" # По времени

day = "day"
week = "week"
month = "month"
quarter = "quarter"
year = "Year"






