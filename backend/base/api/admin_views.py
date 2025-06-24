from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django import forms

from base.models import Slide, SlideImage

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
                SlideImage(hint_index=idx + 1, slide=slide, image=image) for idx, image in enumerate(request.FILES.getlist('images'))
            ])
            
            return redirect('admin:index')
    else:
        form = AddSlidesForm()
    
    context = {
        'title': 'Add Slides Page',
        'form': form,
    }
    
    return render(request, 'add_slides_view.html', context)