from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib import auth

from machinery1.models import *
from ckeditor.widgets import CKEditorWidget


"""   

class JobForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Vehicle Name :"
        self.fields['location'].label = "Vehicle Location :"
        self.fields['salary'].label = "Capacity in kg :"
        self.fields['description'].label = "Physical Description :"
        self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = "Submission Deadline :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"


        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Catterpillar Bulldozer',
            }
        )        
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : Kakamega',
            }
        )
        self.fields['salary'].widget.attrs.update(
            {
                'placeholder': '800kg - 1200kg',
            }
        )
        self.fields['tags'].widget.attrs.update(
            {
                'placeholder': 'Use comma separated. eg: construction, transport ',
            }
        )                        
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',
                
            }
        )        
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )           
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        ) 
        
        
        
"""
        




class MachineForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Vehicle Name :"
        self.fields['location'].label = "Vehicle Location :"
        self.fields['capacity'].label = "Capacity in kg :"
        self.fields['description'].label = "Physical Description :"
        self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = "Submission Deadline :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"


        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Catterpillar Bulldozer',
            }
        )        
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : Kakamega',
            }
        )
        self.fields['capacity'].widget.attrs.update(
            {
                'placeholder': '800kg - 1200kg',
            }
        )
        self.fields['tags'].widget.attrs.update(
            {
                'placeholder': 'Use comma separated. eg: construction, transport ',
            }
        )                        
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',
                
            }
        )        
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )           
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        ) 
        
        
        
        
        
        
        
     


    class Meta:
        model = Machine

        fields = [
            "title",
            "location",
            "job_type",
            "vtype",
            "capacity",
            "description",
            "tags",
            "last_date",
            "company_name",
            "company_description",
            "url"
            ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Service is required")
        return job_type

    def clean_vtype(self):
        vtype = self.cleaned_data.get('vtype')

        if not vtype:
            raise forms.ValidationError("vtype is required")
        return vtype


    def save(self, commit=True):
        machine = super(MachineForm, self).save(commit=False)
        if commit:
            
            machine.save()
        return machine
        
        
       
       
       
class MachineApplyForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['machine']

class MachineBookmarkForm(forms.ModelForm):
    class Meta:
        model = BookmarkMachine
        fields = ['machine']




class MachineEditForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['title'].label = "Vehicle Title :"
        self.fields['location'].label = "Vehicle Location :"
        self.fields['capacity'].label = "Capacity :"
        self.fields['description'].label = "Vehicle Description :"
        # self.fields['tags'].label = "Tags :"
        self.fields['last_date'].label = "Dead Line :"
        self.fields['company_name'].label = "Company Name :"
        self.fields['url'].label = "Website :"


        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'eg : Catterpillar Bulldozer',
            }
        )        
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'eg : Nairobi',
            }
        )
        self.fields['capacity'].widget.attrs.update(
            {
                'placeholder': '800kg - 1200kg',
            }
        )
        # self.fields['tags'].widget.attrs.update(
        #     {
        #         'placeholder': 'Use comma separated. eg: Python, JavaScript ',
        #     }
        # )                        
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'YYYY-MM-DD ',
            }
        )        
        self.fields['company_name'].widget.attrs.update(
            {
                'placeholder': 'Company Name',
            }
        )           
        self.fields['url'].widget.attrs.update(
            {
                'placeholder': 'https://example.com',
            }
        )    

    
        last_date = forms.CharField(widget=forms.TextInput(attrs={
                    'placeholder': 'Service Name',
                    'class' : 'datetimepicker1'
                }))

    class Meta:
        model = Machine

        fields = [
            "title",
            "location",
            "job_type",
            "vtype",
            "capacity",
            "description",
            "last_date",
            "company_name",
            "company_description",
            "url"
            ]

    def clean_job_type(self):
        job_type = self.cleaned_data.get('job_type')

        if not job_type:
            raise forms.ValidationError("Job Type is required")
        return job_type

    def clean_vtype(self):
        vtype = self.cleaned_data.get('vtype')

        if not vtype:
            raise forms.ValidationError("vtype is required")
        return vtype


    def save(self, commit=True):
        machine = super(MachineEditForm, self).save(commit=False)
      
        if commit:
            machine.save()
        return machine

