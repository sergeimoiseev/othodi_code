# -*- coding: UTF-8 -*-
import urllib
# import nltk, urllib
# from bs4 import BeautifulSoup 
# импорт инструмента BeautifulSoup
import bs4
import sys # system
import os
import requests

def get_raw_text_from_url(url,start_marker = 'DATASTART',end_marker = 'DATAEND'):
    responce = requests.get(url) # получили много иформации
    # print(responce.headers['content-type']) # в том числе и информацию о кодировке, в которой скачана страница - можно посмотреть.
    soup = bs4.BeautifulSoup(responce.text, 'html.parser') # BeautifulSoup сам разбиратеся с кодировкой
    texts = soup.findAll(text=True) # возвращает весь текст со всех уровней html

    def visible(element): # выбрасываем все, что браузер бы не вывел на экран.
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False 
        return True

    f = open(os.devnull, 'w')
    temp = sys.stdout
    sys.stdout = f

    visible_texts = filter(visible, texts) # функция "filter()" по значению "visible" (True|False) включает или не включает текст ("texts") в возвращаемый список
    raw_text = u"" # инициализируем пустую строку, которая точно будет печататься в консоли
    for text in visible_texts:
        try:
            print(text)  # русский текст печатается, но что-то все равно не выводится в консоль. Вряд ли это что-то нам пригодится..
            raw_text = raw_text + '\n' + text # Если напечатать удалось, добавляем в итоговую строку
        except UnicodeError as e: # знаем, что будут проблемы с печатью "не той" кодировки.
            pass # игнорируем эти проблемы.
    sys.stdout = temp
    # cut_text = raw_text.split(start_marker)[1].split(end_marker)[0].strip()
    return(raw_text)

if __name__ == "__main__":
    url_1 = "https://www.dropbox.com/s/t9b9n2i03bz7ckk/cities.txt?dl=0"
    # url_1 = "http://google.ru"
    # url_1 = "http://www.cis.uni-muenchen.de/kurse/desi/sp/"
    raw_text = get_raw_text_from_url(url_1)
    out = open('cities_from_dropbox.txt', 'wb')
    out.write(raw_text)
    out.close()
    # print(raw_text)

    # sys.exit(0) # exit script