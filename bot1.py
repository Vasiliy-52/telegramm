import telebot
from extensions import ConvertionException, CryptoConverter
from bot import TOKEN, dict_


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:<имя валюты>' \
           ' <в какую валюту перевести> <количество валюты>\nУвидеть список доступных валют:/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in dict_.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionException('Слишком много/мало параметров.')

        base, quote, amount = value
        cash = CryptoConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {cash}'
        bot.reply_to(message, text)


bot.polling()
