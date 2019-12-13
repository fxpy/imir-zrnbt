import telebot

from django.conf import settings

from preferences import preferences

from main.models import User, Phone

bot = telebot.TeleBot(settings.TOKEN, threaded=False)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = User.objects.get(user_id=message.chat.id)
        user.username = message.chat.username
        user.first_name = message.chat.first_name
        user.last_name = message.chat.last_name
    except User.DoesNotExist:
        user = User(
            user_id=message.chat.id,
            username=message.chat.username,
            first_name=message.chat.first_name,
            last_name=message.chat.last_name
        )
    finally:
        user.save()

    bot.send_message(message.chat.id,
        preferences.Texts.start_message,
        parse_mode='html'
    )
    bot.send_message(message.chat.id,
        preferences.Texts.main_message,
        parse_mode='html'
    )


@bot.message_handler(content_types=['text', 'contact'])
def typing(message):
    try:
        user = User.objects.get(user_id=message.chat.id)
        user.username = message.chat.username
        user.first_name = message.chat.first_name
        user.last_name = message.chat.last_name
    except User.DoesNotExist:
        user = User(
            user_id=message.chat.id,
            username=message.chat.username,
            first_name=message.chat.first_name,
            last_name=message.chat.last_name
        )
    finally:
        user.save()

    if message.contact:
        phone = message.contact.phone_number or ''
    else:
        phone = message.text
    new_phone = ''
    for character in phone:
        if character.isdigit():
            new_phone += character
    phone = new_phone

    for ph in Phone.objects.all():
        if ph.phone == phone:
            bot.send_message(message.chat.id,
                preferences.Texts.result_message.format(
                    phone=ph.phone,
                    name=ph.name,
                    occupation=ph.profession,
                    geo=ph.geobase,
                    status=ph.status
                ),
                parse_mode='html'
            )
            bot.send_message(message.chat.id,
                preferences.Texts.main_message,
                parse_mode='html'
            )
            return

    if len(phone) >= 9:
        for ph in Phone.objects.all():
            if ph.phone.endswith(phone):
                bot.send_message(message.chat.id,
                    preferences.Texts.result_message.format(
                        phone=ph.phone,
                        name=ph.name,
                        occupation=ph.profession,
                        geo=ph.geobase,
                        status=ph.status
                    ),
                    parse_mode='html'
                )
                bot.send_message(message.chat.id,
                    preferences.Texts.main_message,
                    parse_mode='html'
                )
                return

    bot.send_message(message.chat.id,
        preferences.Texts.no_result_message,
        parse_mode='html'
    )
    bot.send_message(message.chat.id,
        preferences.Texts.main_message,
        parse_mode='html'
    )
