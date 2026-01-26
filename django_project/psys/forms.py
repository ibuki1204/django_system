from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "customer_code",
            "customer_name",
            "customer_telno",
            "customer_postalcode",
            "customer_address",
            "discount_rate",
            "delete_flag",
        ]

class CustomerUpdateForm(forms.ModelForm):
    discount_rate = forms.IntegerField(required=False)

    class Meta:
        model = Customer
        fields = [
            "customer_name",
            "customer_telno",
            "customer_postalcode",
            "customer_address",
            "discount_rate",
        ]
