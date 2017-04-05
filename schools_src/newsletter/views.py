from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse
from .forms import ContactForm
from .forms import AboutForm


def home_out(request):
	instance = request.user
	return render(request,'newsletter/home_out.html',{'instance':instance})

def contact(request):
	form1 = ContactForm(request.POST or None)
	context = {
	'form' : form1,
	'title': 'Contact us any time!',

	}
	if form1.is_valid():
		message = form1.cleaned_data.get('message')
		full_name = form1.cleaned_data.get('full_name')
		email = form1.cleaned_data.get('email') 

		subject = 'site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = ['imperialarkon@gmail.com']
		contact_message = message
 
		send_mail(subject,contact_message,from_email,
				  to_email,fail_silently=False)

		context = {
		'form': form1,
		'title2': 'We have received your mail, we will contact you soon! Bye!',
		'title': 'Contact us any time!',
		}

	return render(request, 'newsletter/contact.html', context)

def about(request):
	form1 = AboutForm(request.POST or None)
	context = {
	'form' : form1,
	'title1': 'Join Team schools',
	}

	if form1.is_valid():
		message = form1.cleaned_data.get('message')
		full_name = form1.cleaned_data.get('full_name')
		email = form1.cleaned_data.get('email')

		subject = 'site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = ['imperialarkon@gmail.com']
		contact_message = message + from_email

		send_mail(subject,contact_message,from_email,
				  to_email,fail_silently=False)

		context = {
		'form':form1,
		'title2' : 'We appreciate your interest, We\'ll contact you soon!'
		}

	return render(request, 'newsletter/about.html', context)

def test(request):
	context = {
	'a': 'a',
	}
	return render(request,'date_picker.html',context)