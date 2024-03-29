from django.contrib import admin
from . import models
from django.contrib.admin import widgets

class ManyToManyAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        kwargs['widget']= widgets.FilteredSelectMultiple(
            db_field.verbose_name,
            db_field.name in self.filter_vertical
        )

        return super(admin.ModelAdmin, self).formfield_for_manytomany(
            db_field, request=request, **kwargs)

class WeaponAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Rarity', {'fields': [
         'rarity']}),
        ('Limited', {'fields': [
         'limited']}),
    ]
    list_display = ('name', 'rarity', 'limited')
    list_filter = ['name', 'limited']
    search_fields = ['name']

class CharacterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Rarity', {'fields': [
         'rarity']}),
        ('Limited', {'fields': [
         'limited']}),
    ]
    list_display = ('name', 'rarity', 'limited')
    list_filter = ['name', 'limited']
    search_fields = ['name']



class WeaponInline(admin.TabularInline):
    model = models.Weapon
    extra = 3

class WeaponBannerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['name']}),
        ('Rateups', {'fields': [
         'rateups']}),
        ('End Date', {'fields': [
         'enddate']}),
    ]
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']


class CharacterInline(admin.TabularInline):
    model = models.Character
    extra = 3

class CharacterBannerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['name']}),
        ('Rateups', {'fields': [
         'rateups']}),
        ('End Date', {'fields': [
         'enddate']}),
    ]
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        kwargs['widget']= widgets.FilteredSelectMultiple(
            db_field.verbose_name,
            db_field.name in self.filter_vertical
        )

        return super(admin.ModelAdmin, self).formfield_for_manytomany(
            db_field, request=request, **kwargs)

class CharacterBannerAdmin(ManyToManyAdmin):
    fieldsets = [
        ('Name', {'fields': ['name']}),
        ('Rateups', {'fields': [
         'rateups']}),
        ('End Date', {'fields': [
         'enddate']}),
    ]
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']

class WeaponBanner(ManyToManyAdmin):
    model = models.WeaponBanner

class CharacterBanner(admin.TabularInline):
    model = models.CharacterBanner

admin.site.register(models.Weapon, WeaponAdmin)
admin.site.register(models.Character, CharacterAdmin)
admin.site.register(models.CharacterBanner, CharacterBannerAdmin)
admin.site.register(models.WeaponBanner, WeaponBannerAdmin)
