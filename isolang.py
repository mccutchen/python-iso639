#!/usr/bin/env python

__all__ = ['langs']


class LangDb(dict):
    """A customized dict in which ISO 639-1 language codes are mapped to their
    English and native language names.

    By default, language codes are mapped to their primary native language
    names (i.e., if you use normal dict methods, you'll be dealing with native
    language names).

    English names for languages and alternative names (if applicable) are also
    accessible via special methods.

    Some examples (with dummy data):

    	>>> langs = LangDb({
        ... u'en': (u'English', u'English'),
        ... u'de': (u'German', u'Deutsche'),
        ... u'fr': (u'French', (u'fran\xe7ais', u'langue fran\xe7aise')),
        ... u'gd': ((u'Scottish Gaelic', u' Gaelic'), u'G\xe0idhlig')
        ... })
        >>> langs
        <LangDb: 4 langs>

        # Accessing by key returns primary native name
        >>> langs['en']
        u'English'
        >>> langs['fr']
        u'fran\xe7ais'
        >>> langs['gd']
        u'G\xe0idhlig'
        >>> langs['de']
        u'Deutsche'

        # All the normal dict protocol methods are there, and they all deal
        # with primary native names.
        >>> langs.get('en')
        u'English'
        >>> langs.get('fr')
        u'fran\xe7ais'
        >>> sorted(langs.items())
        [(u'de', u'Deutsche'), (u'en', u'English'), (u'fr', u'fran\xe7ais'), (u'gd', u'G\xe0idhlig')]
        >>> sorted(langs.keys())
        [u'de', u'en', u'fr', u'gd']
        >>> sorted(langs.values())
        [u'Deutsche', u'English', u'G\xe0idhlig', u'fran\xe7ais']

        # You can also explicitly ask for the native name
        >>> langs.native_name('en')
        u'English'
        >>> langs.native_name('fr')
        u'fran\xe7ais'

        # Asking for all names will always return a tuple, even if there is
        # only one name
        >>> langs.native_name('fr', all_names=True)
        (u'fran\xe7ais', u'langue fran\xe7aise')
        >>> langs.native_name('de', all_names=True)
        (u'Deutsche',)

        >>> langs.english_name('fr')
        u'French'
        >>> langs.english_name('gd')
        u'Scottish Gaelic'
        >>> langs.english_name('gd', all_names=True)
        (u'Scottish Gaelic', u' Gaelic')

        # And access iterators over the available language codes or names
        # (these are basically synonyms for iterkeys() and itervalues()
        >>> sorted(langs.codes)
        [u'de', u'en', u'fr', u'gd']
        >>> sorted(langs.names)
        [u'Deutsche', u'English', u'G\xe0idhlig', u'fran\xe7ais']
    """

    ENGLISH = 0
    NATIVE = 1

    # Normal dict protocol
    def __getitem__(self, key):
        """By default, accessing the db by language code will return the
        native language name."""
        english, native = super(LangDb, self).__getitem__(key)
        return native if isinstance(native, basestring) else native[0]

    def get(self, *args, **kwargs):
        value = super(LangDb, self).get(*args, **kwargs)
        try:
            english, native = value
            return primary(native)
        except TypeError:
            return value

    def iteritems(self):
        """An iterator over (code, primary native name) pairs."""
        for code, (english, native) in super(LangDb, self).iteritems():
            yield code, primary(native)

    def items(self):
        """A list of (code, primary native name) pairs."""
        return list(self.iteritems())

    def itervalues(self):
        return (primary(native) for english, native
                in super(LangDb, self).itervalues())

    def values(self):
        return list(self.itervalues())

    # Special LangDb properties and methods
    @property
    def codes(self):
        """An iterator over the language codes in the database."""
        return self.iterkeys()

    @property
    def names(self):
        """An iterator over the primary native names for the languages in the
        database."""
        return self.itervalues()

    @property
    def native_names(self):
        """An iterator over (code, native name) pairs."""
        for code, (english, native) in super(LangDb, self).iteritems():
            yield code, primary(native)

    @property
    def english_names(self):
        """An iterator over (code, English name) pairs."""
        for code, (english, native) in super(LangDb, self).iteritems():
            yield code, primary(english)

    def native_name(self, code, all_names=False):
        """Returns the native name for the given language code.  If all_names
        is True, returns a tuple of all the possible native names."""
        return self._some_name(code, self.NATIVE, all_names)

    def english_name(self, code, all_names=False):
        """Returns the English name for the given language code. If all_names
        is True, returns a tuple of all the possible English names."""
        return self._some_name(code, self.ENGLISH, all_names)

    def _some_name(self, code, which, all_names):
        """Utility function to pull an English or native name (or all names)
        from the db by language code.  Used by native_name() and
        english_name()."""
        value = super(LangDb, self).__getitem__(code)
        if value is None:
            raise KeyError, code
        name = value[which]
        if not all_names:
            return primary(name)
        else:
            return name if isinstance(name, tuple) else (name,)

    def raw_data(self):
        """Provide access to a copy of the raw underlying data."""
        return dict(super(LangDb, self).iteritems())

    def __repr__(self):
        return '<LangDb: %d langs>' % len(self)


def primary(names):
    """Returns the primary name from names, which can be a string or a tuple
    of strings.  If it's a string, it is returned.  If it's a tuple, the first
    element is returned.

    	>>> primary('French')
        'French'
        >>> primary(('Alpha', 'Beta'))
        'Alpha'

        >>> primary('Alpha')
        'Alpha'
        >>> primary(('Alpha', 'Beta'))
        'Alpha'
        >>> primary(None)
        Traceback (most recent call last):
        ...
        TypeError: 'NoneType' object is unsubscriptable
    """
    return names if isinstance(names, basestring) else names[0]


# Maps two-letter language codes to (english name, native name) tuples, where
# either name may be a single string or a list of strings.
langs = LangDb({
    u'aa': (u'Afar', u'Afaraf'),
    u'ab': (u'Abkhaz', u'\u0410\u04a7\u0441\u0443\u0430'),
    u'ae': (u'Avestan', u'avesta'),
    u'af': (u'Afrikaans', u'Afrikaans'),
    u'ak': (u'Akan', u'Akan'),
    u'am': (u'Amharic', u'\u12a0\u121b\u122d\u129b'),
    u'an': (u'Aragonese', u'Aragon\xe9s'),
    u'ar': (u'Arabic', u'\u0627\u0644\u0639\u0631\u0628\u064a\u0629'),
    u'as': (u'Assamese', u'\u0985\u09b8\u09ae\u09c0\u09af\u09bc\u09be'),
    u'av': (u'Avaric',
            (u'\u0430\u0432\u0430\u0440 \u043c\u0430\u0446\u04c0',
             u'\u043c\u0430\u0433\u04c0\u0430\u0440\u0443\u043b \u043c\u0430\u0446\u04c0')),
    u'ay': (u'Aymara', u'aymar aru'),
    u'az': (u'Azerbaijani', u'az\u0259rbaycan dili'),
    u'ba': (u'Bashkir',
            u'\u0431\u0430\u0448\u04a1\u043e\u0440\u0442 \u0442\u0435\u043b\u0435'),
    u'be': (u'Belarusian',
            u'\u0411\u0435\u043b\u0430\u0440\u0443\u0441\u043a\u0430\u044f'),
    u'bg': (u'Bulgarian',
            u'\u0431\u044a\u043b\u0433\u0430\u0440\u0441\u043a\u0438 \u0435\u0437\u0438\u043a'),
    u'bh': (u'Bihari', u'\u092d\u094b\u091c\u092a\u0941\u0930\u0940'),
    u'bi': (u'Bislama', u'Bislama'),
    u'bm': (u'Bambara', u'bamanankan'),
    u'bn': (u'Bengali', u'\u09ac\u09be\u0982\u09b2\u09be'),
    u'bo': ((u'Tibetan Standard', u'Tibetan', u'Central'),
            u'\u0f56\u0f7c\u0f51\u0f0b\u0f61\u0f72\u0f42'),
    u'br': (u'Breton', u'brezhoneg'),
    u'bs': (u'Bosnian', u'bosanski jezik'),
    u'ca': ((u'Catalan', u' Valencian'), u'Catal\xe0'),
    u'ce': (u'Chechen',
            u'\u043d\u043e\u0445\u0447\u0438\u0439\u043d \u043c\u043e\u0442\u0442'),
    u'ch': (u'Chamorro', u'Chamoru'),
    u'co': (u'Corsican', (u'corsu', u'lingua corsa')),
    u'cr': (u'Cree', u'\u14c0\u1426\u1403\u152d\u140d\u140f\u1423'),
    u'cs': (u'Czech', (u'\u010desky', u'\u010de\u0161tina')),
    u'cu': ((u'Old Church Slavonic',
             u'Church Slavic',
             u'Church Slavonic',
             u'Old Bulgarian',
             u'Old Slavonic'),
            u'\u0469\u0437\u044b\u043a\u044a \u0441\u043b\u043e\u0432\u0463\u043d\u044c\u0441\u043a\u044a'),
    u'cv': (u'Chuvash',
            u'\u0447\u04d1\u0432\u0430\u0448 \u0447\u04d7\u043b\u0445\u0438'),
    u'cy': (u'Welsh', u'Cymraeg'),
    u'da': (u'Danish', u'dansk'),
    u'de': (u'German', u'Deutsch'),
    u'dv': ((u'Divehi', u' Dhivehi', u' Maldivian', u''),
            u'\u078b\u07a8\u0788\u07ac\u0780\u07a8'),
    u'dz': (u'Dzongkha', u'\u0f62\u0fab\u0f7c\u0f44\u0f0b\u0f41'),
    u'ee': (u'Ewe', u'E\u028begbe'),
    u'el': (u'Greek',
            u'\u0395\u03bb\u03bb\u03b7\u03bd\u03b9\u03ba\u03ac'),
    u'en': (u'English', u'English'),
    u'eo': (u'Esperanto', u'Esperanto'),
    u'es': ((u'Spanish', u' Castilian'), (u'espa\xf1ol', u'castellano')),
    u'et': (u'Estonian', (u'eesti', u'eesti keel')),
    u'eu': (u'Basque', (u'euskara', u'euskera')),
    u'fa': (u'Persian', u'\u0641\u0627\u0631\u0633\u06cc'),
    u'ff': ((u'Fula', u' Fulah', u' Pulaar', u' Pular'),
            (u'Fulfulde', u'Pulaar', u'Pular')),
    u'fi': (u'Finnish', (u'suomi', u'suomen kieli')),
    u'fj': (u'Fijian', u'vosa Vakaviti'),
    u'fo': (u'Faroese', u'f\xf8royskt'),
    u'fr': (u'French', (u'fran\xe7ais', u'langue fran\xe7aise')),
    u'fy': (u'Western Frisian', u'Frysk'),
    u'ga': (u'Irish', u'Gaeilge'),
    u'gd': ((u'Scottish Gaelic', u' Gaelic'), u'G\xe0idhlig'),
    u'gl': (u'Galician', u'Galego'),
    u'gn': (u'Guaran\xed', u"Ava\xf1e'\u1ebd"),
    u'gu': (u'Gujarati', u'\u0a97\u0ac1\u0a9c\u0ab0\u0abe\u0aa4\u0ac0'),
    u'gv': (u'Manx', (u'Gaelg', u'Gailck')),
    u'ha': (u'Hausa', (u'Hausa', u'\u0647\u064e\u0648\u064f\u0633\u064e')),
    u'he': (u'Hebrew ', u'\u05e2\u05d1\u05e8\u05d9\u05ea'),
    u'hi': (u'Hindi',
            (u'\u0939\u093f\u0928\u094d\u0926\u0940',
             u'\u0939\u093f\u0902\u0926\u0940')),
    u'ho': (u'Hiri Motu', u'Hiri Motu'),
    u'hr': (u'Croatian', u'hrvatski'),
    u'ht': ((u'Haitian', u' Haitian Creole'), u'Krey\xf2l ayisyen'),
    u'hu': (u'Hungarian', u'Magyar'),
    u'hy': (u'Armenian', u'\u0540\u0561\u0575\u0565\u0580\u0565\u0576'),
    u'hz': (u'Herero', u'Otjiherero'),
    u'ia': (u'Interlingua', u'Interlingua'),
    u'id': (u'Indonesian', u'Bahasa Indonesia'),
    u'ie': (u'Interlingue',
            (u'Originally called Occidental', u' then Interlingue after WWII')),
    u'ig': (u'Igbo', u'As\u1ee5s\u1ee5 Igbo'),
    u'ii': (u'Nuosu', u'\ua188\ua320\ua4bf Nuosuhxop'),
    u'ik': (u'Inupiaq', (u'I\xf1upiaq', u'I\xf1upiatun')),
    u'io': (u'Ido', u'Ido'),
    u'is': (u'Icelandic', u'\xcdslenska'),
    u'it': (u'Italian', u'Italiano'),
    u'iu': (u'Inuktitut', u'\u1403\u14c4\u1483\u144e\u1450\u1466'),
    u'ja': (u'Japanese', u'\u65e5\u672c\u8a9e '),
    u'jv': (u'Javanese', u'basa Jawa'),
    u'ka': (u'Georgian', u'\u10e5\u10d0\u10e0\u10d7\u10e3\u10da\u10d8'),
    u'kg': (u'Kongo', u'KiKongo'),
    u'ki': ((u'Kikuyu', u'Gikuyu'), u'G\u0129k\u0169y\u0169'),
    u'kj': ((u'Kwanyama', u'Kuanyama'), u'Kuanyama'),
    u'kk': (u'Kazakh',
            u'\u049a\u0430\u0437\u0430\u049b \u0442\u0456\u043b\u0456'),
    u'kl': ((u'Kalaallisut', u'Greenlandic'),
            (u'kalaallisut', u'kalaallit oqaasii')),
    u'km': (u'Khmer', u'\u1797\u17b6\u179f\u17b6\u1781\u17d2\u1798\u17c2\u179a'),
    u'kn': (u'Kannada', u'\u0c95\u0ca8\u0ccd\u0ca8\u0ca1'),
    u'ko': (u'Korean', (u'\ud55c\uad6d\uc5b4 ', u'\uc870\uc120\ub9d0 ')),
    u'kr': (u'Kanuri', u'Kanuri'),
    u'ks': (u'Kashmiri',
            (u'\u0915\u0936\u094d\u092e\u0940\u0930\u0940',
             u'\u0643\u0634\u0645\u064a\u0631\u064a\u200e')),
    u'ku': (u'Kurdish', (u'Kurd\xee', u'\u0643\u0648\u0631\u062f\u06cc\u200e')),
    u'kv': (u'Komi', u'\u043a\u043e\u043c\u0438 \u043a\u044b\u0432'),
    u'kw': (u'Cornish', u'Kernewek'),
    u'ky': ((u'Kirghiz', u'Kyrgyz'),
            u'\u043a\u044b\u0440\u0433\u044b\u0437 \u0442\u0438\u043b\u0438'),
    u'la': (u'Latin', (u'latine', u'lingua latina')),
    u'lb': ((u'Luxembourgish', u'Letzeburgesch'), u'L\xebtzebuergesch'),
    u'lg': (u'Luganda', u'Luganda'),
    u'li': ((u'Limburgish', u'Limburgan', u'Limburger'), u'Limburgs'),
    u'ln': (u'Lingala', u'Ling\xe1la'),
    u'lo': (u'Lao', u'\u0e9e\u0eb2\u0eaa\u0eb2\u0ea5\u0eb2\u0ea7'),
    u'lt': (u'Lithuanian', u'lietuvi\u0173 kalba'),
    u'lu': (u'Luba-Katanga', u'Luba-Katanga'),
    u'lv': (u'Latvian', u'latvie\u0161u valoda'),
    u'mg': (u'Malagasy', u'Malagasy fiteny'),
    u'mh': (u'Marshallese', u'Kajin M\u0327aje\u013c'),
    u'mi': (u'M\u0101ori', u'te reo M\u0101ori'),
    u'mk': (u'Macedonian',
            u'\u043c\u0430\u043a\u0435\u0434\u043e\u043d\u0441\u043a\u0438 \u0458\u0430\u0437\u0438\u043a'),
    u'ml': (u'Malayalam', u'\u0d2e\u0d32\u0d2f\u0d3e\u0d33\u0d02'),
    u'mn': (u'Mongolian', u'\u041c\u043e\u043d\u0433\u043e\u043b'),
    u'mr': (u'Marathi', u'\u092e\u0930\u093e\u0920\u0940'),
    u'ms': (u'Malay',
            (u'bahasa Melayu',
             u'\u0628\u0647\u0627\u0633 \u0645\u0644\u0627\u064a\u0648\u200e')),
    u'mt': (u'Maltese', u'Malti'),
    u'my': (u'Burmese', u'\u1017\u1019\u102c\u1005\u102c'),
    u'na': (u'Nauru', u'Ekakair\u0169 Naoero'),
    u'nb': (u'Norwegian Bokm\xe5l', u'Norsk bokm\xe5l'),
    u'nd': (u'North Ndebele', u'isiNdebele'),
    u'ne': (u'Nepali', u'\u0928\u0947\u092a\u093e\u0932\u0940'),
    u'ng': (u'Ndonga', u'Owambo'),
    u'nl': (u'Dutch', (u'Nederlands', u'Vlaams')),
    u'nn': (u'Norwegian Nynorsk', u'Norsk nynorsk'),
    u'no': (u'Norwegian', u'Norsk'),
    u'nr': (u'South Ndebele', u'isiNdebele'),
    u'nv': ((u'Navajo', u'Navaho'),
            (u'Din\xe9 bizaad', u'Din\xe9k\u02bceh\u01f0\xed')),
    u'ny': ((u'Chichewa', u' Chewa', u' Nyanja'),
            (u'chiChe\u0175a', u'chinyanja')),
    u'oc': (u'Occitan ', u'Occitan'),
    u'oj': (u'Ojibwa', u'\u140a\u14c2\u1511\u14c8\u142f\u14a7\u140e\u14d0'),
    u'om': (u'Oromo', u'Afaan Oromoo'),
    u'or': (u'Oriya', u'\u0b13\u0b21\u0b3c\u0b3f\u0b06'),
    u'os': ((u'Ossetian', u'Ossetic'),
            u'\u0418\u0440\u043e\u043d \xe6\u0432\u0437\u0430\u0433'),
    u'pa': ((u'Panjabi', u'Punjabi'),
            (u'\u0a2a\u0a70\u0a1c\u0a3e\u0a2c\u0a40',
             u'\u067e\u0646\u062c\u0627\u0628\u06cc\u200e')),
    u'pi': (u'P\u0101li', u'\u092a\u093e\u0934\u093f'),
    u'pl': (u'Polish', u'polski'),
    u'ps': ((u'Pashto', u'Pushto'), u'\u067e\u069a\u062a\u0648'),
    u'pt': (u'Portuguese', u'Portugu\xeas'),
    u'qu': (u'Quechua', (u'Runa Simi', u'Kichwa')),
    u'rm': (u'Romansh', u'rumantsch grischun'),
    u'rn': (u'Kirundi', u'kiRundi'),
    u'ro': ((u'Romanian', u'Moldavian', u'Moldovan'), u'rom\xe2n\u0103'),
    u'ru': (u'Russian',
            u'\u0420\u0443\u0441\u0441\u043a\u0438\u0439 \u044f\u0437\u044b\u043a'),
    u'rw': (u'Kinyarwanda', u'Ikinyarwanda'),
    u'sa': (u'Sanskrit',
            u'\u0938\u0902\u0938\u094d\u0915\u0943\u0924\u092e\u094d'),
    u'sc': (u'Sardinian', u'sardu'),
    u'sd': (u'Sindhi',
            (u'\u0938\u093f\u0928\u094d\u0927\u0940',
             u'\u0633\u0646\u068c\u064a\u060c \u0633\u0646\u062f\u06be\u06cc\u200e')),
    u'se': (u'Northern Sami', u'Davvis\xe1megiella'),
    u'sg': (u'Sango', u'y\xe2ng\xe2 t\xee s\xe4ng\xf6'),
    u'si': ((u'Sinhala', u'Sinhalese'), u'\u0dc3\u0dd2\u0d82\u0dc4\u0dbd'),
    u'sk': (u'Slovak', u'sloven\u010dina'),
    u'sl': (u'Slovene', u'sloven\u0161\u010dina'),
    u'sm': (u'Samoan', u"gagana fa'a Samoa"),
    u'sn': (u'Shona', u'chiShona'),
    u'so': (u'Somali', (u'Soomaaliga', u'af Soomaali')),
    u'sq': (u'Albanian', u'Shqip'),
    u'sr': (u'Serbian',
            u'\u0441\u0440\u043f\u0441\u043a\u0438 \u0458\u0435\u0437\u0438\u043a'),
    u'ss': (u'Swati', u'SiSwati'),
    u'st': (u'Southern Sotho', u'Sesotho'),
    u'su': (u'Sundanese', u'Basa Sunda'),
    u'sv': (u'Swedish', u'svenska'),
    u'sw': (u'Swahili', u'Kiswahili'),
    u'ta': (u'Tamil', u'\u0ba4\u0bae\u0bbf\u0bb4\u0bcd'),
    u'te': (u'Telugu', u'\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41'),
    u'tg': (u'Tajik',
            (u'\u0442\u043e\u04b7\u0438\u043a\u04e3',
             u'to\u011fik\u012b',
             u'\u062a\u0627\u062c\u06cc\u06a9\u06cc\u200e')),
    u'th': (u'Thai', u'\u0e44\u0e17\u0e22'),
    u'ti': (u'Tigrinya', u'\u1275\u130d\u122d\u129b'),
    u'tk': (u'Turkmen',
            (u'T\xfcrkmen', u'\u0422\u04af\u0440\u043a\u043c\u0435\u043d')),
    u'tl': (u'Tagalog',
            (u'Wikang Tagalog',
             u'\u170f\u1712\u1703\u1705\u1714 \u1706\u1704\u170e\u1713\u1704\u1714')),
    u'tn': (u'Tswana', u'Setswana'),
    u'to': (u'Tonga ', u'faka Tonga'),
    u'tr': (u'Turkish', u'T\xfcrk\xe7e'),
    u'ts': (u'Tsonga', u'Xitsonga'),
    u'tt': (u'Tatar',
            (u'\u0442\u0430\u0442\u0430\u0440\u0447\u0430',
             u'tatar\xe7a',
             u'\u062a\u0627\u062a\u0627\u0631\u0686\u0627\u200e')),
    u'tw': (u'Twi', u'Twi'),
    u'ty': (u'Tahitian', u'Reo M\u0101`ohi'),
    u'ug': ((u'Uighur', u'Uyghur'),
            (u'Uy\u01a3urq\u0259',
             u'\u0626\u06c7\u064a\u063a\u06c7\u0631\u0686\u06d5\u200e')),
    u'uk': (u'Ukrainian',
            u'\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430'),
    u'ur': (u'Urdu', u'\u0627\u0631\u062f\u0648'),
    u'uz': (u'Uzbek',
            (u"O'zbek",
             u'\u040e\u0437\u0431\u0435\u043a',
             u'\u0623\u06c7\u0632\u0628\u06d0\u0643\u200e')),
    u've': (u'Venda', u'Tshiven\u1e13a'),
    u'vi': (u'Vietnamese', u'Ti\u1ebfng Vi\u1ec7t'),
    u'vo': (u'Volap\xfck', u'Volap\xfck'),
    u'wa': (u'Walloon', u'Walon'),
    u'wo': (u'Wolof', u'Wollof'),
    u'xh': (u'Xhosa', u'isiXhosa'),
    u'yi': (u'Yiddish', u'\u05d9\u05d9\u05b4\u05d3\u05d9\u05e9'),
    u'yo': (u'Yoruba', u'Yor\xf9b\xe1'),
    u'za': ((u'Zhuang', u'Chuang'), (u'Sa\u026f cue\u014b\u0185', u'Saw cuengh')),
    u'zh': (u'Chinese', (u'\u4e2d\u6587 ', u'\u6c49\u8bed', u'\u6f22\u8a9e')),
    u'zu': (u'Zulu', u'isiZulu')
})

if __name__ == '__main__':
    import doctest
    #doctest.testmod()

    def p(x):
        if isinstance(x, basestring):
            return "u'%s'" % x
        else:
            xs = ["u'%s'" % s for s in x]
            return '(%s)' % ','.join(xs)

    for c, (e, n) in langs.raw_data().items():
        print '%r: (%s, %s),' % (c, p(e), p(n))

