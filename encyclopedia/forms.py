from django import forms # type: ignore

class CreatePageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'style': 'height: 300px; overflow-y: auto;'}))

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 300px; overflow-y: auto;'}), label="Content")

