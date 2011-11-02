from django import forms
from django.forms import fields
from django.core import exceptions
from csm.models import *
import types

def auto_error_class(field, error_class="alert-message error"):
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

#owner management forms
class OwnerMasterForm(AutoInstanceModelForm):
    class Meta:
        model = Owner
        fields = ('username','ownertype','paperless','address1','address2','city','state','zipcode')
    def __init__(self, *args, **kwargs):
        super(OwnerMasterForm, self).__init__(*args, **kwargs)
        self.fields['individualcount'] = forms.IntegerField(initial=0, widget=forms.HiddenInput())

class OwnerEditForm(AutoInstanceModelForm):
    class Meta:
        model = Owner
        fields = ('paperless','address1','address2','city','state','zipcode')
    def __init__(self, *args, **kwargs):
        super(OwnerEditForm, self).__init__(*args, **kwargs)
        self.fields['individualcount'] = forms.IntegerField(initial=0, widget=forms.HiddenInput())

class IndividualForm(AutoInstanceModelForm):
    class Meta:
        model = Individual
        exclude = ('owner',)

#search forms
class SearchForm(forms.Form):
    searchfield = forms.ChoiceField(label='Search By')
    querystring = forms.CharField(label='Criteria', max_length=200)
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['searchfield'].choices = self.choices
        
class OwnerSearchForm(SearchForm):
    choices = [('number','Owner Number'),('contact','Official Contact')]

#election forms
class ElectionForm(AutoInstanceModelForm):
    class Meta:
        model = Election
        widgets = {'description':forms.Textarea(attrs={'class':'xxlarge', 'rows':'4'})}
    def __init__(self, *args, **kwargs):
        super(ElectionForm, self).__init__(*args, **kwargs)
        self.fields['candidatecount'] = forms.IntegerField(initial=0, widget=forms.HiddenInput())

class CandidateForm(AutoInstanceModelForm):
    class Meta:
        model = Candidate
        exclude = ('election',)
        widgets = {'biography':forms.Textarea(attrs={'class':'xxlarge', 'rows':'4'})}

class VoteForm(AutoInstanceModelForm):
    class Meta:
        model = Vote
        exclude = ('owner')
        widgets = {'candidate':forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['selected'] = forms.BooleanField(required=False)
