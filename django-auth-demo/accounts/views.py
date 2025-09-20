from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

verification_tokens = {}


def send_verification_email(to_email, fname, link):
    smtp_server = "smtp.gmail.com"   
    smtp_port = 587                  
    smtp_user = os.environ.get("SMTP_USER")       
    smtp_password = os.environ.get("SMTP_PASS")   

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = "Verify your account"

    body = f"Hi {fname},\n\nPlease click the link to verify your email:\n{link}\n\nThank you."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"Verification email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        messages.error(None, "Failed to send verification email. Contact admin.")

def signup_view(request):
    if request.method == "POST":
        fname = request.POST.get("fname", "").strip()
        lname = request.POST.get("lname", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if not (fname and email and password):
            messages.error(request, "Please fill required fields (first name, email, password).")
            return redirect("signup")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered. Try logging in.")
            return redirect("signup")

        user = User.objects.create_user(username=email, email=email, password=password,
                                        first_name=fname, last_name=lname)
        Profile.objects.create(user=user, mobile=mobile, is_verified=False)

        token = str(uuid.uuid4())
        verification_tokens[token] = user.username
        link = request.build_absolute_uri(f"/accounts/verify/{token}/")
        send_verification_email(email, fname, link)

        messages.success(request, "Account created! Check your email for verification link.")
        return redirect("login")

    return render(request, "accounts/signup.html")


def verify_email(request, token):
    if token in verification_tokens:
        username = verification_tokens.pop(token)
        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            profile.is_verified = True
            profile.save()
            messages.success(request, "Email verified! You can now log in.")
        except User.DoesNotExist:
            messages.error(request, "User not found for this token.")
    else:
        messages.error(request, "Invalid or expired token.")
    return redirect("login")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        user = authenticate(username=email, password=password)
        if user is not None:
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found. Contact admin.")
                return redirect("login")

            if profile.is_verified:
                login(request, user)
                return redirect("about")
            else:
                messages.error(request, "Please verify your email before logging in.")
                return redirect("login")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("login")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def about_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "accounts/about.html")