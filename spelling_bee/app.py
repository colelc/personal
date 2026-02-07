
import json
import os
import itertools
import sys
import argparse
import time
import urllib.request
from collections import Counter
from src.service.scraper import Scraper
from src.service.filter_service import FilterService
from src.service.ai_filter_service import AiFilterService
from src.service.file_service import FileService
from src.config.config import Config
from src.logging.app_logger import AppLogger

class App(object):

    @classmethod
    def go(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("--known", type=str)
        parser.add_argument("--N", type=int)
        args = parser.parse_args()

        FileService.delete_file("app.log")

        logger = AppLogger.set_up_logger("app.log")
        config = Config.set_up_config(".env")
        data = Scraper(config).scrape()

        word_config = {
            "word_file_path" : os.path.join(config.get("input.data.dir"), config.get("word.file")),
            "pairs": data["pairs"],
            "middle": data["middle"],
            "letters":  data["letters"],
            "max_word_length": int(config.get("max.word.length")) or 9
        }

        endpoint = "https://api.dictionaryapi.dev/api/v2/entries/en/"  #football

        answers = list()

        args_n = int(args.N) 
        known_two = args.known
        known_length = len(known_two)
        N = args_n - known_length if args_n > known_length else 0

        logger.info("known: " + known_two)
        logger.info("N: " + str(N))

        middle = word_config["middle"]
        letters = word_config["letters"]
        logger.info("middle: " + middle)
        logger.info("letters: " + str(letters))

        total_combos = 0
        for combo in itertools.product(letters,  repeat=N):
            total_combos += 1

        logger.info("TOTAL combos: " + str(total_combos))

        input_data_dir = config.get("input.data.dir")

        output_data_dir = config.get("output.data.dir")
        os.makedirs(output_data_dir, exist_ok=True)

        http_lookup_file = config.get("http.lookup.file")
        http_lookup_file_path = os.path.join(output_data_dir, http_lookup_file)
        FileService.delete_file(http_lookup_file_path)

        filter_file = config.get("filter.file")
        filter_file_path = os.path.join(output_data_dir, filter_file)
        FileService.delete_file(filter_file_path)

        prefix_file = config.get("prefix.file")
        prefix_file_path = os.path.join(input_data_dir, prefix_file)
        bad_prefixes = FileService.read_file(prefix_file_path)

        suffix_file = config.get("suffix.file")
        suffix_file_path = os.path.join(input_data_dir, suffix_file)
        bad_suffixes = FileService.read_file(suffix_file_path)

        #filterService = FilterService(N, middle, letters)
        aiFilterService = AiFilterService(N, middle, letters, bad_prefixes, bad_suffixes)

        #  BEGIN MAIN PROCESSING LOOP
        counter = 0
        filtered = 0
        http_lookup = 0

        for combo in itertools.product(letters,  repeat=N):
            counter += 1
            if counter % 1000000 == 0:
                App.totals_update(counter, total_combos, filtered, http_lookup)

            part = "".join(combo)
            word = (known_two +  part).upper()
            if word == "PROPITIATORY":
                logger.info(" -> " + word)
            
            #######
            #word = "PROPITIATORY"
            #######

            #doFilter = filterService.filter(word)
            doFilter = aiFilterService.filter(word)
            if doFilter is True:
                #FileService.append(filter_file_path, word)
                filtered += 1
                ######
                #sys.exit()
                continue
                ########

            url = endpoint + word.lower()
            #url = endpoint + "football"
            logger.info(url)
            headers = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}

            req = urllib.request.Request(url, headers=headers,  method="GET")

            try:
                with urllib.request.urlopen(req) as response:
                    json_string = response.read().decode("UTF-8")
                    payload = json.loads(json_string) #dict
                    logger.info(str(payload))
                    answers.append(word)
            except Exception as e:
                pass
                #logger.error(str(e))
            finally:
                http_lookup += 1
                FileService.append(http_lookup_file_path, word)

            time.sleep(0.5)

        answers.sort()
        logger.info(str(answers))

    @classmethod
    def totals_update(cls, count:int, total_combos:int, filtered:int, http_lookup:int) -> None:

        pct = (count / total_combos) * 100
        rounded = round(pct, 2)
        print(\
            str(count) + " of " + str(total_combos) + " (" + str(rounded) + "%)" + ": " \
            + " filtered: " + str(filtered) + " http lookups: " + str(http_lookup) \
            )
                
App.go()