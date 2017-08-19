def getExplain():
    '''
    The args file should be like this:
    <arg_name>:<content>
    <arg_name>:<content>
    :return: doc
    '''

    return getExplain.__doc__

def getArgs(file_name:str):
    file = open(file_name,'r',encoding='utf-8')
    result ={}
    for arg_name,content in (line.split("：") for line in file.readlines()):
        result[arg_name]=content

    return result

if __name__ == "__main__":
    pass