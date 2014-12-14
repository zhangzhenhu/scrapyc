from scrapyc.server.utils.sqlalchemyitem import AlchemyBase,AlchemyItem


 class BaiduUser(AlchemyBase):
     """docstring for BaiduUser"""
     __tablename__ = 'baidu_user'
    uk = Column(Integer, Sequence('baidu_user_uk_seq'), primary_key=True)
    username = Column(String(255))
    pubshare_count = Column(Integer)
    secshare_cnt = Column(Integer)
    fans_count = Column(Integer)
    follow_count = Column(Integer)
    intro = Column(String)
    album_count = Column(Integer)
    tui_user_count = Column(Integer)
    c2c_user_sell_count = Column(Integer)
    c2c_user_buy_count = Column(Integer)
    c2c_user_product_count = Column(Integer)
    avatar_url = Column(String(1024))
    last_insert_time = Column(DateTime)
    last_update_time= Column(DateTime)



class BaiduShare(AlchemyBase):
    """docstring for BaiduShare"""
    __tablename__ = 'baidu_share'
    data_id = Column(String(255), Sequence('baidu_share_id_seq'), primary_key=True)
    feed_type = Column(String(30))
    album_id= Column(String(255))
    shareid = Column(String(255))
    uk = Column(Integer)
    category = Column(Integer)
    feed_time = Column(Integer)
    title = Column(String(1024))
    filecount = Column(Integer)
    public = Column(Integer)
    shorturl = Column(String(1024))
    source_uid = Column(String(255))
    source_id = Column(String(255))
    vCnt = Column(Integer)
    dCnt = Column(Integer)
    tCnt = Column(Integer)
    description = Column(String)
    is_valid =  Column(Integer)
    last_crawl_time = Column(DateTime)

 
class BaiduFile(AlchemyBase):
    __tablename__ = 'baidu_file'
    fs_id = Column(String(255), Sequence('baidu_file_id_seq'), primary_key=True)
    uk = Column(Integer)
    shareid = Column(String(255))
    data_id = Column(String(255))
    album_id = Column(String(255))
    server_filename = Column(String)
    category = Column(Integer)
    isdir = Column(Integer)
    size = Column(Integer)
    path = Column(String)
    md5 = Column(String(255))
    sign = Column(String(255))
    shorturl = Column(String(255))
    is_valid = Column(Integer)
    last_crawl_time= Column(DateTime)


class BaiduUserItem(AlchemyItem):
    """docstring for BaiduUserItem"""
    alchemy_model=BaiduUser
    def __init__(self, arg=None):
        super(BaiduUserItem, self).__init__()
        self.arg = arg
        
class BaiduShareItem(AlchemyItem):
    """docstring for BaiduUserItem"""
    alchemy_model=BaiduShare
    def __init__(self, arg=None):
        super(BaiduShareItem, self).__init__()
        self.arg = arg

class BaiduFileItem(AlchemyItem):
    """docstring for BaiduUserItem"""
    alchemy_model=BaiduFile
    def __init__(self, arg=None):
        super(BaiduFileItem, self).__init__()
        self.arg = arg                