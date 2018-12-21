'''
数据库配置
'''
class DBconfigure(object):
    def __init__(self,db_type,ip,port,db_name,username,password):
        self.dbtype=db_type
        self.ip=ip
        self.port=port
        self.dbName=db_name
        self.username=username
        self.password=password

        def get_dbtype(self):
            return self.dbtype

        def get_ip(self):
            return self.ip

        def get_port(self):
            return self.port

        def get_dbName(self):
            return self.dbName

        def get_username(self):
            return self.username

        def get_password(self):
            return self.password

'''
需要对比范围配置类
'''
class Compar(object):
    def __init__(self,db_config,url,jsessionid,row_text,start_col,sql,db_col):
        #数据库配置
        self.dbConfig=db_config
        #获取url地址
        self.url=url
        #请求网页时需要追加的会话ID
        self.jsessionid=jsessionid
        #搜索关键词
        self.rowtext=row_text
        #开始对比列数
        self.startcol=start_col
        #查询SQL语句
        self.sql=sql
        #查询结果对比列索引值
        self.dbcol=db_col

        def get_db_config(self):
            return self.dbConfig

        def set_db_config(self,db_config):
            self.dbConfig=db_config

        def get_url(self):
            return self.url

        def get_search_row_text(self):
            return self.rowtext

        def set_search_row_text(self,row_text):
            self.rowtext=row_text

        def get_start_col(self):
            return self.startcol

        def get_sql(self):
            return self.sql

        def get_db_col(self):
            return self.dbcol

        def get_jsessionid(self):
            return self.jsessionid

def getinitParam():
    db_config=DBconfigure('postgresql', "172.25.2.9", 5432, 'db_bjzhpt0328', 'dev', '6789@jkl')
    param=Compar( db_config,"http://172.25.16.41:8081/bjzhpt/form/32b20edd7da574988028ad422aefaadf/insert", "JSESSIONID=TAS80811s4do0yf31337mqq56t6kvz8b.TAS8081", "合计",
            2, "SELECT mkmc,total FROM db_sjsb_jdryxx.szgl_jdryjbxx('2018','01','${KEYWORDS}') t(mkmc VARCHAR,total NUMERIC )", 2)
    return param