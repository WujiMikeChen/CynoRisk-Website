from flask import Flask, request, render_template, redirect, flash
import os
from flask_mail import Mail, Message
import re
import dns.resolver

def is_valid_email_format(email):
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", email)

def has_mx_record(email):
    try:
        domain = email.split('@')[1]
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except Exception:
        return False
    
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'txt', 'csv', 'xlsx', 'xls', 'txt', 'tsv',
    'json', 'xml', 'log', 'zip', 'gz', 'tar', '7z','py','r','pkl'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS