#encoding=utf8
#from scrapyc.server.utils.spider.twistarpiplines import TwistarItem,DBObject,Field
from scrapy.item import Field, Item
# create table shop ( 
#     id BIGINT UNSIGNED not null auto_increment primary key,
#     url VARCHAR(4096) not null,
#     html MEDIUMBLOB,
#     insert_time DATETIME,
#     last_update_time DATETIME

#     )



class ShopItem(Item):
    """docstring for BaiduUserItem"""
    url = Field()
    html = Field()
    insert_time = Field()
    last_update_time= Field()

        
class GoodsItem(Item):
    """docstring for BaiduUserItem"""

    url = Field()
    html = Field()
    insert_time = Field()
    last_update_time= Field()



class IndexItem(Item):
    """docstring for BaiduUserItem"""

    url = Field()
    html = Field()
    insert_time = Field()
    last_update_time= Field()



           
if __name__ == "__main__" :
    import pdb
    pdb.set_trace()
