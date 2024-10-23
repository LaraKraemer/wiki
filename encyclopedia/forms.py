from django import forms


class EntryForm(forms.Form):
    title = forms.CharField(required=True, label="Title", widget=forms.TextInput(attrs={
            'class': 'form-control',  
            'placeholder': 'Enter title here...' 
        }))
    content = forms.CharField(required=True, label="Content",
                              widget=forms.Textarea(attrs={
            'class': 'form-control',  
            'placeholder': 'Enter content here...' 
        }))
