import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phones.settings')
django.setup()

from time import sleep

from django.conf import settings

from main import models
from main.handlers import bot

DELAY = 1


def send_post_to_user(post, user):
    text = post.text

    if post.image:
        image_url = f'https://{settings.ALLOWED_HOSTS[0]}/media/{post.image}'

        bot.send_photo(user.user_id,
            photo=image_url,
            caption=text,
            parse_mode='html'
        )
    else:
        bot.send_message(user.user_id,
            text=text,
            parse_mode='html'
        )


def process_post(post):
    post.status = 'process'
    post.save()

    users = list(post.users.all())
    if not users:
        users = list(models.User.objects.all())

    receivers = []
    for user in users:
        receivers.append(user)

    amount_of_receivers = 0

    for user in receivers:
        try:
            send_post_to_user(post, user)
        except BaseException as error:
            pass
        else:
            amount_of_receivers += 1

    post.status = 'done'
    post.amount_of_receivers = amount_of_receivers
    post.save()


def main():
    while True:
        try:
            post = models.Post.objects.filter(status='queue').order_by('created').first()
            if post:
                process_post(post)
        except BaseException as error:
            pass

        sleep(DELAY)


if __name__ == '__main__':
    main()
