from collections import namedtuple
from datetime import date
from time import mktime

import feedparser

FEED = 'http://projects.bobbelderbos.com/pcc/all.rss.xml'

Entry = namedtuple('Entry', 'date title link tags')


def _convert_struct_time_to_dt(stime):
    """Convert a time.struct_time as returned by feedparser into a
    datetime.date object, so:
    time.struct_time(tm_year=2016, tm_mon=12, tm_mday=28, ...)
    -> date(2016, 12, 28)"""
    return date.fromtimestamp(mktime(stime))


def get_feed_entries(feed=FEED):
    """Use feedparser to parse PyBites RSS feed.
       Return a list of Entry namedtuples (date = date, drop time part)"""
    parser = feedparser.parse(feed)
    return [Entry(_convert_struct_time_to_dt(entry.published_parsed), entry.title, entry.link,
                    [t.term.lower() for t in entry.tags]) for entry in parser['entries']]


def filter_entries_by_tag(search, entry):
    """Check if search matches any tags as stored in the Entry namedtuple
       (case insensitive, only whole, not partial string matches).
       Returns bool: True if match, False if not.
       Supported searches:
       1. If & in search do AND match,
          e.g. flask&api should match entries with both tags
       2. Elif | in search do an OR match,
          e.g. flask|django should match entries with either tag
       3. Else: match if search is in tags"""
    intersect = 1
    if '&' in search:
        search = set(search.lower().split('&'))
        intersect = len(search)
    elif '|' in search:
        search = set(search.lower().split('|'))
    else:
        search = {search.lower()}

    return len(set(entry.tags) & search) >= intersect


def main():
    """Entry point to the program
       1. Call get_feed_entries and store them in entries
       2. Initiate an infinite loop
       3. Ask user for a search term, exit on 'q', try again upon empty input
       4. Filter/match the entries (see filter_entries_by_tag docstring)
       5. Print the date+title+link of each match ordered by date desc
       6. Secondly, print the number of matches"""

    entries = sorted(get_feed_entries(), key = lambda x: x.date)

    while True:
        srch_str = input()
        if srch_str.lower() == 'q':
            print('Bye')
            break
        if srch_str == '':
            print('Please provide a search term')
            continue
        matches = 0
        for e in entries:
            if filter_entries_by_tag(srch_str, e):
                print(e.title)
                matches += 1
        print(f'{matches} {"entry" if matches == 1 else "entries"} matched')

    pass


if __name__ == '__main__':
    main()
