import docx
import datetime
import getArgs


def _log(string):
    def outter(fun):
        with open(r"C:\Users\Administrator\Documents\WordLog.txt",'a') as f:
            f.write(str(datetime.datetime.now())+"  -> "+string+"\n")
        def wrapper(self):
            fun(self)
            print("End")
        return wrapper
    return outter


class WordSub:
    def __init__(self,*,word_file_name,out_file_name):
        self.word_file = docx.Document(word_file_name)
        self.out_file_name = out_file_name
        self.count = len(self.word_file.paragraphs)


    def __substitute(self,var):
        lst = getArgs.getArgs("模板变量.txt")
        if var.strip("{}") not in lst.keys():
            raise Exception("请查看一下是否变量名称错误->"+var)
        return lst[var.strip("{}")]

    @_log("Start logging")
    def run(self):
        for num,para in enumerate(self.word_file.paragraphs):
            print("Processing:",num,'/',self.count,end="  ")
            global var
            global inStr
            var = ""
            inStr = False
            for r in para.runs:
                if r.text.startswith("{") and not r.text.endswith("}"):
                    inStr=True
                    var+=r.text
                    r.text=""
                elif inStr and not r.text.endswith("}"):
                    var+=r.text
                    r.text=""
                elif inStr and r.text.endswith("}"):
                    var+=r.text
                    r.text=self.__substitute(var)
                    inStr = False
                    var = ""
                elif r.text.startswith("{") and r.text.endswith("}"):
                    r.text = self.__substitute(r.text)
            print()

        # Update the tables
        for table in self.word_file.tables:
            var = ""
            inStr = False
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        for r in para.runs:
                            if r.text.startswith("{") and not r.text.endswith("}"):
                                inStr = True
                                var += r.text
                                r.text = ""
                            elif inStr and not r.text.endswith("}"):
                                var += r.text
                                r.text = ""
                            elif inStr and r.text.endswith("}"):
                                var += r.text
                                r.text = self.__substitute(var)
                                inStr = False
                                var = ""
                            elif r.text.startswith("{") and r.text.endswith("}"):
                                r.text = self.__substitute(r.text)
        self.word_file.save(self.out_file_name)




if __name__ == "__main__":
    pro_name = getArgs.getArgs("模板变量.txt")["项目名称"]
    wb = WordSub(word_file_name="{项目名称}电缆采购合同模板.docx", out_file_name = pro_name + "电缆采购合同.docx")
    ws = WordSub(word_file_name="{项目名称}电缆销售合同模板.docx", out_file_name = pro_name + "电缆销售合同.docx")
    wc = WordSub(word_file_name="{项目名称}电缆协作合同模板.docx", out_file_name = pro_name + "电缆协作合同.docx")
    ws.run()
    wb.run()
    wc.run()