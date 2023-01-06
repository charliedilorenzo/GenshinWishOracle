from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_character_rateups(rateups):
    # TODO actually implement
    pass
    # if len(rateups < 4):
    #     raise ValidationError(
    #         _('%(rateups)s has too few Characters'),
    #         params={'rateups': rateups},
    #     )
    # elif len(rateups > 4):
    #     raise ValidationError(
    #         _('%(rateups)s has too many Characters'),
    #         params={'rateups': rateups},
    #     )
    
