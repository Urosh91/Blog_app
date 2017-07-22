import datetime
import re
import math

from django.utils.html import strip_tags


def count_words(html_data):
    string = strip_tags(html_data)
    words = re.findall(r'\w+', string)
    word_count = len(words)
    return word_count


def read_time(html_data):
    word_count = count_words(html_data)
    read_time_in_minutes = math.ceil(word_count/200)  # 200 words per minute
    # read_time_in_seconds = read_time_in_minutes * 60
    read_time_total = str(datetime.timedelta(minutes=read_time_in_minutes))
    return read_time_total
