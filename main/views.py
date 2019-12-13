import telebot

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from main.handlers import bot


@csrf_exempt
def update(request):
    update_json = request.body.decode()
    update = telebot.types.Update.de_json(update_json)

    bot.process_new_updates([update])

    return HttpResponse()
