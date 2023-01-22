import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
from time import sleep
import os
load_dotenv()

 
token = os.getenv(token)
bot = telebot.TeleBot(token)
headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}



def get_data():

    with open('Bots/First_Bot/main.txt') as f:
        main_list = [i.strip('\n') for i in f.read().split(',')]
  
    
    all_page_id = []
    all_links = []
    all_headers = []
    all_price = []
    all_img = []
    all_date = []
    kit_f1 = []
    kit_f2 = []
    kit_f3 = []
    actual_list = []  

    for page in range(1,100):
        tmp = requests.get(f'https://www.halooglasi.com/nekretnine/izdavanje-stanova/beograd?cena_d_from=400&cena_d_to=800&cena_d_unit=4&oglasivac_nekretnine_id_l=387237&page={page}',
        headers=headers)

        soup = BeautifulSoup(tmp.text, 'lxml')
        page_kit = soup.find_all(class_='col-md-12 col-sm-12 col-xs-12 col-lg-12')

        if page_kit == []:
            break
     
        for i in page_kit:
            
            id = i.find_next('div').find_next('div').get('id')
            actual_list.append(id)
          
            if id in main_list:
                continue
            else:
                page_id = all_page_id.append(id)
                link = all_links.append('https://www.halooglasi.com' + i.find('a').get('href'))
                header = all_headers.append(i.find('h3').find('a').text)
                price = all_price.append(i.find(class_='central-feature-wrapper').find('span').get('data-value'))
                img = i.find('img').get('src')
                if img == '/Content/Quiddita/Widgets/Product/Stylesheets/img/no-image.jpg':
                    img = 'https://www.halooglasi.com/Content/Quiddita/Widgets/Product/Stylesheets/img/no-image.jpg'
                all_img.append(img)
                date = all_date.append(i.find(class_='publish-date').text.strip('.'))
            
                features = i.find(class_='product-features').find_all('li')
                for e in range(3):

                    try:
                        if e == 0:
                            kit_f1.append(features[e].find(class_='value-wrapper').text.replace('\xa0m2Kvadratura', ' m2'))
                        if e == 1:
                            kit_f2.append(features[e].find(class_='value-wrapper').text.replace('\xa0', ' '))
                        if e == 2:
                            kit_f3.append(features[e].find(class_='value-wrapper').text.replace('\xa0', ' '))
                    except:
                        kit_f3.append('no information')
                        break

    for q in range(len(all_page_id)):
        bot.send_message('-678301043', f"*{all_headers[q]}*,               {all_date[q]}" , parse_mode='Markdown') 
        markup = types.InlineKeyboardMarkup(row_width=1)
        item = types.InlineKeyboardButton(f'{all_price[q]}€, {kit_f1[q]}, {kit_f2[q]}, {kit_f3[q]}', url=all_links[q])
        markup.add(item)
        bot.send_photo('-678301043', all_img[q], reply_markup=markup)
        sleep(9)

                                                # Добавление новых объявлений
    main_list = actual_list                # Корректировка списка
    print(len(actual_list))
    print(len(main_list)) 
  
    with open('Bots/First_Bot/main.txt', 'w') as file:
        print(*main_list, sep=',', file=file)


def main(): pass
 
    # schedule.every(5).minutes.do(get_data)
    # while True:
    #     schedule.run_pending()

if __name__ == '__main__':
    get_data()
    main()