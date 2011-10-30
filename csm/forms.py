from django import forms
from django.forms import fields
from django.core import exceptions
from csm.models import *
import types

def auto_error_class(field, error_class="error"):
    """
       Monkey-patch a Field instance at runtime in order to automatically add a CSS
       class to its widget when validation fails and provide any associated error
       messages via a data attribute
    """

    inner_clean = field.clean

    def wrap_clean(self, *args, **kwargs):
       try:
           return inner_clean(*args, **kwargs)
       except exceptions.ValidationError as ex:
           self.widget.attrs["class"] = self.widget.attrs.get(
               "class", ""
           ) + " " + error_class
           self.widget.attrs["title"] = ", ".join(ex.messages)
           raise ex

    field.clean = types.MethodType(wrap_clean, field, field.__class__)

    return field
    
#extension form to add pk field and find instance on submit
class AutoInstanceModelForm(forms.ModelForm):
    def __init__(self, postdata=None, *args, **kwargs):
        if "instance" in kwargs:
            instance = kwargs.pop("instance")
        elif postdata:
            instance_pk = postdata.get(kwargs.get('prefix') + '-pk', None) if kwargs.get('prefix') else postdata.get('pk', None)
            instance = self.Meta.model.objects.get(pk=instance_pk) if instance_pk else None
        else:
            instance = None
            
        super(AutoInstanceModelForm, self).__init__(postdata, *args, instance=instance, **kwargs)
        self.fields['pk'] = forms.IntegerField(required=False, initial=self.instance.pk, widget=forms.HiddenInput())
        self.fields['delete'] = forms.IntegerField(initial=0, widget=forms.HiddenInput())
        for f in self.fields:
            self.fields[f] = auto_error_class(self.fields[f])

#customer management forms
class OwnerForm(AutoInstanceModelForm):
    class Meta:
        model = Owner
        fields = ('username',)
    def __init__(self, *args, **kwargs):
        super(OwnerForm, self).__init__(*args, **kwargs)
        self.fields['individualcount'] = forms.IntegerField(initial=0, widget=forms.HiddenInput())
        self.fields['officialcontactprefix'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'mainicon icon contacticon', 'readonly':'readonly'}))
        for f in self.fields:
            self.fields[f] = auto_error_class(self.fields[f])

class IndividualForm(AutoInstanceModelForm):
    class Meta:
        model = Individual
        exclude = ('owner',)
