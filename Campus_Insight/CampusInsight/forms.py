# from django.contrib.auth.models import User
from CampusInsight.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Exam, Question

class RegForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Password"}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Password Again"}))
	class Meta:
		model = User
		fields = ["username","email"]
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Username",
			}),
		"email":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Email Id",
			}),
		}

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description', 'date', 'start_time', 'duration', 'docx_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Syllabus'}),
            'docx_file': forms.ClearableFileInput(attrs={'class': 'custom-file-input','id': 'id_docx_file',}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}),
        }

    def clean_duration(self):
        """Ensure the duration is in a valid format."""
        duration = self.cleaned_data.get('duration')
        if isinstance(duration, str):
            try:
                # Attempt to parse the duration string
                duration = forms.fields.DurationField().clean(duration)
            except forms.ValidationError:
                raise forms.ValidationError("Enter the duration in a valid format (e.g., HH:MM:SS).")
        return duration

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option']

