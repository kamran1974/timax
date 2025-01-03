from django import forms

class LogFilterForm(forms.Form):
    from_date = forms.DateField(
        label='از تاریخ',
        widget=forms.DateInput(attrs={'class': 'jalali_date-input'}),
        required=False
    )
    to_date = forms.DateField(
        label='تا تاریخ',
        widget=forms.DateInput(attrs={'class': 'jalali_date-input'}),
        required=False
    )


class CSVUploadForm(forms.Form):
    file = forms.FileField(label="آپلود فایل CSV")
