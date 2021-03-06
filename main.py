# -*- coding: utf-8 -*-
import telebot
import const
import ym
import re
import requests
import advce
import random
import json
import sqlite3
import datetime
import threading
import botan


bot = telebot.TeleBot(const.token)
print("Road to the Dream!")

URL_FOR_CHANGE_CODE_TO_TOKEN_POST = "https://oauth.yandex.ru/token" #HTTP/1.1

###### КОМАНДЫ #####

@bot.message_handler(commands=['stats']) #Статистика с яндекс.метрики
def handler_command_stats(message):

    inlineMakup = telebot.types.InlineKeyboardMarkup()  # Создаём мень клавиатуры
    inleneButton_stats = telebot.types.InlineKeyboardButton(text="Сводка", callback_data="Сводка")
    inleneButton_poved = telebot.types.InlineKeyboardButton(text="Поведения клиентов", callback_data="Поведения клиентов")
    inleneButton_aydit = telebot.types.InlineKeyboardButton(text="Аудетория", callback_data="Аудетория")

    inlineMakup.add(inleneButton_stats)
    inlineMakup.add(inleneButton_poved)
    inlineMakup.add(inleneButton_aydit)


    bot.send_message(message.chat.id,"Выберете форму отчёта:", reply_markup=inlineMakup)

@bot.message_handler(commands=['setpush']) #Проверка на работоспособность сайта
def handler_command_setpush(message):
    bot.send_message(message.chat.id,text="Пожалуйста введите ваш URL. Пример: https://examples.com")

@bot.message_handler(commands=['ya']) #Подключение к яндекс сервисам
def handler_command_getMetrics(message):
    print()
    users_markup = telebot.types.ReplyKeyboardMarkup(True, True) #Создаём меню
    users_markup.row('Да! Давайте начнём!', 'Нет. Не сейчас.')
    bot.send_message(message.chat.id, "Добро пожаловать! Перед началом работы нужно подключиться к метрике! У вас есть минутка?", reply_markup=users_markup)

@bot.message_handler(commands=['track']) #Отслеживание посылок
def handler_command_track(message):
    try:
        if (len(message.text) > 6):
            track = message.text.split(" ")[1]
            get_track = requests.get(
                "https://track24.ru/api/tracking.json.php?apiKey=691b2560170aff61314873f02c8e3170&domain=oauth.yandex.ru/verification_code&code="+str(track))
            print(get_track.text)
            data_track = json.loads(get_track.text)
            text = ("Добавлен в базу:     "+ str(data_track['data']['trackCreationDateTime'])+
                  "\nПоследнее обновление:     "+ str(data_track['data']['trackUpdateDateTime'])+
                  "\nПрогназируюмая дата доставки:     " + str(data_track['data']['trackDeliveredDateTime'])+
                  "\nАдресс доставки:      "+str(data_track['data']['destinationAddress']) +
                  "\nОткуда отправлен:     "+str(data_track['data']['fromCountry'])+
                  "\nПоследнее событие:"+
                  "\nДата: "+str(data_track['data']['events'][0]['eventDateTime']) +
                  "\nСтатус: "+str(data_track['data']['events'][0]['operationType']))

            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "Извините, кажеться введён не вверный формат. Нужно /track ваш_номер_доставки.")
    except KeyError:
        bot.send_message(message.chat.id, "Трек номер не найден. Проверь и попробуйте ещё раз!")
    except:
        bot.send_message(message.chat.id,"Что-то не так! Наши программисты у же бегут исправлять ошибку!")

@bot.message_handler(commands=['postoffice']) #Аналиика почтовой рассылки
def handler_command_postoffice(message):
    try:
        if(len(message.text) > 11):

            conn = sqlite3.connect('D:/users.sqlite')
            cur = conn.cursor()
            cur.execute("SELECT id_metric, token FROM users WHERE id_users = " + str(message.chat.id))
            row = cur.fetchone()

            print(str(row[1]))

            get_post = requests.get("https://postoffice.yandex.ru/api/1.0/stat-list?oauth_token="+row[1]+"&email="+message.text.split(" ")[1])
            print(get_post.text)
            data_post = json.loads(get_post.text)
            bot.send_message(message.chat.id, "Общее кол-во сообщений "+ str(data_post['list']['messages'])
                             +"\nКол-во прочитанных сообщений получателями "+ str(data_post['list']['read'])
                             +"\nКол-во не прочитанных сообщений получателями "+str(data_post['list']['not_read'])
                             +"\nКол-во сообщений помеченные как спам " + str(data_post['list']['spam']))
        else:
            bot.send_message(message.chat.id, "Извините, кажеться введён не правельный формат. Попробуйте ещё раз.")

    except KeyError:
        bot.send_message(message.chat.id, "Данных нет.")
    except TypeError as err:
        bot.send_message(message.chat.id,"Что-то не так! Наши программисты у же бегут исправлять ошибку! " + str(err))

@bot.message_handler(commands=['advice']) #Полезный совет
def handler_command_advice(message):
    bot.send_message(message.chat.id, advce.advices.setdefault(random.randint(2, 23)))

@bot.message_handler(commands=['help']) #Помощь
def handler_command_help(message):
    bot.send_message(message.chat.id, "Привет! Я TwiggBot. "
                                      "Я создан, что бы помогать владельцам инетернет-магазинов управлять и следить за "
                                      "их интернет-магазином. Я пока на стадии разработки, но кое-что уже умею."
                                      "\n /help - Помощь."
                                      "\n /ya - Доступ к сервисам яндекса. ( Нужно для /stats и /info.)"
                                      "\n /stats - Получение статистики."
                                      "\n /track <трек номер> - отслеживание посылок."
                                      "\n /postoffice <e-mail> - получеие статистики рассылки."
                                      "\n /setpush - Проверка сайта."
                                      "\n /info <сайт> - СКОРО!"
                                      "\n /delivery CКОРО!"
                                      "\n /managerDirect - СКОРО!"
                                      "\nЕсли есть какие - то пожелания, вопросы или жалобы обращайтесь к моему создателю @marat_sher!")
    botan.track(const.botan_token,message.chat.id,message,"Команда /help")

@bot.message_handler(commands=['start'] ) #Старт
def handler_command_start(message):
    bot.send_message(message.chat.id, "Привет! Я TwiggBot. "
                                      "Я создан, что бы помогать владельцам инетернет-магазинов управлять и следить за "
                                      "их интернет-магазином. Я пока на стадии разработки, но кое-что уже умею."
                                      "\n /help - Помощь."
                                      "\n /ya - Доступ к сервисам яндекса. ( Нужно для /stats и /info.)"
                                      "\n /stats - Получение статистики."
                                      "\n /track <трек номер> - отслеживание посылок."
                                      "\n /postoffice <e-mail> - получеие статистики рассылки."
                                      "\n /setpush - Проверка сайта."
                                      "\n /info <сайт> - СКОРО!"
                                      "\n /delivery CКОРО!"
                                      "\n /managerDirect - СКОРО!"
                                      "\nЕсли есть какие - то пожелания, вопросы или жалобы обращайтесь к моему создателю @marat_sher!")

@bot.message_handler(commands=['delivery']) #Работа с яндекс.доставкой
def handler_command_delivery(message):
    bot.send_message(message.chat.id,"Это функция пока в разработке. Мы усердно работаем над её реализацией!")

@bot.message_handler(commands=['manager_direct']) #Управление директом
def handler_command_manager_direct(message):
    bot.send_message(message.chat.id, "Это функция пока в разработке. Мы усердно работаем над её реализацией!")

@bot.message_handler(commands=['info']) #Информация о сайте с веб-мастера
def handler_command_info(message):
    bot.send_message(message.chat.id, "Функция в дороботке. Скоро она будет готова!")

##### ТЕКСТ #####

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    global row

    conn = sqlite3.connect('D:/users.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT id_metric, token FROM users WHERE id_users = " + str(call.message.chat.id))
    row = cur.fetchone()
    try:


        if call.data == "Сводка":
            inlineMakup = telebot.types.InlineKeyboardMarkup()  # Создаём мень клавиатуры
            inleneButton_day = telebot.types.InlineKeyboardButton(text="День", callback_data="Сводка_День")
            inleneButton_week = telebot.types.InlineKeyboardButton(text="Неделя",callback_data="Сводка_Неделя")
            inleneButton_month = telebot.types.InlineKeyboardButton(text="Месяц", callback_data="Сводка_Месяц")
            inleneButton_qouter = telebot.types.InlineKeyboardButton(text="Квартал", callback_data="Сводка_Квартал")
            inleneButton_year = telebot.types.InlineKeyboardButton(text="Год", callback_data="Сводка_Год")

            inlineMakup.add(inleneButton_day)
            inlineMakup.add(inleneButton_week)
            inlineMakup.add(inleneButton_month)
            inlineMakup.add(inleneButton_qouter)
            inlineMakup.add(inleneButton_year)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберете иннтервал:", reply_markup=inlineMakup)

        if call.data == "Поведения клиентов":
            r_get_poved = requests.get(ym.general_url + ym.time + ym.ids + str(row[0]) + "&" + ym.metric + ym.upToDayUserRecencyPercentage + "," + ym.upToWeekUserRecencyPercentage + "," + ym.upToMonthUserRecencyPercentage + "&" + ym.oauth_token + row[1])
            data_poved = json.loads(r_get_poved.text)["totals"]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вернувшийся через 1 день - "+ str(data_poved[0][0])
                                  +"\nВернувшийся через 1 неделю - "+str(data_poved[0][1])
                                  +"\nВернувшийся через 1 месяц - "+str(data_poved[0][2]))

        if call.data == "Аудетория":
            r_get_aydit = requests.get(ym.general_url + ym.time + ym.ids + str(row[0]) + "&" + ym.metric + ym.metric_manPercentage + "," + ym.metric_womanPercentage + "," + ym.under18AgePercentage + "," + ym.upTo24AgePercentage + "," + ym.upTo34AgePercentage + "," + ym.upTo44AgePercentage + "," + ym.over44AgePercentage + "&" + ym.oauth_token + row[1])
            data_aydit = json.loads(r_get_aydit.text)["totals"]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Доля мужчин - "+str(data_aydit[0][0])
                                  +"\nДоля женщин - "+str(data_aydit[0][1])
                                  +"\nВозраст до 18 лет - " + str(data_aydit[0][2])
                                  +"\nВозраст с 18 до 24 лет - "+str(data_aydit[0][3])
                                  +"\nВозраст с 24 до 35 лет - "+str(data_aydit[0][4])
                                  +"\nВозраст с 34 до 44 лет - "+str(data_aydit[0][5])
                                  +"\nВозраст более 45 лет - "+ str(data_aydit[0][6]))



        if(call.data == "Сводка_День"):
            r_get_svodka_day = requests.get(ym.general_url + ym.time + ym.ids + str(row[0]) + "&" + ym.preset + ym.traffic + "&" + ym.date1 + "yesterday" + "&" + ym.date2 + "today" + "&" + ym.oauth_token + row[1])
            data_day = json.loads(r_get_svodka_day.text)["totals"]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Визиты - " + str(data_day[0]) + "\nПоситители - " + str(
                                      data_day[1]) + "\nПросмотры - " + str(data_day[2]) + "\nПроцент новых пользователей - " + str(
                                      data_day[3]) + "\nОтказы - " + str(
                                      data_day[4]) + "\nГлубина просмотра - " + str(data_day[5]) + "\nСредняя длительность посещения в секундах - "
                                      + str(data_day[6]))
        if (call.data == "Сводка_Неделя"):
            r_get_svodka_week = requests.get(ym.general_url + ym.time + ym.ids + str(row[0]) + "&" + ym.preset + ym.traffic + "&" + ym.date1 + "7daysAgo" + "&" + ym.date2 + "today" + "&" + ym.oauth_token + row[1])
            data_week = json.loads(r_get_svodka_week.text)["totals"]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Визиты - " + str(data_week[0][0]) + "\nПоситители - " + str(
                                      data_week[1][0]) + "\nПросмотры - " + str(data_week[2][0]) + "\nПроцент новых пользователей - " + str(
                                      data_week[3][0]) + "\nОтказы - " + str(
                                      data_week[4][0]) + "\nГлубина просмотра - "  + str(data_week[5][0]) + "\nСредняя длительность посещения в секундах - "+ str(
                                      data_week[6][0])
                                  )
        if (call.data == "Сводка_Месяц"):
            r_get_svodka_month = requests.get(ym.general_url + ym.time + ym.ids + str(row[0]) + "&" + ym.preset + ym.traffic + "&" + ym.date1 + "7daysAgo" + "&" + ym.date2 + "today" + "&" + ym.oauth_token + row[1])
            data_month = json.loads(r_get_svodka_month.text)["totals"]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Визиты - " + str(data_month[0][0]) + "\nПоситители - " + str(
                                      data_month[1][0]) + "\nПросмотры - " + str(data_month[2][0]) + "\nПроцент новых пользователей - " + str(
                                      data_month[3][0]) + "\nОтказы - " + str(
                                      data_month[4][0]) + "\nГлубина просмотра - " + str(data_month[5][0]) + "\nСредняя длительность посещения в секундах - " + str(
                                      data_month[6][0])
                                  )
        if (call.data == "Сводка_Квартал"):
            r_get_svodka_qortal = requests.get(ym.general_url + ym.time + ym.ids + str(row[0]) + "&" + ym.preset + ym.traffic + "&" + ym.date1 + "90daysAgo" + "&" + ym.date2 + "today" + "&" + ym.oauth_token + row[1])
            data_qortal = json.loads(r_get_svodka_qortal.text)["totals"]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Визиты - " + str(data_qortal[0][0]) + "\nПоситители - " + str(
                                      data_qortal[1][0]) + "\nПросмотры - " + str(data_qortal[2][0]) + "\nПроцент новых пользователей - " + str(
                                      data_qortal[3][0]) + "\nОтказы -" + str(
                                      data_qortal[4][0]) + "\nГлубина просмотра -  " + str(
                                      data_qortal[5][0]) + "\nСредняя длительность посещения в секундах - " + str(
                                      data_qortal[6][0])
                                  )
        if (call.data == "Сводка_Год"):
            r_get_svodka_year = requests.get(ym.general_url + ym.time + ym.ids + str(row[0]) + "&" + ym.preset + ym.traffic + "&" + ym.date1 + "90daysAgo" + "&" + ym.date2 + "today" + "&" + ym.oauth_token + row[1])
            data_year = json.loads(r_get_svodka_year.text)["totals"]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Визиты - " + str(data_year[0][0]) + "\nПоситители - " + str(
                                      data_year[1][0]) + "\nПросмотры - " + str(data_year[2][0]) + "\nПроцент новых пользователей - " + str(
                                      data_year[3][0]) + "\nОтказы - " + str(
                                      data_year[4][0]) + "\nГлубина просмотра - " + str(
                                      data_year[5][0]) + "\nСредняя длительность посещения в секундах - " + str(
                                      data_year[6][0])
                                  )


    except TypeError:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="Похоже.. вы не получили доступ к метрике. Используйте команду /YA")
    except KeyError:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Что-то не так! Наши программисты у же бегут исправлять ошибку!")

@bot.message_handler(content_types=["text"])
def handler_messages_hello(message): # Название функции не играет никакой роли, в принципе

    global token #Переменная токен
    removeMakup = telebot.types.ReplyKeyboardRemove(True) #Убиратель клавиатуры

    try:

        if message.text == "Привет" :
            bot.send_message(message.chat.id, "Привет!")

        if message.text == "Да! Давайте начнём!": #Согласие на подкулючение к яндексу
            bot.send_message(message.chat.id,text="Хорошо! Поехали!",reply_markup=removeMakup)
            inlineMakup = telebot.types.InlineKeyboardMarkup() #Создаём мень клавиатуры
            inleneButton = telebot.types.InlineKeyboardButton(text="Подтвердить!", url=ym.url_For_Users_OAuth_Check) #Кнопка для перехода на сайт подтверждения

            inlineMakup.add(inleneButton) #Добовляем кнопку в клавиатуру

            bot.send_message(message.chat.id, "Прежде всего нужно дать согласие на сбор данных с яндекс.метрики и других сервисов.(Внимание! Ваши личные данные не обрабатываются. Не беспокойтесь). Перейдите по ссылке ниже для этого. После согласия вы получите код подтверждения. Пожалуйста, введите его.", reply_markup=inlineMakup)

        if message.text == "Нет. Не сейчас.":
            bot.send_message(message.chat.id, "Мы вас поняли!",reply_markup=removeMakup)

        if re.match(const.pattern_for_check_code, message.text): #Если введён код полтверждения
            #параметры и заголовки
            payload = ({"grant_type":"authorization_code","code" : message.text, "client_id":const.idApps_Yand,"client_secret":const.passApp_yand,"device_id": const.UUID, "device_name":const.divace_name})
            headers = {"Host": "oauth.yandex.ru","Content-type": "application/x-www-form-urlencoded", "Content-Length":"288"}

            #отправить post запрос
            r_post_token = requests.post(url=URL_FOR_CHANGE_CODE_TO_TOKEN_POST,data=payload,headers=headers) #пост запрос на получение токена
            data_post_token = json.loads(r_post_token.text)
            token = data_post_token['access_token'] #извлекаем токены

            bot.send_message(message.chat.id, "Почти готово! Теперь введите номер вашего счётчика.(Перед номером поставьте знак '|'. Пример: '|12345678')")

        if re.match(const.pattern_for_id_metrics, message.text): #Введ счёсчика
            conn = sqlite3.connect('D:/users.sqlite')
            counter = re.search("\d\d\d\d\d\d\d\d",message.text)
            conn.execute("INSERT INTO users (id_users,token,id_metric) VALUES ('%s','%s','%s')" % (message.chat.id, token, counter.group(0)))
            conn.commit()
            bot.send_message(message.chat.id,"Готово! Вы молодец! Теперь можете приступать к работе, используйте команду /stats")

        if message.text.find("https://") != -1: #введена ссылка
            get = requests.get(message.text)
            status = get.status_code;

            if status == 200:
                bot.send_message(message.chat.id, "Отлично! Всё работает!")
            if status == 204:
                bot.send_message(message.chat.id, "Проблема. Нет содержимого(")
            if status == 404:
                bot.send_message(message.chat.id, "Ой! ресурс не найден(")
            if status == 410:
                bot.send_message(message.chat.id, "Проблема. Сайт удалён(")
            if status == 403:
                bot.send_message(message.chat.id, "Ошибка! Запрещено(")
            if status == 500:
                bot.send_message(message.chat.id, "Ошибка! Внутренняя ошибка сервера(")
    except Exception :
        bot.send_message(message.chat.id,"Что-то не так! Наши программисты у же бегут исправлять ошибку!")



try:
    bot.polling(none_stop=True)
except Exception:
    pass
