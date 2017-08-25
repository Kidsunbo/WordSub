import datetime
import os


def getExplain():
    '''
    The args file should be like this:
    <arg_name>:<content>
    <arg_name>:<content>
    :return: doc
    '''

    return getExplain.__doc__

def getArgs(file_name:str):
    file = open(file_name,'r')
    result ={}
    for arg_name,content in (line.split("：",1) for line in file.readlines() if not line.strip().startswith("#") if line.strip('\n')):
        result[arg_name]=content.rstrip("\n")

    # add the annual information
    result.update(__annualVariable())

    # add the Sale Agreement year,month and day
    __addSellYMD(result)

    # add the supplier information
    __addCompanyInfo(result)

    # check the price
    __checkPrice(result)

    return result


def __addCompanyInfo(lst):
    global supplier
    if "供方名称" in lst:
        supplier = lst["供方名称"]
    else:
        raise Exception("不知道供方的名称")

    supplier_location = "./供应商/"+supplier+".txt"

    with open(supplier_location,'r') as supplier_file:
    	def __innerReplace(content:str):
    		

        for arg_name, content in (line.split("：",1) for line in supplier_file.readlines() if not line.strip().startswith("#") if
                                  line.strip('\n')):
            content = content.replace("{到货期限}",lst["到货期限"])
            lst[arg_name] = content.replace("\n","")

def __addSellYMD(lst):
    global y
    global m
    global d
    
    if '年' not in lst.keys() or '月' not in lst.keys() or '日' not in lst.keys()  :
        now = datetime.datetime.now()
        y = now.year
        m = now.month
        d = now.day
        lst['年']=str(y)
        lst['月']='0'+str(m) if len(str(m))==1 else str(m)
        lst['日']='0'+str(d) if len(str(d))==1 else str(d)
    else:
        y = int(lst['年'].lstrip('0'))
        m = int(lst['月'].lstrip('0'))
        d = int(lst['日'].lstrip('0'))
    dt = datetime.datetime(y,m,d)
    dt += datetime.timedelta(days = 3)
    lst['销售年']=str(dt.year)
    lst['销售月']='0'+str(dt.month) if len(str(dt.month))==1 else str(dt.month)
    lst['销售日']='0'+str(dt.day) if len(str(dt.day))==1 else str(dt.day)

def __checkPrice(lst):
    b = float(lst['采购小写金额'].replace(',',""))
    s = float(lst['销售小写金额'].replace(',',""))
    if not 1.06<s/b<1.08:
        raise Exception("审核一下金额")

def __annualVariable():
    lst = {}
    if os.path.exists("./战略协议/战略相关变量.txt"):
        f = open("./战略协议/战略相关变量.txt",'r')
        for arg_name, content in (line.split("：",1) for line in f.readlines() if not line.strip().startswith("#") if
                                  line.strip('\n')):
            lst[arg_name] = content.rstrip("\n")
        f.close()
        if lst["是否续签"] == "是":
            lst["续签情况"] = "续"
        else:
            lst["续签情况"]=""
        return lst
    else:
        raise Exception("请提供战略协议的相关信息")


if __name__ == "__main__":
    for i in getArgs("项目相关变量.txt").items():
        print(i)
