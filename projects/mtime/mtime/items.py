# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ColumnFamily(scrapy.Item):
    family = scrapy.Field()
    row_key = scrapy.Field()


class Table(scrapy.Item):
    table_name = scrapy.Field()


class DetailFamily(ColumnFamily):
    name = scrapy.Field()
    birthday = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    constellation = scrapy.Field()
    blood_group = scrapy.Field()
    edu_background = scrapy.Field()
    biography = scrapy.Field()


    def __init__(self):
        self.family = "detail"


class FilmographiesFamily(ColumnFamily):

    def __init__(self):
        self.family = "Filmographies"


class PhotoFamily(ColumnFamily):

    def __init__(self):
        self.family = "photo"


class VideoFamily(ColumnFamily):

    def __init__(self):
        self.family = "video"


class NewsFamily(ColumnFamily):

    def __init__(self):
        self.family = "news"


class CommentFamily(ColumnFamily):

    def __init__(self):
        self.family = "comment"


class UrlFamily(ColumnFamily):

    details_url = scrapy.Field()
    filmographies_url = scrapy.Field()
    photo_gallery_url = scrapy.Field()
    video_url = scrapy.Field()
    news_url = scrapy.Field()
    comment_url = scrapy.Field()

    def __init__(self):
        self.family = "url"


class PeopleItem(Table):
    # define the fields for your item here like:
    url_family = scrapy.Field()
    detail_family = scrapy.Field()
    filmographies_family = scrapy.Field()
    photo_family = scrapy.Field()
    video_family = scrapy.Field()
    news_family = scrapy.Field()
    comment_family = scrapy.Field()

    def __init__(self):
        self.table_name = "people"
    pass


class KeyNameItem(scrapy.Item):
    key = scrapy.Field()
    name_cn = scrapy.Field()
    name_en = scrapy.Field()