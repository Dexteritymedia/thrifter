from django import forms

from .models import Category, Contact

class BudgetForm(forms.Form):
    budget = forms.DecimalField(label="Enter your budget", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={"placeholder":"e.g., 20000", "class":"form-control"}))
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    include_accommodation = forms.BooleanField(required=False, label="Include Accommodation", widget=forms.CheckboxInput())


class ContactForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"name@example.com", "class":"form-control"}))
    choice = forms.ChoiceField(label="Quick message", required=False, choices=Contact.CHOICE, widget=forms.Select(attrs={"class":"form-control"}))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control", "id":"floatingTextarea"}))
    class Meta:
        model = Contact
        fields = ['email', 'name', 'message', 'choice', 'phone_no']

    def clean(self):
        cleaned_data = super().clean()
        message = cleaned_data.get('message')
        choice = cleaned_data.get('choice')

        if not message and not choice:
            raise forms.ValidationError("Please fill out either the message field or the choice field")
