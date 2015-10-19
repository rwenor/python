from django.contrib import admin

from .models import Choice, Question, Mn_Name

from .models import Thing, Part, Ma_Part


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date')
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']
    #list_display = ('question_text', 'pub_date', 'was_published_recently')
	

#class Ma_Part(admin.ModelAdmin):

class PartInline(admin.TabularInline):
    model = Part
    extra = 3

class ThingAdmin(admin.ModelAdmin):
    list_display = ('ma_id', 'thing_desc')
    inlines = [PartInline]



admin.site.register(Question, QuestionAdmin)

admin.site.register(Ma_Part)
admin.site.register(Thing, ThingAdmin)
admin.site.register(Part)
admin.site.register(Mn_Name)

