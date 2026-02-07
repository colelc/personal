import random
import re
from collections import Counter

class AiFilterService(object):
    def __init__(self, N, middle, letters, bad_prefixes, bad_suffixes):
        self.N = N
        self.middle = middle
        self.letters = letters
        self.bad_prefixes = bad_prefixes
        self.bad_suffixes = bad_suffixes
        self.MIN_VOWEL_RATIO = 0.30

        self.BAD_VOWEL_TRIGRAMS = {
            "AOO", "OOI", "IIA", "IAI", "OAO", "AOI",
            "UUA", "UUO", "III"
        }

        self.COMMON_VOWEL_BIGRAMS = {
            "EA", "OU", "IO", "IA", "OI", "AU", "IE"
        }

        self.RARE_VOWEL_BIGRAMS = {
            "OA", "OY", "YI", "YO", "AO"
        }

        self.VOWELS = set("aeiouy")

    def filter(self, word):
        if self.looks_like_word(word.upper()):
            return False
        
        return True
    
    def looks_like_word(self, s):
        return (
            self.has_middle(s)
            and not self.find_consecutive_consonants(s)
            and not self.consonant_count(s)
            and not self.has_consecutive_vowels(s)
            and not self.word_contains(s)
            and not self.starts_with(s)
            and not self.ends_with(s)
        )
    
    def word_contains(self, word):
        values = ("AO", "AE", "IY")
        if any (sub in word for sub in values):
            return True
        
        return False
    
    def starts_with(self, word):
        avoid = set(self.bad_prefixes)
        return word.startswith(tuple(avoid))
        
    def ends_with(self, word):
        avoid = set(self.bad_suffixes)
        return word.endswith(tuple(avoid))
    
    def has_consecutive_vowels(self, word:str) -> bool:
        pattern = re.compile(r"[AEIOUY]{3}|I{2}|U{2}|A{2}|Y{2}", re.IGNORECASE)

        match = pattern.search(word)
        if match:
            #self.logger.info(word + " : contains consecutive vowels")
            return True

        return False
            
    def consonant_count(self, word:str):
        pattern = re.compile(
            r"([BCDFGHJKLMNPQRSTVWXYZ])(?:.*\1){3,}",
            re.IGNORECASE
        )

        match = pattern.search(word)
        if match:
            return True
        
        return False
    
    def find_consecutive_consonants(self, word:str):
        pattern = re.compile(r"[BCDFGHJKLMNPQRSTVWXYZ]{3}|Y{2}|V{2}|H{2}|J{2}|K{2}|W{2}|X{2}", re.IGNORECASE)

        if pattern.search(word):
            #self.logger.info(word + " : Contains 4 consecutive consonants")
            return True

    def has_middle(self, s):
        return self.middle.upper() in s.upper()

