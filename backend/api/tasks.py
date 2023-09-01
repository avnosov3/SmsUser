from django.core.mail import send_mail

from backend.celery import app
from backend.settings import ADMIN_EMAIL


@app.task
def send_confirmation_code(email, code):
    try:
        send_mail(
            'Вы зарегистрировались на ресурсе.',
            f'Ваш код-подтверждение: {code}',
            ADMIN_EMAIL,
            [email],
            fail_silently=False,
        )
        return 'Email sent successfully'
    except Exception as e:
        return f'Email sending failed: {str(e)}'
