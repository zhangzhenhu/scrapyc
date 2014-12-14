from scrapyc.server.utils.sqlalchemyitem import AlchemyBase,AlchemyItem


 class BaiduUser(AlchemyBase):
     """docstring for BaiduUser"""
     __tablename__ = 'baidu_user'
    uk = scrapy.Field()
    username = scrapy.Field()
    pubshare_count = scrapy.Field()
    secshare_cnt = scrapy.Field()
    fans_count = scrapy.Field()
    follow_count = scrapy.Field()
    intro = scrapy.Field()
    album_count = scrapy.Field()
    tui_user_count = scrapy.Field()
    c2c_user_sell_count = scrapy.Field()
    c2c_user_buy_count = scrapy.Field()
    c2c_user_product_count = scrapy.Field()
    avatar_url = scrapy.Field()
    last_insert_time = scrapy.Field()
    last_update_time= scrapy.Field()

     def __init__(self, arg):
         super(BaiduUser, self).__init__()
         self.arg = arg

class BaiduShare(AlchemyBase):
    """docstring for BaiduShare"""
    __tablename__ = 'baidu_share'
    feed_type=scrapy.Field()
    album_id=scrapy.Field()
    shareid = scrapy.Field()
    uk = scrapy.Field()
    data_id = scrapy.Field()
    category = scrapy.Field()
    feed_time = scrapy.Field()
    title = scrapy.Field()
    filecount = scrapy.Field()
    public = scrapy.Field()
    shorturl = scrapy.Field()
    source_uid = scrapy.Field()
    source_id = scrapy.Field()
    vCnt = scrapy.Field()
    dCnt = scrapy.Field()
    tCnt = scrapy.Field()
    description = scrapy.Field()
    is_valid =  scrapy.Field()
    last_crawl_time= scrapy.Field()
    def __init__(self, arg):
        super(BaiduShare, self).__init__()
        self.arg = arg
 
class BaiduFile(AlchemyBase):
    __tablename__ = 'baidu_file'
    fs_id = scrapy.Field()
    uk = scrapy.Field()
    data_id = scrapy.Field()
    album_id = scrapy.Field()
    shareid = scrapy.Field()
    server_filename = scrapy.Field()
    category = scrapy.Field()
    isdir = scrapy.Field()
    size = scrapy.Field()
    path = scrapy.Field()
    md5 = scrapy.Field()
    sign = scrapy.Field()
    shorturl = scrapy.Field()
    is_valid=scrapy.Field()
    last_crawl_time= scrapy.Field()


class BaiduUserItem(AlchemyItem):
    """docstring for BaiduUserItem"""
    alchemy_model=BaiduUser
    def __init__(self, arg):
        super(BaiduUserItem, self).__init__()
        self.arg = arg
        