from django import forms
from rango.models import Category, Page
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the name:")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields =('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title:")
    url = forms.URLField(max_length=200, help_text="Please enter the URL")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude=('category',)

    def clean(self):
        clean_data = self.cleaned_data
        url = clean_data.get('url')
        if url and not url.startswith('http://'):
            url = 'http://'+ url
            clean_data['url'] = url
            return clean_data