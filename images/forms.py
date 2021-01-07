from django import forms
from .models import ImagePost
from django.utils.text import slugify
from urllib import request as req
from django.core.files.base import ContentFile


class ImagePostForm(forms.ModelForm):
    
    class Meta:
        model = ImagePost
        fields = ['title', 'description', 'url']
        widgets= {'url': forms.HiddenInput}

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extension = ['jpg', 'jpeg']
        url_extension = url.rsplit('.', 1)[1].lower()
        if url_extension not in valid_extension:
            raise forms.ValidationError("The given url does not match a valid image extension")
        else:
            return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image_obj = super().save(commit=False)
        image_url = self.cleaned_data['url']
        filename = slugify(image_obj.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        full_filename = "{0}.{1}".format(filename, extension)

        # Download Image 
        response = req.urlopen(image_url)
        image_obj.image.save(full_filename, ContentFile(response.read()), save=False)
        if commit:
            image_obj.save()
        return image_obj
    
