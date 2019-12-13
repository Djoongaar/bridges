from django import forms

from newsapp.models import News, NewsProduct, NewsDiscussItem


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(NewsForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'


class NewsProductForm(forms.ModelForm):
    class Meta:
        model = NewsProduct
        fields = []

    # def __init__(self, *args, **kwargs):
    #     super(NewsProductForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'


class NewsDiscussItemForm(forms.ModelForm):
    class Meta:
        model = NewsDiscussItem
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(NewsDiscussItemForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
