from django import forms
import re
from django.contrib.auth.models import User
from .models import Comment, Profile, ShippingAddress

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Tài khoản', max_length=30, widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())
    first_name = forms.CharField(label='Nhập tên', widget=forms.TextInput())
    last_name = forms.CharField(label='Nhập họ', widget=forms.TextInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError("Mật khẩu không hợp lệ")

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Tên tài khoản có kí tự đặc biệt")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")
   
    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Địa chỉ email không hợp lệ")
        # try:
        # #   User.objects.get(email = email)
        #     User.objects.filter(email=email).first()
        #     test =  User.objects.filter(email=email).first()
        #     print("test",test)
        # except:
        #     return email
        # raise forms.ValidationError("Email đã tồn tại")
    
        user_by_email = User.objects.filter(email=email).first()
        if user_by_email is None:
            return email
        else:
            raise forms.ValidationError("Email đã tồn tại")

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'],first_name=self.cleaned_data['first_name'],last_name=self.cleaned_data['last_name'],)



class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.author = self.author
        comment.product = self.product.first()
        comment.save()

    class Meta:
        model = Comment
        fields = ["body"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ("customer", "order", "address", "mobile")