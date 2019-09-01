from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import UserCreationForm, LoginForm
from blog.tasks import send_mail_task


User = get_user_model()


class SignupView(View):
    form_class = UserCreationForm

    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'account/signup.html', {'form': self.form_class})
        else:
            return redirect('blog:post-list')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            email_subject = 'Activate your account'
            message = render_to_string('account/email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail_task.delay(email_subject,
                           message,
                           form.cleaned_data.get('email'))

            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
        return render(request, 'account/signup.html', {'form': form})


class ActivateView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=int(uid))
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            return redirect('blog:post-list')
        else:
            return HttpResponse('Activation link is invalid!')


class LoginView(View):
    form_class = LoginForm

    def get(self, request):
        if request.user.is_anonymous:
            form = self.form_class()
            return render(request, 'account/login.html', {'form': form})
        else:
            return redirect('blog:post-list')

    def post(self, request):
        next_url = request.GET.get('next')
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                if next_url:
                    return redirect(next_url)
                return redirect('blog:post-list')
            else:
                return render(request,
                              'account/login.html',
                              {'form': form, 'error': 'Wrong credentials'})
        return render(request, 'account/login.html', {'form': form})
