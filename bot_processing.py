import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
from time import sleep
import os

load_dotenv()

 
TOKEN = os.getenv(token)
bot = telebot.TeleBot(TOKEN)
headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}


def get_sample_from_file(): 

    global main_list
    with open('Bots/First_Bot/main.txt') as f:
        main_list = [i.strip('\n') for i in f.read().split(',')]
    

def get_data_by_BeautifulSoup():
    
    global all_page_id, all_links, all_headers, all_price, all_img, all_date, area_of_flat_list, amount_of_rooms_list, floor_type_list, actual_list, main_list
    all_page_id, all_links, all_headers, all_price, all_img, all_date = [], [], [], [], [], []
    area_of_flat_list, amount_of_rooms_list, floor_type_list, actual_list = [], [], [], []
     
    page = 1

    while True:
        tmp = requests.get(f'https://www.halooglasi.com/nekretnine/izdavanje-stanova/beograd?cena_d_from=400&cena_d_to=800&cena_d_unit=4&oglasivac_nekretnine_id_l=387237&page={page}',
        headers=headers)
        page += 1
        soup = BeautifulSoup(tmp.text, 'lxml')
        page_kit = soup.find_all(class_='col-md-12 col-sm-12 col-xs-12 col-lg-12')

        if page_kit == []:
            break
     
        get_data_from_each_ad(page_kit)


def get_data_from_each_ad(page_kit):
    
    global all_page_id, all_links, all_headers, all_price, all_img, all_date, area_of_flat_list, amount_of_rooms_list, floor_type_list, actual_list

    for i in page_kit:
        
        id = i.find_next('div').find_next('div').get('id')
        actual_list.append(id)

        if id in main_list:
            continue
        else:
            all_page_id.append(id)
            all_links.append(f"https://www.halooglasi.com/{i.find('a').get('href')}")
            all_headers.append(i.find('h3').find('a').text)
            price = all_price.append(i.find(class_='central-feature-wrapper').find('span').get('data-value'))
            img = i.find('img').get('src')

            if img == '/Content/Quiddita/Widgets/Product/Stylesheets/img/no-image.jpg':
                img = 'https://www.halooglasi.com/Content/Quiddita/Widgets/Product/Stylesheets/img/no-image.jpg'
            
            all_img.append(img)
            date = all_date.append(i.find(class_='publish-date').text.strip('.'))
        
            features = i.find(class_='product-features').find_all('li')
            AMOUNT_OF_FEATURES = 3
            for e in range(AMOUNT_OF_FEATURES):

                try:
                    if e == 0:
                        area_of_flat_list.append(features[e].find(class_='value-wrapper').text.replace('\xa0m2Kvadratura', ' m2'))
                    if e == 1:
                        amount_of_rooms_list.append(features[e].find(class_='value-wrapper').text.replace('\xa0', ' '))
                    if e == 2:
                        floor_type_list.append(features[e].find(class_='value-wrapper').text.replace('\xa0', ' '))
                except:
                    floor_type_list.append('no information')
                    break
    
def send_message_to_telegram():   

    for q in range(len(all_page_id)):

        bot.send_message('-678301043', f"*{all_headers[q]}*,      {all_date[q]}" , parse_mode='Markdown') 
        markup = types.InlineKeyboardMarkup(row_width=1)
        item = types.InlineKeyboardButton(f'{all_price[q]}€, {area_of_flat_list[q]}, {amount_of_rooms_list[q]}, {floor_type_list[q]}', url=all_links[q])
        markup.add(item)
        try:
            bot.send_photo('-678301043', all_img[q], reply_markup=markup)
        except:
             bot.send_message('-678301043', 'no picture', reply_markup=markup)
             print('Нет картинки')
             continue
        sleep(9)

def correct_sample():

    global actual_list, main_list                                          
    main_list = actual_list          
    with open('Bots/First_Bot/main.txt', 'w') as file:
        print(*main_list, sep=',', file=file)


def main():

    get_sample_from_file()
    get_data_by_BeautifulSoup()
    send_message_to_telegram()            
    correct_sample()
    print(f'цикл выполнен ...{datetime.now().strftime("%H:%M")} ')

if __name__ == '__main__':
    schedule.every(2).minutes.do(main)
    while True:
        schedule.run_pending()
        