import requests
from bs4 import BeautifulSoup
from test.Param import getinitParam
'''
请求页面返回内容
'''

def getHtml(url,jsessionid=''):
    if jsessionid !=''and '?'in url:
        url=url+"&"+jsessionid
    else:
        url=url+"?"+jsessionid
    r=requests.get(url)
    r.encoding='utf-8'
    text=r.text
    return text.replace("\r\n", "").replace("\n", "").strip()

"""
从网页中读取指定省份列
"""
def read_col(table,init_param):
    row_name=[]
    trs=table.contents
    start_index = -1
    row_index = 0
    for tr in trs:
        # if isinstance(tr,str)==False:
            tds=tr.contents
        # 获取直接子节点td
            if tds[0].string==init_param.get_search_row_text():
                start_index=row_index
            row_index=row_index+1
    if start_index>-1:
        for row_index in range(start_index,len(trs)):
            tr=trs[row_index]
            # if isinstance(tr,str)==False:
            if tr.contents[0].string.isspace():
                break
            row_name.append(tr.contents[0].string)
    return row_name

"""
从网页中读取指定行数据
"""
def read_row(table,init_param):
    arr=[]
    trs=table[0].contents
    for tr in trs:
        # tr=a[i]
        # if isinstance(tr,str)==False:
            tds=tr.contents
            if tds[0].string==init_param.get_search_row_text():
                for col_index in range(len(tds)):
                        if (col_index>init_param.get_start_col()-1):
                            arr.append(tds[col_index].string)
    return arr

"""
从数据库查询结果中读取指定列数据
"""
def read_form_db(init_param):
    arr=[]
    db_config=init_param.get_db_config()
    db_type=db_config.get_dbtype()
    if db_type=='postgresql':
        conn=psycopg2.connect(host=db_config.get_ip(),port=db_config.get_port(),
                              dbname=db_config.get_dbName(),user=db_config.get_username(),
                              pasword=db_config.get_password())
    elif db_type=='mysql':
        conn=mysql.connect(host=db_config.get_ip(),port=db_config.get_port(),
                              dbname=db_config.get_dbName(),user=db_config.get_username(),
                              pasword=db_config.get_password())

    cur=conn.cursor()
    cur.execute(init_param.get_sql().replace("${KEYWORDS}",init_param.get_search_row_text()))
    #fetchall():接收全部的返回结果行.返回多个元组，即返回多条记录(rows),如果没有结果,则返回 ()
    #将返回所有结果，返回二维元组，如(('id','name'),('id','name'))
    rows = cur.fetchall()
    for row in rows:
        try:
            arr.append(row[init_param.get_db_col-1])
        except IndexError as e:
            print("init_param中的db_col设置值超出了查询结果列数")
    cur.close();
    return arr
initParam=getinitParam()
_jsessionid=initParam.get_jsessionid()
_url=initParam.get_url()
html=getHtml(_url,_jsessionid)
soup = BeautifulSoup(html, "html.parser")
table=soup.select('#reportTable')

if len(table)<=0:
    print("无法查找到")
else:
    _col_name=read_col(table,initParam)
    for n in _col_name:
        initParam.set_search_row_text(n)
        if len(_col_name)>0:
            _web_row=read_row(table,initParam)
            _db_row=read_form_db(initParam)
            result=[]
            if len(_web_row)==len(_db_row):
                for x in len(_web_row):
                    try:
                        assert _web_row[x]==_db_row[x]
                    except AssertionError  as e:
                        result.append("【"+initParam.get_search_row_text()+"】请求断言失败，请求返回第"+
                                      str(x+initParam.get_start_col()-1))+"列的值为"+str(_web_row[x])+
                                      "sql值为"+ str(_db_row[x]+'\n')
                if len(result)>0:
                    print("========="+initParam.get_search_row_text()+"行数据不一致"+"=========")
                    print(''.jion(result))
                else:
                    print("【"+initParam.get_search_row_text()+"】数据完全一致")
            else:
               print("【" + initParam.get_search_row_text() + "】网页结果和数据库列数不一致")
        else:
            print("未找到关键字，请检查 initParam.search_row_text 参数是否正确" + initParam.get_search_row_text())




