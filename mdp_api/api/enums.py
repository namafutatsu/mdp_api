from django.utils.translation import ugettext_lazy as _

CURRENCY_CAD = 'CAD'
CURRENCY_CHF = 'CHF'
CURRENCY_DKK = 'DKK'
CURRENCY_EUR = 'EUR'
CURRENCY_GBP = 'GBP'
CURRENCY_NOK = 'NOK'
CURRENCY_RUB = 'RUB'
CURRENCY_SEK = 'SEK'
CURRENCY_USD = 'USD'

CURRENCY_CHOICES = (
    (CURRENCY_CAD, _("Canadian Dollars ($)")),
    (CURRENCY_CHF, _("Swiss Francs (CHF)")),
    (CURRENCY_DKK, _("Danish Krone (kr)")),
    (CURRENCY_EUR, _("Euros (€)")),
    (CURRENCY_GBP, _("British pound (£)")),
    (CURRENCY_NOK, _("Norwegian Krone (kr)")),
    (CURRENCY_RUB, _("Russian ruble (₽)")),
    (CURRENCY_SEK, _("Swedish Krona (kr)")),
    (CURRENCY_USD, _("US Dollars ($)")),
)

EVENT_FORMAT_SHORT = 'short'
EVENT_FORMAT_MEDIUM = 'medium'
EVENT_FORMAT_LONG = 'long'

EVENT_FORMAT_CHOICES = (
    (EVENT_FORMAT_SHORT, _("Less than 24 hours")),
    (EVENT_FORMAT_MEDIUM, _("Two to three days")),
    (EVENT_FORMAT_LONG, _("More than three days")),
)

EVENT_TAG_BEGINNER_FRIENDLY = 'beginner_friendly'
EVENT_TAG_INTERNATIONAL = 'international'
EVENT_TAG_PWD_FRIENDLY = 'pwd_friendly'
EVENT_TAG_UNDERAGE_FRIENDLY = 'underage_friendly'

EVENT_TAG_CHOICES = (
    (EVENT_TAG_BEGINNER_FRIENDLY, _("Beginner friendly")),
    (EVENT_TAG_INTERNATIONAL, _("International")),
    (EVENT_TAG_PWD_FRIENDLY, _("PWD friendly")),
    (EVENT_TAG_UNDERAGE_FRIENDLY, _("Underage friendly")),
)

EVENT_TAG_DICT = {key: value for (key, value) in EVENT_TAG_CHOICES}

LANGUAGE_CHOICES = (
    ('af', _("Afrikanns")),
    ('ar', _("Arabic")),
    ('bg', _("Bulgarian")),
    ('bn', _("Bengali")),
    ('bo', _("Tibetan")),
    ('ca', _("Catalan")),
    ('cs', _("Czech")),
    ('cy', _("Welsh")),
    ('da', _("Danish")),
    ('de', _("German")),
    ('el', _("Greek")),
    ('en', _("English")),
    ('es', _("Spanish")),
    ('et', _("Estonian")),
    ('eu', _("Basque")),
    ('fa', _("Persian")),
    ('fi', _("Finnish")),
    ('fj', _("Fiji")),
    ('fr', _("French")),
    ('ga', _("Irish")),
    ('gu', _("Gujarati")),
    ('he', _("Hebrew")),
    ('hi', _("Hindi")),
    ('hr', _("Croation")),
    ('hu', _("Hungarian")),
    ('hy', _("Armenian")),
    ('id', _("Indonesian")),
    ('is', _("Icelandic")),
    ('it', _("Italian")),
    ('ja', _("Japanese")),
    ('jw', _("Javanese")),
    ('ka', _("Georgian")),
    ('km', _("Cambodian")),
    ('ko', _("Korean")),
    ('la', _("Latin")),
    ('lt', _("Lithuanian")),
    ('lv', _("Latvian")),
    ('mi', _("Maori")),
    ('mk', _("Macedonian")),
    ('ml', _("Malayalam")),
    ('mn', _("Mongolian")),
    ('mr', _("Marathi")),
    ('ms', _("Malay")),
    ('mt', _("Maltese")),
    ('ne', _("Nepali")),
    ('nl', _("Dutch")),
    ('no', _("Norwegian")),
    ('pa', _("Punjabi")),
    ('pl', _("Polish")),
    ('pt', _("Portuguese")),
    ('qu', _("Quechua")),
    ('ro', _("Romanian")),
    ('ru', _("Russian")),
    ('sk', _("Slovak")),
    ('sl', _("Slovenian")),
    ('sm', _("Samoan")),
    ('sq', _("Albanian")),
    ('sr', _("Serbian")),
    ('sv', _("Swedish ")),
    ('sw', _("Swahili")),
    ('ta', _("Tamil")),
    ('te', _("Telugu")),
    ('th', _("Thai")),
    ('to', _("Tonga")),
    ('tr', _("Turkish")),
    ('tt', _("Tatar")),
    ('uk', _("Ukranian")),
    ('ur', _("Urdu")),
    ('uz', _("Uzbek")),
    ('vi', _("Vietnamese")),
    ('xh', _("Xhosa")),
    ('zh', _("Chinese (Mandarin")),
)

LANGUAGES_DICT = {key: value for (key, value) in LANGUAGE_CHOICES}
