import tkinter

import time

window=tkinter.Tk()

window.geometry('400x250')
window.title("Timer")

def get_date():
    current=time.localtime()

    days=[
        'Понедельник',
        'Вторник',
        'Среда',
        'Четверг',
        'Пятница',
        'Суббота',
        'Воскресенье',
    ]
    
    months =[
        'января',
        'февраля',
        'марта',
        'апреля',
        'мая',
        'июня',
        'июля',
        'августа',
        'сентября',
        'октября',
        'ноября',
        'декабря',
    ]
    
    return f'{current.tm_mday} {months[current.tm_mon-1] }, {days[current.tm_wday]}'

def get_time():
    current=time.localtime()

    hour = current.tm_hour if current.tm_hour>=10 else '0'+str(current.tm_hour)
    minute = current.tm_min if current.tm_min>=10 else '0'+str(current.tm_min)
    
    return f'{hour}:{minute}'

date_info_label = tkinter.Label(text=get_date(), font='helvetica 20 bold')
date_info_label.pack()

time_label = tkinter.Label(text=get_time(), font='helevtica 100')
time_label.pack()


while True:
    date_info_label.config(text=str(get_date()))
    time_label.config(text=str(get_time()))
    date_info_label.update()
    time_label.update()
    
    
