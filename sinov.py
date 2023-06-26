# from telebot import *
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
# import requests
# from requests_oauthlib import OAuth1
# import json
# import emoji

# HEMIS_url = 'https://student.qarshidu.uz/rest/'

# baza_url = 'https://api.e-dek.uz/api/'

# bot=TeleBot("1247570628:AAEERuhDzEINvLxaQaNkFEXCOMIbgbsgARA")

# def och(msg):
#     f = open(f"{msg.chat.id}.json", "r")
#     x = f.read()
#     f.close()
#     return x

# def yop(msg,z):
#     f = open(f"{msg.chat.id}.json", "w")
#     f.write(str(z))
#     f.close()

# def yuqot(msg,id):
#     bot.delete_message(msg.chat.id,id)


# @bot.message_handler(commands=['start'])
# def start(msg):
#     bot.send_photo(msg.chat.id,open("start.png","rb"), caption="Qarshi davlat universitetining\nElektron dekanat botiga\nXush kelibsiz")
#     a = bot.send_message(msg.chat.id, "Hemis loginingizni yuboring")
#     bot.register_next_step_handler(a, parol)


# def login(msg):
#     a = bot.send_message(msg.chat.id, "Hemis loginingizni yuboring")
#     bot.register_next_step_handler(a, parol)


# def parol(msg):
#     if str(msg.text) == "/start":
#         bot.send_message(msg.chat.id, f"loginni noto'g'ri kiritdingiz")
#         login(msg)
#     f = open(f"{msg.chat.id}.json", "w")
#     f.write('''{
#     "id": "",
#     "login": "",
#     "parol": "",
#     "token": "",
#     "ism": "",
#     "familya": "",
#     "murojaat_turi": ""
#     }''')
#     f.close()
#     a = str(msg.text)
#     x = och(msg)
#     y = json.loads(x)
#     y["login"] = a
#     z = json.dumps(y)
#     yop(msg,z)
#     a = bot.send_message(msg.chat.id, "Hemis parolingizni yuboring")
#     bot.register_next_step_handler(a, tekshirish)


# def tekshirish(msg):
#     x = och(msg)

#     y = json.loads(x)
#     login = y["login"]
#     parol = str(msg.text)

#     url = HEMIS_url+"v1/auth/login"
#     data = {"login": login, "password": parol}
#     header = {'content-type': 'application/json; charset=UTF-8'}

#     response = requests.post(url, data=json.dumps(data), headers=header, verify=False)
#     res = response.json()

#     if response.ok:
#         y["token"] = res["data"]["token"]
#         y["parol"] = parol
#         z = json.dumps(y)
#         yop(msg,z)

#         url = HEMIS_url+"v1/education/schedule"
#         headers = {"Content-Type": "application/json",
#                    "Authorization": 'Bearer '+str(y['token'])}
#         response = requests.get(url, headers=headers, verify=False)

#         if response.ok:
#             res = response.json()
#             chat_id=msg.message_id

#             for i in res["data"]:
#                 bot.send_message(msg.chat.id,f"{i}")
#             # bot.register_next_step_handler(a,surachi)
#         else:
#             bot.send_message(msg.chat.id, "login yoki parol xato")
#             login(msg)
#     else:
#         bot.send_message(msg.chat.id, "login yoki parol xato")
#         login(msg)

# @bot.message_handler(content_types=['text'])
# def surachi(msg):
#     x=och(msg)
#     y=json.loads(x)
#     url = HEMIS_url+"v1/education/schedule"
#     headers = {"Content-Type": "application/json",
#                 "Authorization": 'Bearer '+str(y['token'])}
#     response = requests.get(url, headers=headers, verify=False)
#     if response.ok:
#         res = response.json()
#         oxiri=len(res["data"])
#         haftaId=res["data"][oxiri-1]["_week"]-1
#         du=[[],[],[]]
#         se=[[],[],[]]
#         chor=[[],[],[]]
#         pay=[[],[],[]]
#         ju=[[],[],[]]
#         jadval=""
#         for i in res["data"]:
#             if i["_week"]==haftaId:
#                 if (i["lesson_date"]-i["weekStartTime"])/86400==0:
#                     du[0].append(i["subject"]["name"])
#                     du[1].append(i["trainingType"]["name"])
#                     vaqti=i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]
#                     du[2].append(vaqti)
#                 elif (i["lesson_date"]-i["weekStartTime"])/86400==1:
#                     se[0].append(i["subject"]["name"])
#                     se[1].append(i["trainingType"]["name"])
#                     vaqti=i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]
#                     se[2].append(vaqti)
#                 elif (i["lesson_date"]-i["weekStartTime"])/86400==2:
#                     chor[0].append(i["subject"]["name"])
#                     chor[1].append(i["trainingType"]["name"])
#                     vaqti=i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]
#                     chor[2].append(vaqti)
#                 elif (i["lesson_date"]-i["weekStartTime"])/86400==3:
#                     pay[0].append(i["subject"]["name"])
#                     pay[1].append(i["trainingType"]["name"])
#                     vaqti=i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]
#                     pay[2].append(vaqti)
#                 elif (i["lesson_date"]-i["weekStartTime"])/86400==4:
#                     ju[0].append(i["subject"]["name"])
#                     ju[1].append(i["trainingType"]["name"])
#                     vaqti=i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]
#                     ju[2].append(vaqti)
#         jadval+="Dushanba\n"
#         for i in range(len(du[0])):
#             jadval+=f"{i+1}.{du[0][i]} ({du[1][i]})  {du[2][i]}\n\n"
#         jadval+="Seshanba\n"
#         for i in range(len(se[0])):
#             jadval+=f"{i+1}.{se[0][i]} ({se[1][i]})  {se[2][i]}\n\n"
#         jadval+="Chorshanba\n"
#         for i in range(len(chor[0])):
#             jadval+=f"{i+1}.{chor[0][i]} ({chor[1][i]})  {chor[2][i]}\n\n"
#         jadval+="Payshanba\n"
#         for i in range(len(pay[0])):
#             jadval+=f"{i+1}.{pay[0][i]} ({pay[1][i]})  {pay[2][i]}\n\n"
#         jadval+="Juma\n"
#         for i in range(len(ju[0])):
#             jadval+=f"{i+1}.{ju[0][i]} ({ju[1][i]})  {ju[2][i]}\n\n"
#         bot.send_message(msg.chat.id,f"{jadval}")
#     else:
#         bot.send_message(msg.chat.id, "muammo")
# bot.infinity_polling()

from datetime import datetime,date
timestamp = 1685059200 
date_time = datetime.fromtimestamp(timestamp) 
# print("Date time object:", date_time) 
# d = date_time.strftime("%m/%d/%Y, %H:%M:%S") 
# print("Output 2:", d)  
# d = date_time.strftime("%d %b, %Y") 
# print("Output 3:", d) 
# d = date_time.strftime("%d %B, %Y") 
# print("Output 4:", d) 
# d = date_time.strftime("%I%p") 
# print("Output 5:", d)
# print(date.today())
today=date.today()
d=today.strftime("%A")
print(type(d))