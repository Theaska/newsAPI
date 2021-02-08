from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_notification(template_name, subject, receivers, **kwargs):
    domain = Site.objects.get_current()
    context = kwargs.get('context', {})
    context.update({
        'domain': domain,
    })
    template = get_template(template_name)
    message = template.render(context)
    msg = EmailMultiAlternatives(subject, from_email=settings.EMAIL_HOST_USER, to=receivers)
    msg.attach_alternative(message, "text/html")
    msg.send()

