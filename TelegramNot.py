import telebot

TOKEN='6058694274:AAFEUpQQfVE4_Wsy_HQMGuQAJwFUhz-_RmM'
bot = telebot.TeleBot(TOKEN)
MY_LIST=('36','37','38','39','40','41','42','43','44','45','S','M','L','XL','XXL')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name} {message.from_user.last_name}|\n'
                                      f'Готовы сделать заказ?')
    bot.register_next_step_handler(message, answer)

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() in ['да','yes']:
        bot.send_message(message.chat.id,'Скиньте фотографию товара')
        bot.register_next_step_handler(message, photo)
    elif message.text.lower() in ['нет','no','not']:
        bot.send_message(message.chat.id,'Вы не готовы сделать заказ. \n'
                                         'Напишите да или yes, когда будете готовы сделать заказ!')
        bot.register_next_step_handler(message, answer)
    else:
        bot.send_message(message.chat.id, 'Напишите пожалуйста: да(yes) или нет(not, no)')
        bot.register_next_step_handler(message, answer)

def get_size(message):
    global size
    while message.text not in MY_LIST:
        bot.send_message(message.chat.id, 'Вы прислали не размер!')
    if message.text in MY_LIST:
        size = message.text
        bot.send_message(message.chat.id, 'Пришлите URL адрес:')
        bot.register_next_step_handler(message, get_URL)

def get_URL(message):
    global url
    text_url=message.text
    url='https://'+text_url.split('https://')[1].split()[0]
    bot.send_message(message.chat.id, url)

@bot.message_handler(content_types=['photo'])
def photo(message):
    raw = message.photo[2].file_id
    name = raw + ".jpg"
    print ('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f"{name}", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id,'Пришлите пожалуйста размер вещи')
    bot.register_next_step_handler(message, get_size)





bot.polling()
print(size)

