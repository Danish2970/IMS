from django import forms
from .models import Location, Floor, Room, Item



class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        # ONLY include fields that exist in your models.py
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Main Warehouse'}),
        }
class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = ['name']  # Ensure 'name' matches your Model field
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 1st Floor',
                # REMOVE any 'readonly': 'readonly' or 'disabled' if they are here!
            }),
        }
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import Location, Floor, Room, Item

# ... (LocationForm, FloorForm, RoomForm remain as before)

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        # These MUST match the {{ form.field_name }} in your HTML template
        fields = ['category', 'item_name', 'brand', 'quantity', 'date_in', 'date_out', 'image']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Office Chair'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. IKEA'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_out': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }