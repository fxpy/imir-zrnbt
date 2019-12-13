import random
from string import ascii_lowercase

from django.db import models
from django.core.exceptions import ValidationError
from preferences.models import Preferences

MAX_IMAGE_SIZE_MB = 5
RANDOM_FILENAME_LENGTH = 8


class User(models.Model):
    joined = models.DateTimeField('Первый запуск бота, UTC',
        auto_now_add=True
    )

    user_id = models.BigIntegerField('ID',
        unique=True
    )

    username = models.CharField('@username',
        max_length=256, blank=True, null=True
    )

    first_name = models.CharField('Имя',
        max_length=256, blank=True, null=True
    )
    last_name = models.CharField('Фамилия',
        max_length=256, blank=True, null=True
    )

    last_action = models.CharField(
        max_length=256, blank=True, null=True
    )

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Phone(models.Model):
    phone = models.CharField('Телефон',
        max_length=256,
        help_text='Без "+"'
    )

    name = models.CharField('ФИО',
        max_length=256,
        default='-'
    )

    profession = models.CharField('Профессия',
        max_length=256,
        default='-'
    )
    geobase = models.CharField('Геобаз',
        max_length=256,
        default='-'
    )

    status = models.CharField('Статус',
        max_length=256,
        default='-'
    )

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'телефон'
        verbose_name_plural = 'телефоны'


class Texts(Preferences):
    start_message = models.TextField('Приветствие',
        default='-'
    )
    main_message = models.TextField('Ввод номера',
        default='-'
    )
    result_message = models.TextField('Результат',
        default='-'
    )
    no_result_message = models.TextField('Пусто',
        default='-'
    )

    def __str__(self):
        return 'Тексты'

    class Meta:
        verbose_name = 'список'
        verbose_name_plural = 'списки'


class Image(models.ImageField):
    max_size_mb = MAX_IMAGE_SIZE_MB

    def __init__(self, *args, **kwargs):
        kwargs['upload_to'] = self.get_path
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['validators'] = [self.validate_image]

        return super().__init__(*args, **kwargs)

    def get_path(self, instance, filename, length=RANDOM_FILENAME_LENGTH):
        file_format = filename.split('.')[-1]

        filename = ''
        for index in range(length):
            filename += random.choice(ascii_lowercase)

        return f'{filename}.{file_format}'

    def validate_image(self, image):
        image_size_bytes = image.file.size
        max_size_bytes = self.max_size_mb * 1024 * 1024

        if image_size_bytes > max_size_bytes:
            raise ValidationError(f'Максимальный размер файла - {self.max_size_mb}МБ')


class Post(models.Model):
    created = models.DateTimeField('Дата создания, UTC',
        auto_now_add=True,
        null=True
    )

    users = models.ManyToManyField(verbose_name='Пользователи',
        to='User', related_name='posts',
        blank=True, null=True
    )
    status = models.CharField('Статус',
        max_length=9,
        choices=[
            ('created', 'Создан'),
            ('queue', 'В очереди'),
            ('process', 'Рассылается'),
            ('done', 'Разослан')
        ],
        default='created'
    )

    image = Image('Изображение')
    text = models.TextField('Текст',
        max_length=4000, null=True
    )

    def save(self, *args, **kwargs):
        if self.status == 'created' and self.text:
            self.status = 'queue'

        super().save(*args, **kwargs)

    amount_of_receivers = models.IntegerField('Получателей',
        blank=True, null=True
    )

    def __str__(self):
        time_isoformat = self.created.isoformat(sep=' ', timespec='seconds')
        time_isoformat = time_isoformat[:time_isoformat.index('+')]

        return f'{time_isoformat}'

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
