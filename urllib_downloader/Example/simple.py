import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from download_urllib import download_manager


# Simple Download
main_keywords = ['Pizza']
download_manager(main_keywords)


main_keywords = ['Car', 'Motorbike']
download_manager(main_keywords, total=3)

main_keywords = ['Car', 'Motorbike']
extra_words = ['red', 'blue', 'green', 'expensive']
download_manager(main_keywords, extra_keywords=extra_words, total=3)