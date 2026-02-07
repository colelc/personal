import os
import csv
import stat
import json
from src.logging.app_logger import AppLogger

class FileService(object):

    @staticmethod
    def read_file(filename:str):
        entries = []
        with open(filename, "r", encoding="utf-8") as f:
            entries = [line.strip() for line in f]

        return entries

    @staticmethod
    def append(filename:str, obj):
        with open(filename, "a") as f:
            f.write(obj + "\n")

    @staticmethod
    def file_exists(filename:str) -> bool:
        #logger = AppLogger.get_logger()
        if os.path.exists(filename):
            #logger.info(filename + " exists")
            return True
        
        #logger.info(filename  + " does not exist")
        return False
    
    @staticmethod
    def write_file(filename:str, obj):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(obj))

    @staticmethod
    def delete_file(filename):
        if os.path.exists(filename):
            try:
                # Clear read-only flag (Windows)
                os.chmod(filename, stat.S_IWRITE)
                os.remove(filename)
                #print(f"Deleted {filename}")
            except PermissionError:
                print(f"Permission denied: {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")
            # else:
            #     print(f"Still exists: {filename}")
        #else:
        #    print(filename + " does not exist")
