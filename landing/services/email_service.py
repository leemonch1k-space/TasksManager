from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class EmailService:
    @classmethod
    def send_activation_email(
            cls, user: User, schema: str, domain: str, token: str
    ) -> None:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = f"{schema}://{domain}/accounts/activate/{uid}/{token}"

        subject = "Welcome to IssueOut!"
        html_content = render_to_string(
            "registration/email/acc_active_email.html",
            {"user": user, "url": url}
        )
        email = EmailMessage(
            subject=subject,
            body=html_content,
            to=[user.email],
        )
        email.content_subtype = "html"

        email.send()
