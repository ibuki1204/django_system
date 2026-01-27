from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    discount_rate = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=99,
        label="割引率"
    )

    class Meta:
        model = Customer
        fields = [
            "customer_code",
            "customer_name",
            "customer_telno",
            "customer_postalcode",
            "customer_address",
            "discount_rate",
        ]
        widgets = {
            "customer_code": forms.TextInput(attrs={
                "maxlength": "6",
                "placeholder": "6桁"
            }),
            "customer_name": forms.TextInput(attrs={
                "maxlength": "20",
            }),
            "customer_telno": forms.TextInput(attrs={
                "maxlength": "13",
                "placeholder": "ハイフン可"
            }),
            "customer_postalcode": forms.TextInput(attrs={
                "maxlength": "8",
                "placeholder": "例:123-4567"
            }),
            "customer_address": forms.TextInput(attrs={
                "maxlength": "40",
            }),
        }

    # 仕様書ベースの入力チェック（業務アプリっぽく）
    def clean_customer_code(self):
        code = self.cleaned_data["customer_code"]
        if len(code) != 6:
            raise forms.ValidationError("得意先コードは6桁で入力してください。")
        return code


class CustomerUpdateForm(forms.ModelForm):
    discount_rate = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=99,
        label="割引率"
    )

    class Meta:
        model = Customer
        fields = [
            "customer_name",
            "customer_telno",
            "customer_postalcode",
            "customer_address",
            "discount_rate",
        ]
        widgets = {
            "customer_name": forms.TextInput(attrs={
                "maxlength": "20",
            }),
            "customer_telno": forms.TextInput(attrs={
                "maxlength": "13",
                "placeholder": "ハイフン可"
            }),
            "customer_postalcode": forms.TextInput(attrs={
                "maxlength": "8",
                "placeholder": "例:123-4567"
            }),
            "customer_address": forms.TextInput(attrs={
                "maxlength": "40",
            }),
        }
