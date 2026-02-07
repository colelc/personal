import os
import re
from itertools import groupby
from src.logging.app_logger import AppLogger

class FilterService(object):
    def __init__(self, N, middle, letters):
        self.logger = AppLogger.get_logger()
        self.N = N
        self.middle = middle
        self.letters = letters


    def filter(self, word):
        if not word.__contains__(self.middle):
            #logger.info(word + " skip")
            return True

        if self.find_consecutive_consonants(word):
            #logger.info(word + " skip")
            return True

        if self.has_consecutive_vowels(word):
            #logger.info(word + " skip")
            return True
        
        if self.word_contains(word):
            return True
        
        if self.starts_with(word):
            return True
        
        if self.ends_with(word):
            return True
        
        #if self.consonant_count(word):
        #    return True
        
        #if self.letter_counts(word):
        #    return True
        
        #if self.ends_with(word):
        #    return True

    def word_contains(self, word):
        values = ("AO", "AE", "IY")
        if any (sub in word for sub in values):
            return True
        
        return False
    
    def starts_with(self, word):
        prefixes = set(["TC", "PC", "CP", "CC", "RR", "PP", "TT", "CI", "PTO", "AOT", "RPI", "AOI", "TAO", "RAO", "PROY"])
        return word.startswith(tuple(prefixes))
        
    def ends_with(self, word):
        suffixes = set(["TR", "TC", "PC", "CP", "CC", "RR", "PP", "TT", "CI", "TI", "OI", "RI", "ROP", "CRO", "PTO", "TIR", "RIT", "ROT", "IOT", "AOT", "RPI", "AO", "AOR", "AOC", "AOP", "AOI", "RAI", "PAI", "TAI", "AI", "CAI", "CAO", "PAO", "TAO", "RAO"])
        #last_two = word[-2:]
        #if last_two in suffixes:
        return word.endswith(tuple(suffixes))
        
    def letter_counts(self, word):
        distinct_letters = set(word)
        count = len(distinct_letters)
        if count <= 5:
            return True
        
        return False

    def find_consecutive_consonants(self, word:str):
        pattern = re.compile(r"[BCDFGHJKLMNPQRSTVWXYZ]{3}", re.IGNORECASE)

        if pattern.search(word):
            #self.logger.info(word + " : Contains 4 consecutive consonants")
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


    def has_consecutive_vowels(self, word:str) -> bool:
        pattern = re.compile(r"[AEIOU]{3}|I{2}", re.IGNORECASE)

        match = pattern.search(word)
        if match:
            #self.logger.info(word + " : contains consecutive vowels")
            return True

        return False
            

