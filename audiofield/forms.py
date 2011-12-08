from django.forms.fields import FileField

        
class AudioFormField(FileField):
    
    def clean(self, data, initial=None):
        if data != '__deleted__':
            return super(AudioFormField, self).clean(data, initial)
        else:
            return '__deleted__'
