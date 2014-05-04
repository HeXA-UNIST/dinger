from django import forms

class ArticleForm(forms.Form):
    subject = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    private = forms.BooleanField(required=False)

    # upload

class CommentForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea)
