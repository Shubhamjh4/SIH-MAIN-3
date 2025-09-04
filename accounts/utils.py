import uuid
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

def generate_token():
    return str(uuid.uuid4())

def send_verification_email(user, token):
    subject = 'Verify your email address'
    verification_link = f'http://localhost:3000/verify-email/{token}'
    
    html_message = render_to_string('accounts/email/verify_email.html', {
        'user': user,
        'verification_link': verification_link
    })
    
    send_mail(
        subject=subject,
        message=f'Click this link to verify your email: {verification_link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message
    )

def send_password_reset_email(user, token):
    subject = 'Reset your password'
    reset_link = f'http://localhost:3000/reset-password/{token}'
    
    html_message = render_to_string('accounts/email/reset_password.html', {
        'user': user,
        'reset_link': reset_link
    })
    
    send_mail(
        subject=subject,
        message=f'Click this link to reset your password: {reset_link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message
    )
