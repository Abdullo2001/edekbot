from telebot import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from requests_oauthlib import OAuth1
from chiz import chizma
from datetime import date
import requests
import json
import emoji
import matplotlib.pyplot as plt


HEMIS_url = 'https://student.qarshidu.uz/rest/'

baza_url = 'https://api.e-dek.uz/api/'

bot=TeleBot("6002012435:AAG92Il_1hbsZ8OkUfFO402J0R8Xc2IVGXw")

rm = ReplyKeyboardRemove()

touches = InlineKeyboardMarkup()
touch1 = InlineKeyboardButton("Ariza", callback_data="A")
touch2 = InlineKeyboardButton("Tushuntirish xati", callback_data="TX")
touch3 = InlineKeyboardButton("Iltimosnoma", callback_data="I")
touch4 = InlineKeyboardButton("Murojaatnoma", callback_data="M")

touches.add(touch1)
touches.add(touch2)
touches.add(touch3)
touches.add(touch4)

knopkalar = ReplyKeyboardMarkup(resize_keyboard=True)
knopka1 = KeyboardButton("Murojaat yuborish")
knopka2 = KeyboardButton("Mening murojaatlarim")
knopka3 = KeyboardButton("Dars jadvali")
knopka4 = KeyboardButton("Kunlik dars jadvali")
knopka5 = KeyboardButton("O'qish joyidan ma'lumotnoma")

knopkalar.add(knopka1)
knopkalar.add(knopka2)
knopkalar.add(knopka3)
knopkalar.add(knopka4)
knopkalar.add(knopka5)


def vaqt_ajrat(vaqt):
    fullyear=str(vaqt.split("T")[0])
    clock=str(vaqt.split("T")[1])

    yil=fullyear.split("-")[0]
    oy=fullyear.split("-")[1]
    sana=fullyear.split("-")[2]
    soat=clock.split(":")[0]
    minut=clock.split(":")[1]
    sekund=float(clock.split(":")[2])
    sekund=round(sekund)
    vaqt_list=[sana,oy,yil,soat,minut,sekund]
    return vaqt_list

def yuqot(msg,id):
    bot.delete_message(msg.chat.id,id)

def och(msg):
    f = open(f"{msg.chat.id}.json", "r")
    x = f.read()
    f.close()
    return x

def yop(msg,z):
    f = open(f"{msg.chat.id}.json", "w")
    f.write(str(z))
    f.close()

def xatolik(msg):
    bot.send_message(msg.chat.id,"Qaytadan urinib ko'ring")

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_photo(msg.chat.id,open("start.png","rb"), caption="Qarshi davlat universitetining\nElektron dekanat botiga\nXush kelibsiz")
    a = bot.send_message(msg.chat.id, "Hemis loginingizni yuboring")
    bot.register_next_step_handler(a, parol)


def login(msg):
    a = bot.send_message(msg.chat.id, "Hemis loginingizni yuboring",reply_markup=rm)
    bot.register_next_step_handler(a, parol)


def parol(msg):
    if str(msg.text) == "/start":
        bot.send_message(msg.chat.id, f"loginni noto'g'ri kiritdingiz")
        login(msg)
    f = open(f"{msg.chat.id}.json", "w")
    f.write('''{
    "id": "",
    "login": "",
    "parol": "",
    "token": "",
    "ism": "",
    "familya": "",
    "murojaat_turi": ""
    }''')
    f.close()
    a = str(msg.text)
    x = och(msg)
    y = json.loads(x)
    y["login"] = a
    z = json.dumps(y)
    yop(msg,z)
    a = bot.send_message(msg.chat.id, "Hemis parolingizni yuboring")
    bot.register_next_step_handler(a, tekshirish)


def tekshirish(msg):
    x = och(msg)

    y = json.loads(x)
    login = y["login"]
    parol = str(msg.text)

    url = HEMIS_url+"v1/auth/login"
    data = {"login": login, "password": parol}
    header = {'content-type': 'application/json; charset=UTF-8'}

    response = requests.post(url, data=json.dumps(data), headers=header, verify=False)
    res = response.json()

    if response.ok:
        y["token"] = res["data"]["token"]
        y["parol"] = parol
        z = json.dumps(y)
        yop(msg,z)

        url = HEMIS_url+"v1/account/me"
        headers = {"Content-Type": "application/json",
                   "Authorization": 'Bearer '+str(y['token'])}
        response = requests.get(url, headers=headers, verify=False)

        if response.ok:
            res = response.json()
            chat_id=msg.message_id
            yuqot(msg,chat_id-3)
            yuqot(msg,chat_id-2)
            yuqot(msg,chat_id-1)
            yuqot(msg,chat_id)
            bot.send_message(msg.chat.id, f"Salom {res['data']['first_name']} {res['data']['second_name']}\n Qashi Davlat universitetining \nElektron dekanat botiga xush kelibsiz\nBotimiz orqali Universitet ma'muriyatiga murojaat yo'llashingiz mumkin.", reply_markup=knopkalar)

            data = {"ism": str(res['data']['first_name']), "familiya": str(res['data']['second_name']), "sharif": str(res["data"]['third_name']), "hemisId": str(res['data']["student_id_number"]), "yonalish": str(res['data']["specialty"]["name"]), "talimShakl": str(res['data']["educationForm"]['name']), "talimTur": str(res["data"]["educationType"]["name"]), "guruh": str(res["data"]["group"]["name"]), "fakultet": str(res["data"]["faculty"]["name"]), "bosqich": str(res["data"]["level"]["name"]), "manzil": str(res["data"]["district"]["name"])}
            url = baza_url+'talaba'
            header = {"Content-Type": "application/json"}
            response = requests.post(url, data=json.dumps(data), headers=header, verify=False)

        if response.ok:
            res = response.json()

            x=och(msg)
            y = json.loads(x)
            y["id"] = res["id"]
            z = json.dumps(y)
            yop(msg,z)

        else:
            bot.send_message(msg.chat.id, f"{response.text} Bazadan javob ola olmadik.\n Birozdan so'ng urinib ko'ring")
            login(msg)
    else:
        bot.send_message(msg.chat.id, "login yoki parol xato")
        login(msg)


@bot.message_handler(content_types=['text'])
def saralash(msg):
    if str(msg.text) == "Murojaat yuborish":
        bot.send_message(msg.chat.id, "Murojaat turini tanlang: ", reply_markup=touches)
    elif str(msg.text) == "Mening murojaatlarim":
        murojaatlarim(msg)
    elif str(msg.text)=="Dars jadvali":
        dars_jadvali(msg)
    elif str(msg.text)=="Kunlik dars jadvali":
        kunlik_dars_jadvali(msg)
    elif str(msg.text)=="O'qish joyidan ma'lumotnoma":
        malumotnoma(msg)
    else:
        bot.send_message(msg.chat.id, "Noma'lum buyruq yuborildi.")


def murojaatlarim(msg):
    url = baza_url+'murojaat'
    header = {"Content-Type": "application/json"}
    response = requests.get(url, headers=header)
    if response.ok:
        x=och(msg)
        y = json.loads(x)
        student_id = y["id"]
        res = response.json()
        javob = ""
        for i in res["content"]:
            if i["talaba"]["id"] == student_id:
                time=vaqt_ajrat(i["created"])
                soatemoji=emoji.emojize(":stopwatch:",language='alias')
                if i["holat"]=="ORGANILMOQDA":
                    javob += f"\n{soatemoji}  {time[0]}.{time[1]}.{time[2]}    {time[3]}:{time[4]}:{time[5]}\n\nMurojaat turi: {i['mavzu']}\nHolati: {i['holat']}\n\n----------------------------------\n"
                else:
                    javob += f"\n{soatemoji}  {time[0]}.{time[1]}.{time[2]}    {time[3]}:{time[4]}:{time[5]}\n\nMurojaat turi: {i['mavzu']}\nHolati: {i['holat']}\nXulosa: {i['xulosa']}\n\n----------------------------------\n"
        if javob == "":
            bot.send_message(msg.chat.id, "Siz hali murojaat qilmagansiz.")
        else:
            bot.send_message(msg.chat.id, f"{javob}")
    elif response["error"]=="Your request was made with invalid or expired JSON Web Token.":
       a= bot.send_message(msg.chat.id, f"Bot qayta ro'yhatdan o'ting")
       bot.register_next_step_handler(a,login)
    else:
        bot.send_message(msg.chat.id, "Ma'lumotlarni yuklashda xatolik yuz berdi.", reply_markup=knopkalar)

def dars_jadvali(msg):
    x=och(msg)
    y=json.loads(x)
    url = HEMIS_url+"v1/education/schedule"
    headers = {"Content-Type": "application/json",
                "Authorization": 'Bearer '+str(y['token'])}
    response = requests.get(url, headers=headers, verify=False)
    res = response.json()
    if response.ok:
        du=[[],[],[]]
        se=[[],[],[]]
        chor=[[],[],[]]
        pay=[[],[],[]]
        ju=[[],[],[]]
        sh=[[],[],[]]
        jadval=""
        for i in res["data"]:
            haftaboshi=i["weekStartTime"]
            date_time = datetime.fromtimestamp(haftaboshi) 
            d = date_time.strftime("%U")
            today=date.today()
            t = today.strftime("%U")
            if d==t:
                timestamp = i["lesson_date"] 
                date_time = datetime.fromtimestamp(timestamp)   
                if date_time.strftime("%A")=="Monday":
                    du[0].append(i["subject"]["name"])
                    du[1].append(i["trainingType"]["name"])
                    vaqti=i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]
                    du[2].append(vaqti)
                elif date_time.strftime("%A")=="Tuesday":
                    se[0].append(i["subject"]["name"])
                    se[1].append(i["trainingType"]["name"])
                    vaqti=i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]
                    se[2].append(vaqti)
                elif date_time.strftime("%A")=="Wednesday":
                    chor[0].append(i["subject"]["name"])
                    chor[1].append(i["trainingType"]["name"])
                    vaqti=i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]
                    chor[2].append(vaqti)
                elif date_time.strftime("%A")=="Thursday":
                    pay[0].append(i["subject"]["name"])
                    pay[1].append(i["trainingType"]["name"])
                    vaqti=i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]
                    pay[2].append(vaqti)
                elif date_time.strftime("%A")=="Friday":
                    ju[0].append(i["subject"]["name"])
                    ju[1].append(i["trainingType"]["name"])
                    vaqti=i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]
                    ju[2].append(vaqti)
                elif date_time.strftime("%A")=="Saturday":
                    sh[0].append(i["subject"]["name"])
                    sh[1].append(i["trainingType"]["name"])
                    vaqti=i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]
                    sh[2].append(vaqti)
        jadval_rasmi=[]
        qator=[]
        qator.append(["Fan nomi","Dars vaqti/xonasi",""])
        
        if len(du[0])!=0:
            qator.append(["","Dushanba",""])
            jadval+="Dushanba\n"
            for i in range(len(du[0])):
                l=[]
                l.append(i+1)
                l.append(du[0][i]+f"({du[1][i]})")
                l.append(du[2][i])
                qator.append(l)
                jadval+=f"{i+1}.{du[0][i]} ({du[1][i]})  {du[2][i]}\n\n"
        
        if len(se[0])!=0:
            qator.append(["","Seshanba",""])
            jadval+="Seshanba\n"
            for i in range(len(se[0])):
                l=[]
                l.append(i+1)
                l.append(se[0][i]+f"({se[1][i]})")
                l.append(se[2][i])
                qator.append(l)
                jadval+=f"{i+1}.{se[0][i]} ({se[1][i]})  {se[2][i]}\n\n"
        
        if len(chor[0])!=0:
            qator.append(["","Chorshanba",""])
            jadval+="Chorshanba\n"
            for i in range(len(chor[0])):
                l=[]
                l.append(i+1)
                l.append(chor[0][i]+f"({chor[1][i]})")
                l.append(chor[2][i])
                qator.append(l)
                jadval+=f"{i+1}.{chor[0][i]} ({chor[1][i]})  {chor[2][i]}\n\n"
        
        if len(pay[0])!=0:
            qator.append(["","Payshanba",""])
            jadval+="Payshanba\n"
            for i in range(len(pay[0])):
                l=[]
                l.append(i+1)
                l.append(pay[0][i]+f"({pay[1][i]})")
                l.append(pay[2][i])
                qator.append(l)
                jadval+=f"{i+1}.{pay[0][i]} ({pay[1][i]})  {pay[2][i]}\n\n"
        
        if len(ju[0])!=0:
            qator.append(["","Juma",""])
            jadval+="Juma\n"
            for i in range(len(ju[0])):
                l=[]
                l.append(i+1)
                l.append(ju[0][i]+f"({ju[1][i]})")
                l.append(ju[2][i])
                qator.append(l)
                jadval+=f"{i+1}.{ju[0][i]} ({ju[1][i]})  {ju[2][i]}\n\n"
    
        if len(sh[0])!=0:
            qator.append(["","Shanba",""])
            jadval+="Shanba\n"
            for i in range(len(sh[0])):
                l=[]
                l.append(i+1)
                l.append(sh[0][i]+f"({sh[1][i]})")
                l.append(sh[2][i])
                qator.append(l)
                jadval+=f"{i+1}.{sh[0][i]} ({sh[1][i]})  {sh[2][i]}\n\n"
        chizma(msg,qator,"Haftalik dars jadvali")
        bot.send_photo(msg.chat.id,open(f'{msg.chat.id}.png','rb'),caption=f"{jadval}")
    elif res["error"]=="Your request was made with invalid or expired JSON Web Token.":
       bot.send_message(msg.chat.id, f"Bot qayta ro'yhatdan o'ting")
       login(msg)
    else:
        bot.send_message(msg.chat.id,"Xatolik yuz berdi qayta urinib ko'ring")

def kunlik_dars_jadvali(msg):
    x=och(msg)
    y=json.loads(x)
    url = HEMIS_url+"v1/education/schedule"
    headers = {"Content-Type": "application/json",
                "Authorization": 'Bearer '+str(y['token'])}
    response = requests.get(url, headers=headers, verify=False)
    if response.ok:
        res = response.json()
        today = date.today()
        satr=[]
        tr=1
        l=["Fan nomi","Dars vati/xonasi",""]
        satr.append(l)
        print(satr)
        for i in res["data"]:
            timestamp = i["lesson_date"] 
            date_time = datetime.fromtimestamp(timestamp) 
            d = date_time.strftime("%Y-%m-%d")
            if str(d)==str(today):
                tur=i["trainingType"]["name"]
                l=[tr,i["subject"]["name"]+f"({tur})",i["lessonPair"]["start_time"]+"-"+i["lessonPair"]["end_time"]+" "+i["auditorium"]["name"]]
                satr.append(l)
                tr=tr+1
        if tr==1:
            bot.send_message(msg.chat.id,f"{today}{d}Bugun dars yo'q")
        else:
            today=date.today()
            t = today.strftime("%A")
            haftakuni=""
            if t=="Monday":
                haftakuni="Dushanba"
            elif t=="Tuesday":
                haftakuni="Seshanba"
            elif t=="Wednesday":
                haftakuni="Chorshanba"
            elif t=="Thursday":
                haftakuni="Payshanba"
            elif t=="Friday":
                haftakuni="Juma"
            elif t=="Saturday":
                haftakuni="Shanba"

            chizma(msg,satr,f"{haftakuni}")
            bot.send_photo(msg.chat.id,open(f'{msg.chat.id}.png','rb'))
    elif res["error"]=="Your request was made with invalid or expired JSON Web Token.":
       bot.send_message(msg.chat.id, f"Bot qayta ro'yhatdan o'ting")
       login(msg)
    else:
        bot.send_message(msg.chat.id,"Xatolik yuz berdi qayta urinib ko'ring")

def malumotnoma(msg):
    x=och(msg)
    y=json.loads(x)
    token=str(y["token"])
    url = HEMIS_url+"v1/student/reference"
    headers = {"Content-Type": "application/json",
                "Authorization": 'Bearer '+token}
    response = requests.get(url, headers=headers, verify=False)
    if response.ok:
        res=response.json()
        url=res["data"][0]["file"]
        headers = {"Content-Type": "application/json",
                    "Authorization": 'Bearer '+token}
        response = requests.get(url, headers=headers, verify=False)
        
        if response.ok:
            with open(f"malumotnoma{msg.chat.id}.pdf", 'wb') as f:
                f.write(response.content)
                f.close()
            bot.send_document(msg.chat.id,open(f"malumotnoma{msg.chat.id}.pdf",'rb'))
        else:
            xatolik(msg)
    elif res["error"]=="Your request was made with invalid or expired JSON Web Token.":
       bot.send_message(msg.chat.id, f"Bot qayta ro'yhatdan o'ting")
       login(msg)
    else:
        bot.send_message(msg.chat.id,"Xatolik yuz berdi qayta urinib ko'ring")



@bot.callback_query_handler(func=lambda call: True)
def surov(call):
    f = open(f"{call.message.chat.id}.json", "r")
    x = f.read()
    f.close()
    y = json.loads(x)
    
    if call.data == "A":
        y["murojaat_turi"]="Ariza"
        
    elif call.data == "TX":
        y["murojaat_turi"]="Tushuntirish xati"
    elif call.data == "I":
        y["murojaat_turi"]="Iltimosnoma"
    elif call.data == "M":
        y["murojaat_turi"]="Murojaatnoma"
    z = json.dumps(y)
    yop(call.message,z)
    yuqot(call.message,call.message.message_id-1)
    yuqot(call.message,call.message.message_id)
    a=bot.send_message(call.message.chat.id,"Murojaat matnini yuboring",reply_markup=rm)
    bot.register_next_step_handler(a,murojaat_yuborish)

def qayta_surov(msg):
    a=bot.send_message(msg.chat.id,"Murojaat matnini yuboring",reply_markup=rm)
    bot.register_next_step_handler(a,murojaat_yuborish)

def murojaat_yuborish(msg):
    yuqot(msg,msg.message_id-1)
    yuqot(msg,msg.message_id)
    firstsign=str(msg.text)
    firstsign=firstsign[0]
    if firstsign=="/":
        a=bot.send_message("Noto'g'ri matn kiritildi.\n Qayta kiriting")
        bot.register_next_step_handler(a,qayta_surov)
    x=och(msg)
    y = json.loads(x)
    data = {"talaba":{"id":y["id"]},"oqituvchi":{"id":1},"mavzu":y["murojaat_turi"],"matn": str(msg.text), "fayl":"","spravka":"", "holat":"ORGANILMOQDA","xulosa":""}
    url = baza_url+'murojaat'
    header = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=header, verify=False)
    if response.ok:
        ptichka=emoji.emojize(":check_mark_button:",language='alias')
        bot.send_message(msg.chat.id,f"{ptichka}Murojaat yuborildi",reply_markup=knopkalar)
    else:
        bot.send_message(msg.chat.id, "Bazadan javob ola olmadik.\n Birozdan so'ng urinib ko'ring")



bot.infinity_polling()
