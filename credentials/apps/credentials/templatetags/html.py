"""
Template tags and helper functions for escaping script tag.
"""

import re

from django import template
from django.template.defaultfilters import date
from django.utils.translation import get_language


register = template.Library()

_ARABIC_NUMERALS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

_ARABIC_MONTHS = {
    "January": "يناير", "February": "فبراير", "March": "مارس",
    "April": "أبريل", "May": "مايو", "June": "يونيو",
    "July": "يوليو", "August": "أغسطس", "September": "سبتمبر",
    "October": "أكتوبر", "November": "نوفمبر", "December": "ديسمبر",
}


@register.filter
def arabic_numerals(value):
    """Translate Western digits and English month names to Arabic (e.g. '15 July 2026' → '١٥ يوليو ٢٠٢٦')."""
    result = str(value)
    for en, ar in _ARABIC_MONTHS.items():
        result = re.sub(en, ar, result, flags=re.IGNORECASE)
    return result.translate(_ARABIC_NUMERALS)


@register.filter(expects_localtime=True, is_safe=False)
def month(value):
    """
    Provides the month from a provided date as a string.

    This is used to work around a bug in the Spanish django month translations.
    See LEARNER-3859 for more details.

    Arguments:
        value (datetime): date to format

    Returns:
        string: A formatted version of the month
    """
    formatted = date(value, "E")

    language = get_language()
    if language and language.split("-")[0].lower() == "es":
        return formatted.lower()

    return formatted
