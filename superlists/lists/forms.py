from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item

STR_EMPYT_LIST_ERROR = "You can't have an empty list item"
STR_DUPLICATE_ITEM_ERROR = "You've already got this in you list"


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


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.instance.list = for_list

    # def __int__(self, for_list, *args, **kwargs):
    #     super(ExistingListItemForm, self).__int__(*args, **kwargs)
    #     self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {"text": [STR_DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
