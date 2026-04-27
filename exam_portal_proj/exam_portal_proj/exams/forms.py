from django import forms
from .models import ExamForm


class ExamFormSubmission(forms.ModelForm):
    """
    ModelForm tied to ExamForm model.
    We exclude 'student' and 'submitted_at' because those are set in the view,
    not filled in by the student directly.
    """
    class Meta:
        model  = ExamForm
        fields = ['full_name', 'course', 'year', 'address', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. B.Tech CSE, BCA, MCA',
            }),
            'year': forms.Select(attrs={
                'class': 'form-select',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your current address',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-digit mobile number',
            }),
        }
        labels = {
            'full_name'   : 'Full Name',
            'course'      : 'Course / Programme',
            'year'        : 'Academic Year',
            'address'     : 'Address',
            'phone_number': 'Phone Number',
        }

    # Custom validation: phone must be digits only, 10-15 chars
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain digits only.")
        if not (10 <= len(phone) <= 15):
            raise forms.ValidationError("Phone number must be between 10 and 15 digits.")
        return phone
