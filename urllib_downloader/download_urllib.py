import os
import re
import random
import logging
import urllib.request
import urllib.error
from urllib.parse import quote
from multiprocessing import Pool, current_process, log_to_stderr
from user_agent import generate_user_agent

# @Author: lc
# @Date:   2017-09-25 23:54:24
# @Last Modified by: Koubae
# @Last Modified time: 2020-12-10 16:34:22


####################################################################################################################
# Download images from google with specified keywords for searching
# search query is created by "main_keyword + supplemented_keyword"
# if there are multiple keywords, each main_keyword will join with each supplemented_keyword
# mainly use urllib, and each search query will download at most 100 images due to page source code limited by google
# allow single process or multiple processes for downloading
####################################################################################################################

#  TODO Add CLI command Line. with argparse

log_file = 'trace.log'
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s  %(message)s")

URL_ROOT = 'https://www.google.com/search?q='
URL_END = '&source=lnms&tbm=isch'


def logger(msg, level):
    """Helper function | prints and outputs into a log the download_images that functions process"""
    print(msg, flush=True)
    if level == 'info':
        logging.info(msg)
    elif level == 'warning':
        logging.warning(msg)
    elif level == 'error':
        logging.error(msg)


def downloader(url, process, search=False):
    """Download raw content of the Whole Google Image WebPage or of a URL, depending where the function is called
    Args:
        url (str): url of the page or of a process pic
        process (str): Current Process, used in Multiprocessing, returned from current_process().name
        search (bool): Search Flag, if True it has to download the entire page, if False url is a picture
    Returns:
        raw content of the Webpage or pic's URL
    """

    headers = dict()
    headers['User-Agent'] = generate_user_agent()
    if search:
        headers['Referer'] = 'https://www.google.com'
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        return resp.read()
    except urllib.error.HTTPError as e:
        err =  f'HTTPError while downloading image {url}\nhttp code { e.code}, reason:{e.reason}, process:{process}'
        logger(err, 'warning')
    except urllib.error.URLError as e:
        err = f'URLError while downloading image {url}\nreason:{e.reason}, process:{process}'
        logger(err, 'warning')
    except Exception as e:
        if search:
            err = f'error while downloading page {url} during process:{process}'
            logger(err, 'error')
        else:
            err = f'Unexpected error while downloading {url}\nerror type:{type(e)}, args:{e.args}, process:{process}'
            logger(err, 'error')


def sniff_page(search_url, process):
    """
    Search Whole Google Image WebPage and scans for patterns of src= html attr.
    Args:
        search_url (str): Composed url string pre-compiled to search in Google
        process (str): Current Process, used in Multiprocessing, returned from current_process().name
    Returns:
         set of links if found else empty set
    """
    page_content = downloader(search_url, process=process, search=True)
    page_content = str(page_content)
    if page_content:
        link_list = re.findall('src="(.*?)"', page_content)
        if len(link_list) == 0:
            msg = f'Found 0 links from page {search_url}'
            logger(msg, 'warning')
            return set()
        else:
            return set(link_list)
    else:
        return set()


def gen_dir(download_dir, main_keyword):
    """Helper function | generates a directory where pics will be downloaded, default dir is ./data/"""
    if not download_dir:
        download_dir = './data/'
    img_dir = download_dir + main_keyword + '/'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    return img_dir


def gen_name(count, img_dir):
    """Helper function | Generate (hopefully) unique IDs for any pictures & prevents name collisions"""
    # FAQ if the current picture has the same name os a previously downloaded pic it'll overwrite the old one.
    id_ = str(hex(random.randrange(1000)))
    file_name = id_ + f'_{count}.jpg'
    file_path = img_dir + file_name
    return file_name, file_path


def extract_links(main_keyword, extra_keywords, process):
    """
    Helper function | Feeds the sniff_page function with URLs pre-compiled to be search in Google
    Args:
        main_keyword (str, list): Main Keyword of the search
        extra_keywords (str, list, None): Extra Keywords that are stuck in the search URL like -> %20[extra_keyword]&...
        process (str): Current Process, used in Multiprocessing, returned from current_process().name
    Returns:
        A unique set of Links, if urls aren't found,  return None
    """
    image_links = set()
    if extra_keywords:
        for j in range(len(extra_keywords)):
            msg = f'Process {process} supplemented keyword: {extra_keywords[j]}'
            logger(msg, 'info')
            search_url = URL_ROOT + quote(main_keyword + ' ' + extra_keywords[j]) + URL_END
            print(search_url)
            image_links = image_links.union(sniff_page(search_url, process))
    else:
        msg = f'Process {process} Keyword: {main_keyword}'
        logger(msg, 'info')
        search_url = URL_ROOT + quote(main_keyword) + URL_END
        image_links = image_links.union(sniff_page(search_url, process))
    msg = f'Process {process} get {len(image_links)} links so far'
    logger(msg, 'info')
    return image_links


def download_images(main_keyword, extra_keywords=None, download_dir=None, total=None, download=True):
    """download images with one main keyword and multiple supplemented keywords
    Args:
        main_keyword (str): main keyword
        extra_keywords (list[str], optional): list of supplemented keywords
        download_dir (str, optional): string with ending /, defines the pictures' s download root directory
        total (int, str): Number of picture to be downloaded | default 10 | if total == all it will download all urls
        download (bool): If False, picture won't be downloaded | default True
    Returns:
        None
    """

    process = current_process().name
    msg = f'Process {process} Main keyword: {main_keyword}'
    logger(msg, 'info')

    img_dir = gen_dir(download_dir, main_keyword)
    image_links = extract_links(main_keyword, extra_keywords, process)

    msg = f"Process {process} get totally {len(image_links)} links"
    logger(msg, 'info')

    if not download:
        msg = "==="*15 + " < " + f"Process {process} Terminated" + " > " + "==="*15
        logger(msg, 'info')
        return

    if isinstance(total, str) and str(total.lower()) == 'all':
        total = len(image_links)
    elif not total:
        total = 10

    msg = "==="*15 + " < " + "Start downloading" + " > " + "==="*15
    logger(msg, 'info')

    count = 1  # NOTE: Only used to generate the name of the picture, is quite redundant as we generate a random id.
    limit = 0
    errors = 0
    for link in image_links:
        if limit == total:
            msg = "==="*15 + " < " + f"Process Terminated total {errors} errors" + " > " + "==="*15
            logger(msg, 'info')
            break
        else:
            data = downloader(link, process=process)
            if data:
                file_name, file_path = gen_name(count, img_dir)
                with open(file_path, 'wb') as wf:
                    wf.write(data)
                msg = f'Process {process} downloaded image {main_keyword}/{file_name}'
                logger(msg, 'info')
                count += 1
                limit += 1
            else:
                errors += 1
                continue


def download_manager(main_keywords, extra_keywords=None, download_dir=None,
                     total=None, download=True, multiprocess=False, debug=False):
    """Delegator function |
    Takes care to call download_images for each main_keywords | Args are the same as download_images function"""

    if multiprocess:

        if debug:
            log_to_stderr(logging.DEBUG)
        p = Pool()
        for i in range(len(main_keywords)):
            p.apply_async(download_images, args=(main_keywords[i], extra_keywords, download_dir, total, download))
        p.close()
        p.join()
    else:
        for n in range(len(main_keywords)):
            download_images(main_keywords[n], extra_keywords=extra_keywords,
                            download_dir=download_dir, total=total, download=download)


if __name__ == '__main__':

    main_keywords = ['Pizza']
    supplemented_keywords = ['tomato', 'basil']
    download_manager(main_keywords, extra_keywords=supplemented_keywords, total='all', multiprocess=True, debug=True, download=True)


