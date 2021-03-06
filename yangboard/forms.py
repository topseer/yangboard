from django import forms
from django_bootstrap3_daterangepicker import fields
from django_bootstrap3_daterangepicker import widgets

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.forms import ModelForm



class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        #Check date is not in past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

class NameForm(forms.Form):    
    your_name = forms.CharField(label='Name', max_length=100)    

   
class NoteForm(forms.Form):    
    note_title = forms.CharField(label='New Note Title', max_length=100)            
    note_appointment = forms.DateField(label='Appointment Date',initial=datetime.date.today)                                                                
    note_details = forms.CharField(label='Note Details')        

class Rev_Loan(forms.Form):    
    note_title = forms.CharField(label='New Note Title', max_length=100,widget = forms.HiddenInput(), required = False)                



class PeriodFilter(forms.Form):
    Range= fields.DateRangeField(
         widget=widgets.DateRangeWidget(picker_options={'ranges': widgets.common_dates()}),
         label = ''
         )
    