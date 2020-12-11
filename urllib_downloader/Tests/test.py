import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from download_urllib import download_manager
import unittest

# ..urllib_downloader.donwload_urllib
class Test(unittest.TestCase):

    def test_one_keyword(self):
        main_keyword = ['neutral']
        download_manager(main_keyword, extra_keywords=None, total=2)

    def test_download_false(self):
        main_keyword = ['neutral']
        download_manager(main_keyword, extra_keywords=None, total=2, download=False)

    def test_custom_dir(self):
        main_keywords = ['pizza', 'pasta']
        extra_k = ['pomodoro', 'salami', 'tuna']
        my_dir = './my_dir/'
        download_manager(main_keywords, extra_keywords=extra_k, download_dir=my_dir, total=2)

    def test_multiprocess(self):
        main_keywords = ['neutral', 'angry']
        supplemented_keywords = ['facial expression', 'people', 'covid', 'world']
        download_manager(main_keywords, extra_keywords=supplemented_keywords, total=10, multiprocess=True, debug=True)

        main_keywords = ['neutral', 'angry', 'surprise', 'disgust', 'fear', 'happy', 'sad']

        supplemented_keywords = ['facial expression', \
                                 'human face', \
                                 'face', \
                                 'old face', \
                                 'young face', \
                                 'adult face', \
                                 'child face', \
                                 'woman face', \
                                 'man face', \
                                 'male face', \
                                 'female face', \
                                 'gentleman face', \
                                 'lady face', \
                                 'boy face', \
                                 'girl face', \
                                 'American face', \
                                 'Chinese face', \
                                 'Korean face', \
                                 'Japanese face', \
                                 'actor face', \
                                 'actress face' \
                                 'doctor face', \
                                 'movie face'
                                 ]
        download_manager(main_keywords, extra_keywords=supplemented_keywords, total='all', multiprocess=True, debug=True)


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)


if __name__ == '__main__':
    run_tests(Test)
