import telebot
from config import currencys, TOKEN
from extention import ConvertionException, CryptoConverter, get_picture

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def start_help(message):
    text = "Для начала работы введите команду в одну строку в следующей последовательности:\n\n" \
           "*<исходная валюта>* \ \n*<сумму для конвертации>* \ \n*<необходимая валюта>*\n" \
           "\n \nОзнакомиться со списком доступных валют можно с помощью команды /values\n\n" \
           "Чтобы вновь увидеть это сообщение с подсказками наберите /start или /help\n\n" \
           "Чтобы получить список ресурсов где можно посмотреть больше валют введите /sources"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["values"])
def value(message):
    text = "*Доступные валюты:*\n"
    for key in currencys.keys():
        text = "\n- ".join((text, f"_{key}_"))
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["sources"])
def sources(message):
    fpic = get_picture()
    bot.send_photo(message.chat.id, fpic, "*Для дополнительной информации используйте ссылки ниже:*\n\n"
                                          "_Форум CryptoCompare:_\n"
                                          "https://www.cryptocompare.com/\n\n"
                                          "_Сервис выбора финансовых и страховых услуг:_\n"
                                          "https://www.sravni.ru/valjuty/\n\n"
                                          "_Сбербанк:_\n"
                                          "http://www.sberbank.ru/ru/quotes/currencies", parse_mode="Markdown")

@bot.message_handler(content_types=["text"])
def convert(message):
    try:
        values = message.text.lower().split(" ")

        if len(values) != 3:
            raise ConvertionException("Введено некорректное число параметров.")
        or_cur, quantity, fin_cur = values

        total_amount = CryptoConverter.get_price(or_cur, quantity, fin_cur)
    except ConvertionException as e:

        bot.reply_to(message, f"Ошибка при вводе данных:\n{e}")
    except Exception as e1:
        bot.reply_to(message, f'Невозможно обработать команду:\n{e1}')

    else:
        text = f'Цена *{quantity}* шт "_{or_cur}_" в валюте "_{fin_cur}_": *{round(total_amount * float(quantity), 2)}*'
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

bot.polling(none_stop=True)