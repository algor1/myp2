from django import forms

class NewTaskForm(forms.Form):
    your_name = forms.CharField(, max_length=100)
    title = forms.CharField(max_length=200, blank=True)
    task_text = forms.TextField()

