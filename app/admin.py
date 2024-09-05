from django.contrib import admin

from .models import QuizQuestion, Category, Contact, FAQ

# Register your models here.

admin.site.register(QuizQuestion)
admin.site.register(Contact)
admin.site.register(FAQ)
admin.site.register(Category)
