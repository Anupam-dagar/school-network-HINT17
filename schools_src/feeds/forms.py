from django import forms

from .models import Photo, Feed


class PhotoForm(forms.ModelForm): 
    class Meta:
        model = Photo
        fields = ('file',)

class FeedForm(forms.ModelForm):
	class Meta:
		model = Feed 
		fields = ('post','post_pic')

	def __init__(self, *args, **kwargs):
		super(FeedForm, self).__init__(*args, **kwargs)
		self.fields['post_pic'].required = False

