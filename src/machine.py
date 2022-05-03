import pandas as pd
import glob
import tabula
import sqlite3
from src import buttons
from datetime import datetime, date, time
class Meta:
    def __init__(self):
        self.pdf_files = glob.glob('*.pdf')
        self.pdf_table = tabula.read_pdf(self.pdf_files[0],multiple_tables=True, pages='all')
        self.con = sqlite3.connect('register.db')
        self.cur = self.con.cursor()
        try:
            self.cur.execute('''CREATE TABLE stocks
               (member_id text, class text,  mention bool, register bool)''')
            self.con.commit()
        except:
            pass

    async def add_membersql(self,msg,member_id,grate,result):
        
        if len(result) == 0:
            self.cur.execute("INSERT INTO stocks VALUES (?,?,?,?)", (member_id, grate, True, True))
            self.con.commit()
            await msg.reply("Все прошло успешно",reply_markup=buttons.startMenu)
            
        else:
            if result[0][0] != 1:
                self.cur.execute("UPDATE stocks SET class = (?), register=1 WHERE register = 0 AND member_id=(?)", (grate,member_id))
                self.con.commit()
                await msg.reply("Готово",reply_markup=buttons.startMenu)

    async def state_machine(self,msg):
        member_id = msg.from_user.id
        self.cur.execute("SELECT register FROM stocks WHERE member_id = (?)",(member_id,))
        result = self.cur.fetchall()
        await self.add_membersql(msg,member_id, msg['text'], result)

        if result[0][0] == 1:
            print(msg['text'])
            if msg['text'] == "уроки на завтра":
                text = self.show_timetable(member_id,0)
                await msg.reply(text)

            if msg['text'] == "уроки на сегодня":
                text = self.show_timetable(member_id,1)
                await msg.reply(text)

            if msg['text'] == "⏳ Сколько осталось времени":
                text = self.left_time(member_id)
                await msg.reply(text)
            if msg['text'] == "ℹ️ Изменить класс":
                self.cur.execute("UPDATE stocks SET register=0 WHERE member_id=(?)", (member_id,))
                self.con.commit()
                await msg.reply("Сейчас напиши на какой класс хочешь поменять *8Г*")

    def left_time(self, member_id):
        page, grate =  self.number_grate(member_id)
        id_raw, reset=self.get_dayid(member_id,1)
        for i in range(id_raw-reset, id_raw-1):
            time1 = self.pdf_table[page].iloc[i,1].split('-')[0]
            time2 = self.pdf_table[page].iloc[i,1].split('-')[1]
            
            d1 = datetime.strptime(datetime.now().strftime("%H:%M:%S"),"%H:%M:%S")
            d2 = datetime.strptime(time1, "%H:%M")
            d3 = datetime.strptime(time2, "%H:%M")

            if(d1<d2):
                try:
                    return str(d2-d1) + " Осталось до конца перемены." + " Сейчас будет " + self.pdf_table[page].iloc[i,grate*2+2]
                except:
                    return "Уроки закончились"
            elif(d1<d3):
                try:
                    return str(d3-d1) + " Осталось до конца урока." + " Следуйщий будет "+ self.pdf_table[page].iloc[i+1,grate*2+2]
                except:
                    return "Уроки закончились"
        return "Уроки закончились"

    def number_grate(self,member_id):
        self.cur.execute("SELECT class FROM stocks WHERE member_id = (?)",(member_id,))
        result = self.cur.fetchall()
        grate = result[0][0][-1].lower() 
        number = result[0][0]
        if len(number)==2:
            number=int(number[0])-6
        else:
            number=int(int(number[0])*10+int(number[1]))-6
        if grate == 'а':
            grate = 0

        elif grate == 'б':
            grate = 1

        elif grate == 'в':
            grate = 2

        elif grate == 'г':
            grate = 3
        print(grate)
        return number,grate

    def get_dayid(self,member_id,today):
        day=datetime.today().isoweekday() - today 
        if day == 6:
            day = 0

        pdf_day = 0 
        reset=0
        id_raw =0
        page,grate =  self.number_grate(member_id) 
        while True:
            if reset > self.pdf_table[page].iloc[id_raw,0]:
                
                if pdf_day == day:
                    break
                pdf_day+=1
            reset = self.pdf_table[page].iloc[id_raw,0]
            id_raw+=1
        return id_raw,reset

    def show_timetable(self,member_id,today):
        id_raw,reset=self.get_dayid(member_id,today)
        
        page,grate =  self.number_grate(member_id) 
        
        text=''
        for i in range(int(id_raw-reset),id_raw):
            #if str(self.pdf_table[page].iloc[i,grate*2+2]) == 'nan':
            #    continue
            text=( text + str(self.pdf_table[page].iloc[i,1]) + ' - ' + str(self.pdf_table[page].iloc[i,grate*2+2]) +
             " " + str(self.pdf_table[page].iloc[i,grate*2+3]).split('.')[0] + '\n')
        return text
