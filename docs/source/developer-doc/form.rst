.. _forms:

AudioFile Forms
===============

.. _Audiofile_Forms:

Forms Definition
----------------

This form aims to be used in the django admin, support all the features for convertion per default::
    
    class AdminAudioFileForm(ModelForm):
        class Meta:
            model = AudioFile
            fields = ['name', 'audio_file']

The following form aims to be used on frontend to power simple upload of audio files without convertion::

    class CustomerAudioFileForm(ModelForm):
        audio_file = forms.FileField(widget=CustomerAudioFileWidget)
        class Meta:
            model = AudioFile
            fields = ['name', 'audio_file']
            exclude = ('user',)


Forms Usage
-----------

We provide you a simple example of using the forms to list and upload audio file on the frontend.

In url.py::
    
    ...
    (r'^$', 'frontend.views.add_audio'),
 
In view.py::    
    
    ...
    @login_required
    def add_audio(request):
        template = 'frontend/add_audio.html'
        form = CustomerAudioFileForm()

        # Add audio
        if request.method == 'POST':
            form = CustomerAudioFileForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = User.objects.get(username=request.user)
                obj.save()
                return HttpResponseRedirect('/')

            # To retain frontend widget, if form.is_valid() == False
            form.fields['audio_file'].widget = CustomerAudioFileWidget()

        data = {
           'audio_form': form,
        }

        return render_to_response(template, data,
               context_instance=RequestContext(request))
               


This is an other example how to edit the audiofield on the frontend.

In url.py::
    
    ...
    (r'^edit/(.+)/$', 'frontend.views.edit_audio'),


In view.py::

    ...
    @login_required
    def edit_audio(request, object_id):

        obj = AudioFile.objects.get(pk=object_id)
        form = CustomerAudioFileForm(instance=obj)

        if request.GET.get('delete'):
            # perform delete
            if obj.audio_file:
                if os.path.exists(obj.audio_file.path):
                    os.remove(obj.audio_file.path)
            obj.delete()
            return HttpResponseRedirect('/')
        
        if request.method == 'POST':
            form = CustomerAudioFileForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
        
        template = 'frontend/edit_audio.html'

        data = {
           'audio_form': form,
        }
        
        return render_to_response(template, data,
               context_instance=RequestContext(request))

