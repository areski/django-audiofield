.. _forms:

AudioFile Forms
===============

.. _Audiofile_Forms:

Forms Definition
----------------

This form aims to be used in the django admin, support all the features for convertion per default::
    
    class AdminAudioFileForm(ModelForm)

The following form aims to be used on frontend to power simple upload of audio files without convertion::
    
    CustomerAudioFileForm(ModelForm)


Forms Usage
-----------

We provide you a simple example of using the forms to list and upload audio file on the frontend.

In url.py::
    
    ...
    (r'^$', 'frontend.views.index_view'),
 
In view.py::    
    
    ...
    @login_required
    def index_view(request):
        template = 'frontend/demo.html'
        form = CustomerAudioFileForm()
        audio_list = AudioFile.objects.all()
        # Add audio
        if request.method == 'POST':
            form = CustomerAudioFileForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = User.objects.get(username=request.user)
                obj.save()
                request.session["msg"] = _('"%(name)s" is added successfully.') %\
                {'name': request.POST['name']}
                return HttpResponseRedirect('/')

            # To retain frontend widget, if form.is_valid() == False
            form.fields['audio_file'].widget = CustomerAudioFileWidget()
        data = {
           'audio_form': form,
           'audio_list': audio_list,
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
                request.session["msg"] = _('"%(name)s" is updated successfully.') \
                % {'name': request.POST['name']}
                return HttpResponseRedirect('/')
        
        template = 'frontend/audio.html'
        data = {
           'audio_form': form,
        }
        return render_to_response(template, data,
               context_instance=RequestContext(request))

