from django.shortcuts import render

# Create your views here.
# validator/views.py

import csv
import requests
import re
import json
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile

def validate_email(email):
    # Use a regular expression to validate email format
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return False

    # Use Google's DNS-over-HTTPS API to validate the domain
    domain = email.split('@')[1]
    url = f'https://dns.google/resolve?name={domain}&type=A'
    response = requests.get(url)
    data = json.loads(response.content)
    if 'Answer' in data:
        return True
    return False

def validate_domain(domain):
    # Use Google's DNS-over-HTTPS API
    url = f'https://dns.google/resolve?name={domain}&type=A'
    response = requests.get(url)
    data = json.loads(response.content)
    if 'Answer' in data:
        return True
    return False

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            emails = []
            domains = []
            with open(uploaded_file.file.path, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    for item in row:
                        if '@' in item:
                            email = item
                            emails.append(email)
                            domain = email.split('@')[1]
                            if domain not in domains:
                                domains.append(domain)
            valid_emails = []
            invalid_emails = []
            valid_domains = []
            invalid_domains = []
            for email in emails:
                if validate_email(email):
                    valid_emails.append(email)
                else:
                    invalid_emails.append(email)
            for domain in domains:
                if validate_domain(domain):
                    valid_domains.append(domain)
                else:
                    invalid_domains.append(domain)
            context = {
                'emails': emails,
                'domains': domains,
                'valid_emails': valid_emails,
                'invalid_emails': invalid_emails,
                'valid_domains': valid_domains,
                'invalid_domains': invalid_domains,
            }
            return render(request, 'validator/result.html', context)
    else:
        form = UploadFileForm()
    return render(request, 'validator/index.html', {'form': form})