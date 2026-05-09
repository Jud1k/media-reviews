from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""
        
        self.fields["username"].widget.attrs.update(
            {
                "class": "w-full text-white px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent",
                "placeholder": "Enter your username",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "w-full text-white px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent",
                "placeholder": "Create a password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "w-full text-white px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent",
                "placeholder": "Confirm password",
            }
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "w-full text-white px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent",
                "placeholder": "Enter your username",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "w-full text-white px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent",
                "placeholder": "Enter your password",
            }
        )
