from django import forms

from lists.models import Item

STR_EMPYT_LIST_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):

    def save(self, for_list, commit=True):
        self.instance.list = for_list
        return super().save(commit)

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': "Enter a to-do item",
                'class': "form-control input-lg",
            })
        }
        error_messages = {
            'text': {'required': STR_EMPYT_LIST_ERROR}
        }
