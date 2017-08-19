import docx
import getArgs


def _log(string):
    def outter(fun):
        print(string)
        def wrapper(self):
            fun(self)
            print("End")
        return wrapper
    return outter


class WordSub:
    def __init__(self,*,word_file_name,args_file_name):
        self.word_file = docx.Document(word_file_name)
        self.args_file = open(args_file_name,'r',encoding='utf-8')
        self.count = len(self.word_file.paragraphs)

    def __substitute(self):
        pass

    @_log("Start logging")
    def run(self):
        for i in enumerate(self.word_file.paragraphs):
            print("Processing:",i[0],'/',self.count,end="  ")
            print(i[1].text)




if __name__ == "__main__":
    ws = WordSub(word_file_name="华发峰景湾花园电缆采购合同.docx",args_file_name="test.txt")
    ws.run()