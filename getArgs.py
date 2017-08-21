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
    for arg_name,content in (line.split("：") for line in file.readlines()):
        result[arg_name]=content.rstrip("\n")

    return result

if __name__ == "__main__":
    for i in getArgs("模板变量.txt").items():
        print(i)