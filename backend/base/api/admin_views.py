from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django import forms

from base.models import Slide, SlideImage

import zipfile

class AddSlidesForm(forms.Form):
    prof_discipline = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Professor | Discipline'}))
    hints_amount = forms.IntegerField(min_value=1)
    difficulty_level = forms.IntegerField(min_value=1, max_value=5)

@staff_member_required
def add_slides_view(request):
    
    if request.method == 'POST':
        
        form = AddSlidesForm(request.POST, request.FILES)
        if form.is_valid():
            
            prof_discipline = form.cleaned_data['prof_discipline']
            hints_amount = form.cleaned_data['hints_amount']
            difficulty_level = form.cleaned_data['difficulty_level']
            
            slide = Slide.objects.filter(prof_discipline=prof_discipline).first()
            if not slide:
                slide = Slide.objects.create(
                    prof_discipline=prof_discipline,
                    hints_amount=hints_amount,
                    difficulty_level=difficulty_level
                )
            
            SlideImage.objects.bulk_create([
                SlideImage(hint_index=idx, slide=slide, image=image) for idx, image in enumerate(request.FILES.getlist('images'))
            ])
            
            return redirect('admin:index')
    else:
        form = AddSlidesForm()
    
    context = {
        'title': 'Add Slides Page',
        'form': form,
    }
    
    return render(request, 'add_slides_view.html', context)

class AddZipForm(forms.Form):
    zip = forms.FileField(widget=forms.FileInput(attrs={'placeholder': '', 'accept': '.zip'}))

@staff_member_required
def add_zip_view(request):
    if request.method != 'POST':
        form = AddZipForm()
    else:
        form = AddZipForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'add_zip_view.html', {'title': 'Add .zip File Page', 'form': form})
        allzips = form.cleaned_data['zip']
        
        with zipfile.ZipFile(allzips) as all_zf:
            for idx, filename in enumerate(all_zf.namelist()):
                with all_zf.open(filename) as uploaded_zip:
                    if not uploaded_zip.name.endswith('.zip'):
                        raise Exception("Uploaded file is not a .zip file.")
                    
                    
                    with zipfile.ZipFile(uploaded_zip) as zf:
                        
                        prof_discipline = uploaded_zip.name.split('.')[0]
                        prof_discipline = prof_discipline.replace('__', ' | ')
                        prof_discipline = prof_discipline.replace('_', ' ').title()
                    
                        file_list = zf.namelist() 
                        file_list.sort()
                        hints_amount = len(file_list)
                        difficulty_level = len(file_list) % 5 if len(file_list) < 5 else 5
                        
                        slide = Slide.objects.filter(prof_discipline=prof_discipline).first()
                        if not slide:
                            slide = Slide.objects.create(
                                prof_discipline=prof_discipline,
                                hints_amount=hints_amount,
                                difficulty_level=difficulty_level
                            )
                            
                        for existing_image in SlideImage.objects.filter(slide=slide):
                            existing_image.delete()
                        
                        for idx, filename in enumerate(file_list):
                            with zf.open(filename) as file:
                                parsed_file = ContentFile(file.read(), name=filename)
                                SlideImage.objects.create(hint_index=idx, slide=slide, image=parsed_file)

        if '_addanother' in request.POST:
            return redirect('add_zip_view')
        else:
            return redirect('admin:index')
    
    
    context = {
        'title': 'Add .zip File Page',
        'form': form,
    }
    
    return render(request, 'add_zip_view.html', context)