import logging
import re

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler
)


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False


logging.basicConfig(filename="log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

TOKEN = '2067328448:AAFkDDEjFb6oB8NrMXXposDDlI8OmN32OVU'


def start(update: Update, _):
    update.message.reply_text("Введите /survey чтобы начать опрос")


def survey(update: Update, _):
    update.message.reply_text("Вы начали опрос")
    update.message.reply_text("Как вас зовут? \n (ФИО полностью)")
    return 1


def fio_response(update: Update, context):
    fio = re.findall('\w+\s\w+(\s\w+)?', update.message.text)
    if fio.__len__() == 0:
        update.message.reply_text('Неверно указано имя')
        return 1
    else:
        update.message.reply_text("Сколько вам лет?")
        return 2


def age_response(update: Update, context):
    age = re.findall('\d+', update.message.text)
    global point
    if age.__len__() == 0:
        update.message.reply_text("Неверно указан возраст")
        return 2
    else:
        if int(age[0]) > 40:
            point = 0
        else:
            point = 1
        update.message.reply_text("Где вы проживаете? ")
        return 3


def state_response(update: Update,  context):
    state = update.message.text
    update.message.reply_text("Укажите номер телефона :")
    return 4


def phone_response(update: Update,  context):
    phone = re.findall('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', update.message.text)
    if phone.__len__() == 0:
        update.message.reply_text("Номер не соответствует формату")
        return 4
    else:
        update.message.reply_text("Укажите email")
        return 5


def email_response(update: Update,  context):
    email = re.findall(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+', update.message.text)
    if email.__len__() == 0:
        update.message.reply_text("Неверно указана почта")
        return 5
    else:
        update.message.reply_text("Есть ли образование в сфере дизайна? \n Да/Нет")
        return 6


def education_response(update: Update,  context):
    education = re.findall('^(Да|Нет)$', update.message.text)
    global point
    if education.__len__() != 0:
        if education[0] == 'Нет':
            point = point + 1
        update.message.reply_text("Умеете ли вы работать в Adobe Illustrator и Photoshop? \n Да/Нет")
        return 7
    else:
        update.message.reply_text("Укажите либо да, либо нет")
        return 6


def ability_response(update: Update,  context):
    adob_photo = re.findall('^(Да|Нет)$', update.message.text)
    global point
    if adob_photo.__len__() != 0:
        if adob_photo[0] == 'Нет':
            point = point + 1
        update.message.reply_text("Укажите стаж работы в годах(0.5,1.5)")
        return 8
    else:
        update.message.reply_text("Укажите либо ДА, либо НЕТ")
        return 7


def exp_design_response(update: Update,  context):
    exp = update.message.text
    if not is_float(exp):
        update.message.reply_text("Указывайте в годах:0.5,1.5,2 и т.д.")
        return 8
    else:
        update.message.reply_text("Укажите ссылку на портфолио. \n Если его нет ответьте 'нет' ")
        return 9


def portfolio_response(update: Update,  context):
    port = update.message.text
    update.message.reply_text("Готовы ли вы к работе на полную занятость в нашей компании, 5-8ч/день")
    return 10


def zanyt_response(update: Update,  context):
    answer = re.findall('^(Да|Нет)$', update.message.text)
    global point
    if answer.__len__() != 0:
        if answer[0] == 'Нет':
            point = point + 1
        update.message.reply_text("На какой уровень дохода вы рассчитываете?")
        return 11
    else:
        update.message.reply_text("Укажите либо Да, либо Нет")
        return 10


def zp_response(update: Update,  context):
    zp = re.findall('\d+', update.message.text)
    global point
    if int(zp[0]) >= 70000:
        point = point + 1
    update.message.reply_text("Из какого источника вы узнали о вакансии")
    return 12


def info_reponse(update: Update,  context):
    info = update.message.text
    global point
    update.message.reply_text("Спасибо за заполнение анкеты")
    if point == 5:
        update.message.reply_text("Вы нам  не подходите")
    else:
        update.message.reply_text("Вы нам подходите")
    return ConversationHandler.END


def stop(update: Update):
    update.message.reply_text("Good Bye!")
    return ConversationHandler.END


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('survey', survey)],

    states={
        1: [MessageHandler(Filters.text & ~Filters.command, fio_response)],
        2: [MessageHandler(Filters.text & ~Filters.command, age_response)],
        3: [MessageHandler(Filters.text & ~Filters.command, state_response)],
        4: [MessageHandler(Filters.text & ~Filters.command, phone_response)],
        5: [MessageHandler(Filters.text & ~Filters.command, email_response)],
        6: [MessageHandler(Filters.text & ~Filters.command, education_response)],
        7: [MessageHandler(Filters.text & ~Filters.command, ability_response)],
        8: [MessageHandler(Filters.text & ~Filters.command, exp_design_response)],
        9: [MessageHandler(Filters.text & ~Filters.command, portfolio_response)],
        10: [MessageHandler(Filters.text & ~Filters.command, zanyt_response)],
        11: [MessageHandler(Filters.text & ~Filters.command, zp_response)],
        12: [MessageHandler(Filters.text & ~Filters.command, info_reponse)],
    },

    fallbacks=[CommandHandler('stop', stop)]
)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
