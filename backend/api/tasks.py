from django.core.mail import send_mail

from backend.celery import app
from backend.settings import EMAIL_HOST_USER


@app.task
def send_confirmation_code(email, code):
    try:
        send_mail(
            'Вы зарегистрировались на ресурсе.',
            f'Ваш код-подтверждение: {code}',
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return 'Email sent successfully'
    except Exception as e:
        return f'Email sending failed: {str(e)}'
