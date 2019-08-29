from django.shortcuts import render, redirect, render_to_response
from django.views import View
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import CustomUserCreationForm
from .models import CustomUser


class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            email_subject = 'Activate your account'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            message = render_to_string('users/email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()

            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')


User = get_user_model()


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            print(uidb64, token)
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=int(uid))
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        print(user)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            return redirect('blog:post-list')
        else:
            return HttpResponse('Activation link is invalid!')

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponse('Password changed successfully')