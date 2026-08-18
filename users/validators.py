import datetime

from django.core.exceptions import ValidationError

MAX_IMAGE_SIZE_MB = 5
MAX_IMAGE_SIZE = MAX_IMAGE_SIZE_MB * 1024 * 1024

def validate_image_size(file) -> None:
    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError(f'Размер файла не должен превышать {MAX_IMAGE_SIZE_MB} МБ.')


def validate_date_of_birth(date_of_birth: datetime.date | None) -> None:
    if date_of_birth and date_of_birth > datetime.date.today():
        raise ValidationError('Укажите корректную дату рождения.')
