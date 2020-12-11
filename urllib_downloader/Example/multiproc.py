import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from download_urllib import download_manager


main_keywords = ['neutral', 'angry', 'surprise', 'disgust', 'fear', 'happy', 'sad']

supplemented_keywords = ['facial expression',
                         'human face',
                         'face',
                         'old face',
                         'young face',
                         'adult face',
                         'child face',
                         'woman face',
                         'man face',
                         'male face',
                         'female face',
                         'gentleman face',
                         'lady face',
                         'boy face',
                         'girl face',
                         'American face',
                         'Chinese face',
                         'Korean face',
                         'Japanese face',
                         'actor face',
                         'actress face'
                         'doctor face',
                         'movie face'
                         ]

if __name__ == '__main__':
    # Multiprocess
    keywords = ['Car', 'Motorbike']
    extra__words = ['red', 'blue', 'green', 'expensive']
    download_manager(keywords, extra_keywords=extra__words, total=3, multiprocess=True)
    download_manager(main_keywords, extra_keywords=supplemented_keywords, total=10,
                     multiprocess=True, debug=True, download_dir='.new_dir/')

