from django.contrib import admin
from .models import Character, Weapon
# , CharacterBanner, WeaponBanner


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
    model = Weapon
    extra = 3

class WeaponBannerAdmin(admin.ModelAdmin):
    pass

class CharacterInline(admin.TabularInline):
    model = Character
    extra = 3

class CharacterBannerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Character, CharacterAdmin)
