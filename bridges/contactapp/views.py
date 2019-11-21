from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from contactapp.forms import ContactForm


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email_data = form.save()
            subject = 'Заявка с сайта'
            message = 'Имя: {}\nНомер телефона: {}\nE-mail: {}\nТема: {}\nСообщение: {}'.format(email_data.name,
                                                                                                email_data.phone,
                                                                                                email_data.email,
                                                                                                email_data.subject,
                                                                                                email_data.message)
            send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
            form = ContactForm()
    else:
        form = ContactForm()

    context = {
        'page_title': 'Контакты',
        'bred_title': 'Контакты',
        'form': form,
    }
    return render(request, 'contactapp/contact.html', context)
