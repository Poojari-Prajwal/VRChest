from django.contrib import admin
from .models import Feedback, Appointment, Gallery_Image, Review, Article

# Register your models here.
admin.site.register(Feedback)
admin.site.register(Appointment)
admin.site.register(Gallery_Image)
admin.site.register(Review)
admin.site.register(Article)