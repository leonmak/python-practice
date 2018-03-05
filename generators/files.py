import itertools
import os
import requests
import re


def generate_file_names(directory, extension):
    """Generates a sequence of opened files matching a specific extension"""
    return (open(os.path.join(curr_dir, file_name))  # same as yield open(..)
            for curr_dir, dir_names, file_names in os.walk(directory)
            for file_name in file_names
            if file_name.endswith(extension))


def cat_files(files):
    """Takes in an iterable of filenames"""
    return (line    # == yield line
            for fname in files
            for line in fname)


def grep_files(lines, pattern=None):
    """Takes in an iterable of lines"""
    return (line
            for line in lines
            if pattern in line)


def get_links(link):
    """Crawl page for links BFS"""
    links_to_visit = [link]
    while links_to_visit:
        current_link = links_to_visit.pop(0)        # de-queue
        page = requests.get(current_link)
        for url in re.findall('<a href="([^"]+)">', str(page.content)):
            if url[0] == '/':
                url = current_link + url[1:]
            pattern = re.compile('https?')
            if pattern.match(url):
                links_to_visit.append(url)          # enqueue
        yield current_link


if __name__ == '__main__':
    py_files = generate_file_names('.', '.py')
    py_file = cat_files(py_files)
    lines = grep_files(py_file, 'def')
    print(list(lines))

    webpage = get_links('http://example.org')
    first_5_links = itertools.islice(webpage, 5)
    print(list(first_5_links))