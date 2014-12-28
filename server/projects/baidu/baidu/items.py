#encoding=utf8
from scrapyc.server.utils.spider.twistarpiplines import TwistarItem
#from sqlalchemy import Column,BigInteger, Integer,TEXT, ForeignKey, String,DateTime,Sequence


# class BaiduUser(AlchemyBase):
#     """docstring for BaiduUser"""
#     __tablename__ = 'baidu_user'
#     uk = Column(BigInteger, Sequence('baidu_user_uk_seq'), primary_key=True)
#     username = Column(String(4096))
#     pubshare_count = Column(BigInteger)
#     secshare_cnt = Column(BigInteger)
#     fans_count = Column(BigInteger)
#     follow_count = Column(BigInteger)
#     intro = Column(TEXT)
#     album_count = Column(BigInteger)
#     tui_user_count = Column(BigInteger)
#     c2c_user_sell_count = Column(BigInteger)
#     c2c_user_buy_count = Column(BigInteger)
#     c2c_user_product_count = Column(BigInteger)
#     avatar_url = Column(String(1024))
#     last_insert_time = Column(DateTime)
#     last_update_time= Column(DateTime)



# class BaiduShare(AlchemyBase):
#     """docstring for BaiduShare"""
#     __tablename__ = 'baidu_share'
#     data_id = Column(String(255), Sequence('baidu_share_id_seq'), primary_key=True)
#     feed_type = Column(String(30))
#     album_id= Column(String(255))
#     shareid = Column(String(255))
#     uk = Column(BigInteger)
#     category = Column(Integer)
#     feed_time = Column(BigInteger)
#     title = Column(String(4096))
#     filecount = Column(Integer)
#     public = Column(Integer)
#     shorturl = Column(String(1024))
#     source_uid = Column(String(255))
#     source_id = Column(String(255))
#     vCnt = Column(BigInteger)
#     dCnt = Column(BigInteger)
#     tCnt = Column(BigInteger)
#     description = Column(TEXT)
#     is_valid =  Column(Integer)
#     last_crawl_time = Column(DateTime)

 
# class BaiduFile(AlchemyBase):
#     __tablename__ = 'baidu_file'
#     fs_id = Column(String(255), Sequence('baidu_file_id_seq'), primary_key=True)
#     uk = Column(BigInteger)
#     shareid = Column(String(255))
#     data_id = Column(String(255))
#     album_id = Column(String(255))
#     server_filename = Column(String(4096))
#     category = Column(Integer)
#     isdir = Column(Integer)
#     size = Column(BigInteger)
#     path = Column(String(2048))
#     md5 = Column(String(255))
#     sign = Column(String(255))
#     shorturl = Column(String(255))
#     is_valid = Column(Integer)
#     last_crawl_time= Column(DateTime)

class BaiduUser(object):
    """docstring for BaiduUser"""
    TABLENAME="baidu_user"
    def __init__(self, arg):
        super(BaiduUser, self).__init__()
        self.arg = arg

class BaiduShare(object):
    """docstring for BaiduUser"""
    TABLENAME="baidu_share"
    def __init__(self, arg):
        super(BaiduUser, self).__init__()
        self.arg = arg

class BaiduFile(object):
    """docstring for BaiduUser"""
    TABLENAME="baidu_file"
    def __init__(self, arg):
        super(BaiduUser, self).__init__()
        self.arg = arg


class BaiduUserItem(TwistarItem):
    """docstring for BaiduUserItem"""
    alchemy_model=BaiduUser

        
class BaiduShareItem(TwistarItem):
    """docstring for BaiduUserItem"""
    alchemy_model=BaiduShare

class BaiduFileItem(TwistarItem):
    """docstring for BaiduUserItem"""
    alchemy_model=BaiduFile





           
if __name__ == "__main__" :
    import pdb
    pdb.set_trace()
