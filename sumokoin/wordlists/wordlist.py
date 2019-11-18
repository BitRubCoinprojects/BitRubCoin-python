#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from binascii import crc32

from six import with_metaclass


WORDLISTS = {}
_log = logging.getLogger(__name__)


class WordlistType(type):
    def __new__(cls, name, bases, attrs):
        if bases:
            if 'language_name' not in attrs:
                raise TypeError("Missing language_name for {0}".format(name))
            if 'unique_prefix_length' not in attrs:
                raise TypeError("Missing 'unique_prefix_length' for {0}".format(name))
            if 'word_list' not in attrs:
                raise TypeError("Missing 'word_list' for {0}".format(name))

            if 'english_language_name' not in attrs:
                _log.warn("No 'english_language_name' for {0} using '{1}'".format(name, language_name))
                attrs['english_language_name'] = attrs['language_name']

            if len(attrs['word_list']) != 1626:
                raise TypeError("Wrong word list length for {0}".format(name))

        new_cls = super(WordlistType, cls).__new__(cls, name, bases, attrs)

        if bases:
            WORDLISTS[new_cls.english_language_name] = new_cls

        return new_cls


class Wordlist(with_metaclass(WordlistType)):
    n = 1626

    @classmethod
    def encode(cls, hex):
        """Convert hexadecimal string to mnemonic word representation with checksum.
        """
        out = []
        for i in range(len(hex) // 8):
            word = endian_swap(hex[8*i:8*i+8])
            x = int(word, 16)
            w1 = x % cls.n
            w2 = (x // cls.n + w1) % cls.n
            w3 = (x // cls.n // cls.n + w2) % cls.n
            out += [cls.word_list[w1], cls.word_list[w2], cls.word_list[w3]]
        checksum = cls.get_checksum(" ".join(out))
        out.append(checksum)
        checksum_2 = cls.get_second_checksum(" ".join(out))
        out.append(checksum_2)
        return " ".join(out)

    @classmethod
    def decode(cls, phrase):
        """Calculate hexadecimal representation of the phrase.
        """
        phrase = phrase.split(" ")
        out = ""
        for i in range(len(phrase) // 3):
            word1, word2, word3 = phrase[3*i:3*i+3]
            w1 = cls.word_list.index(word1)
            w2 = cls.word_list.index(word2) % cls.n
            w3 = cls.word_list.index(word3) % cls.n
            x = w1 + cls.n *((w2 - w1) % cls.n) + cls.n * cls.n * ((w3 - w2) % cls.n)
            out += endian_swap("%08x" % x)
        return out

    @classmethod
    def get_checksum(cls, phrase):
        """Given a mnemonic word string, return a string of the computed checksum.

        :rtype: str
        """
        phrase_split = phrase.split(" ")
        # Standard format
        phrase = phrase_split[:24]
        wstr = "".join(word[:cls.unique_prefix_length] for word in phrase)
        wstr = bytearray(wstr.encode('utf-8'))
        z = ((crc32(wstr) & 0xffffffff) ^ 0xffffffff ) >> 0
        z2 = ((z ^ 0xffffffff) >> 0) % len(phrase)
        return phrase_split[z2]

    @classmethod
    def get_second_checksum(cls, phrase):
        """Given a mnemonic word string + checksum,
        return a string of the computed second checksum.

        :rtype: str
        """
        phrase_split = phrase.split(" ")
        # Standard format + checksum
        phrase = phrase_split[:25]
        wstr = "".join(word[:cls.unique_prefix_length] for word in phrase)
        wstr = bytearray(wstr.encode('utf-8'))
        z = ((crc32(wstr) & 0xffffffff) ^ 0xffffffff ) >> 0
        z2 = ((z ^ 0xffffffff) >> 0) % len(cls.word_list)
        return cls.word_list[z2]


def get_wordlist(name):
    try:
        return WORDLISTS[name]
    except KeyError:
        raise ValueError("No such word list")


def list_wordlists():
    return WORDLISTS.keys()


def endian_swap(word):
    """Given any string, swap bits and return the result.

    :rtype: str
    """
    return "".join([word[i:i+2] for i in [6, 4, 2, 0]])
