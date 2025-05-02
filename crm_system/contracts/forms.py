from django import forms
from .models import Contract
from bootstrap_datepicker_plus.widgets import DatePickerInput


class ContractForm(forms.ModelForm):
    clear_file = forms.BooleanField(
        label='Удалить текущий файл?',
        required=False,
        initial=False,
    )

    class Meta:
        model = Contract
        fields = '__all__'
        widgets = {
            'created_at': DatePickerInput(format='%Y-%m-%d').start_of('day'),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get('clear_file'):
            # Удаляем старый файл
            if instance.file:
                instance.file.delete(save=False)
            instance.file = None

        if commit:
            instance.save()
        return instance

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file and self.instance and self.instance.pk:

            return self.instance.file
        return file