from django import forms

from cities_light.models import Country, Region, SubRegion

from .models import HouseModel, FlatModel, SpaceModel, BUILDING_TYPES, ACCOMMODATION_TYPES



class HouseModelForm(forms.ModelForm):
    # Dependent Drop down list in django
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['state'].queryset = Region.objects.none()
        self.fields['city'].queryset = SubRegion.objects.none()
        
        if 'country' in self.data:
            try:
                country_id = int(self.data['country'])
                print(country_id, 'form')
                self.fields['state'].queryset = Region.objects.filter(country__id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        if 'state' in self.data:
            try:
                state = int(self.data['state'])
                self.fields['city'].queryset = SubRegion.objects.filter(region__id=state).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            state = self.instance.state.name
            # print(state)
            self.fields['state'].queryset = self.instance.country.region_set
            self.fields['city'].queryset = SubRegion.objects.filter(region__name=state).order_by('name')
    
    
    class Meta:
        model = HouseModel
        fields = [
            'name', 'address',
            'country',
            'state', 'city',
            'building_type',
            'accommodation_type',
            'total_number_of_accommodation_space',
            'available_number_accommodation_space',
            'house_price', 'electricity',
            'water', 'newly_built', 'sale',
            'exterior_image', 'c_of_o', 'd_of_a', 'tenant_agreement'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),  
            'state': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'building_type': forms.Select(attrs={'class': 'form-control'}),
            'accommodation_type': forms.Select(attrs={'class': 'form-control'}),
            'total_number_of_accommodation_space': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_number_accommodation_space': forms.NumberInput(attrs={'class': 'form-control'}),
            'house_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'electricity': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'water': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'newly_built': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'exterior_image': forms.FileInput(attrs={'class': 'form-control'}),
          
            'c_of_o' : forms.FileInput(attrs={'class': 'form-control'}),
            'd_of_a': forms.FileInput(attrs={'class': 'form-control'}),
            'tenant_agreement': forms.FileInput(attrs={'class': 'form-control'}),
            
        }


class FlatModelForm(forms.ModelForm):
    
    class Meta:
        model = FlatModel
        fields = [
            'house', 'floor',
            'side', 'accommodation_type',
            'price',
            'bedroom',
            'kitchen', 'sittingroom',
            'convience'
        ]
        
        widgets = {
            'house': forms.Select(attrs={'class': 'form-control'}),
            'floor': forms.Select(attrs={'class':'form-control'}),
            'side': forms.Select(attrs={'class':'form-control'}),
            'accommodation_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'bedroom': forms.FileInput(attrs={'class': 'form-control'}),
            'kitchen': forms.FileInput(attrs={'class': 'form-control'}),
            'sittingroom': forms.FileInput(attrs={'class': 'form-control'}),
            'convience': forms.FileInput(attrs={'class': 'form-control'}),
        }



class SpaceModelForm(forms.ModelForm):
    class Meta:
        model = SpaceModel
        exclude = ['taken']   
        
        widgets = {
            'house': forms.Select(attrs={'class': 'form-control'}),
            'floor': forms.Select(attrs={'class':'form-control'}),
            'spacename': forms.TextInput(attrs={'class':'form-control'}),
            'accommodation_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
        
class LookUpForm(forms.Form):
    location = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter the area you want to live'}))
    building_type = forms.ChoiceField(choices=BUILDING_TYPES, widget=forms.Select(attrs={'class' : 'form-control'}))
    accommodation_type = forms.ChoiceField(choices=ACCOMMODATION_TYPES, widget=forms.Select(attrs={'class' : 'form-control'}))
    min_price = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '25000'}))
    max_price = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : '100000'}))

