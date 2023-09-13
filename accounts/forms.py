from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import User
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta): # UCF 상속, model만 내것으로수정하고 나머지 그대로
        model = get_user_model()
        fields = ('username', )
        

class CustomAuthenticationForm(AuthenticationForm):
    pass

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)