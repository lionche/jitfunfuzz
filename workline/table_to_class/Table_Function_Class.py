import itertools
import math
import re
import subprocess
import sys
import tempfile
import time

from dbConnecttion.Table_Operation import Table_Testcase
from workline.assemble_tools.callable_processor import CallableProcessor


class Function_Object(object):

    def __init__(self, function_object):
        self.Id = function_object.get('id')
        self.Function_content: str = str(function_object.get('Function_content'), 'utf-8')
        self.SourceFun_id = function_object.get('SourceFun_id')
        self.Mutation_method = function_object.get('Mutation_method')
        self.Mutation_times = function_object.get('Mutation_times')
        self.Remark = function_object.get('Remark')
        # self.js_line_count = self.getJSfileSize(self.Function_content, 10)
        # self.var_line_count = self.count_var_lines(self.Function_content)
        # self.prefix_list = self.prefixList()

    def __str__(self):
        return str(self.Function_content)

    #     def count_var_lines(self, code: str):
    #         """
    #         数一数包含var的最后一行是第几行
    #         :param file_path: 文件的地址
    #         :return: 最后一个var的行数,也就是前缀的行数
    #         """
    #         regex = r'function.*\n( {4}"use strict";\n)?( {4}var.*\n)*'
    #
    #         matches = re.finditer(regex, code, re.MULTILINE)
    #
    #         count = 0
    #         for matchNum, match in enumerate(matches, start=1):
    #             # print(match.group(0))
    #
    #             for line in match.group(0).splitlines():
    #                 count = count + 1
    #         return count
    #
    #     def getJSfileSize(self, code: str, cut_max_line: int) -> int:
    #         lines_list = code.splitlines()
    #         return min(len(lines_list), cut_max_line)
    #
    #     def prefixList(self):
    #         prefix_list = []
    #         for prefix_line in range(self.var_line_count, self.js_line_count):
    #             # 获取到了前缀
    #             function_prefix = self.getPrefix(self.Function_Content, prefix_line)
    #             prefix_list.append(function_prefix)
    #         return prefix_list
    #
    #         # Function_content, SourceFun_id, Mutation_method, Remark
    #
    #     def gpt_replace_block(self, prefix_line, function):
    #
    #         orginal_block_list = self.analysis_js_block(self.Function_Content)
    #         # print(orginal_block_list)
    #         gpt_block_list = self.analysis_js_block(function)
    #         # print(gpt_block_list)
    #
    #         block_num = self.fineBlockIdx(gpt_block_list, prefix_line + 1)
    #
    #         # 当前块不是最后一个块的话
    #         # if block_num != len(gpt_block_list):
    #         # 使用当前代码块替换掉对应的代码块
    #         try:
    #             # print('原用例')
    #             # for block in orginal_block_list:
    #             #     print(block)
    #             #     print("-"*50)
    #             #
    #             # print('GPT用例')
    #             # for block in gpt_block_list:
    #             #     print(block)
    #             #     print("-"*50)
    #
    #             orginal_block_list_copy = orginal_block_list.copy()
    #
    #             orginal_block_list_copy[block_num - 1] = gpt_block_list[block_num - 1]
    #
    #             # print('替换后')
    #             # for block in orginal_block_list_copy:
    #             #     print(block)
    #             #     print("-"*50)
    #
    #             code_string = ''
    #             for block in orginal_block_list_copy:
    #                 code_string += block
    #             return code_string + '\n'
    #         except:
    #             pass
    #
    #     def getPrefix(self, code: str, cut_line: int):
    #         lines_list = code.splitlines(True)
    #         line_list_cut = lines_list[0:cut_line]
    #         function_cut = ''
    #         for i in line_list_cut:
    #             function_cut += i
    #         # print(function_cut)
    #         # print('--')
    #         return function_cut
    #
    #     def fineBlockIdx(self, gpt_block_list, gpt_line_num):
    #         """替换代码块
    #         :param orginal_block_list: 原文件的代码块
    #         :param gpt_block_list: gpt生成文件的代码块
    #         :param gpt_line_num: gpt开始续写的第一行代码
    #         :return:当前代码块
    #         """
    #
    #         block_count = 0
    #         line_count = 0
    #
    #         for idx, block in enumerate(gpt_block_list):
    #             line_count = len(block.splitlines()) + line_count
    #
    #             # print(block, line_count)
    #
    #             if gpt_line_num <= line_count:
    #                 block_count = idx
    #                 break
    #
    #         return block_count + 1
    #
    #     def analysis_js_block(self, code) -> list:
    #         """
    #         正则匹配代码块
    #         :param test_str: 代码源文件
    #         :return:
    #         """
    #         block_list = []
    #         regex = r'(^ {4})([^} ].*)([^;]$)\n(.*\n)*? {4}}((\))?)(;?)$\n|^ {4}\w+.*;$\n|function.*\n|^}| {4}"use strict"\n;| {4}for.*{}\n'
    #         matches = re.finditer(regex, code, re.MULTILINE)
    #         for matchNum, match in enumerate(matches, start=1):
    #             block_list.append(match.group())
    #         return block_list
    #
    #     def gpt_mutation_3(self, sess):
    #         """
    #         变量替换
    #         :return:
    #         """
    #         print("2.正在使用变量替换变异")
    #         start_time = time.time()
    #
    #         Function_Content_line_list = self.Function_Content.splitlines(True)
    #
    #         var_number = self.countVarNumber(Function_Content_line_list)
    #         if var_number:
    #             # 使用function的第一行来作为生成的前缀
    #             all_functions = self.function_generate(Function_Content_line_list[0], sess)
    #
    #             # 包含所有相同前缀提取出来的值得set
    #             varSet = []
    #             for function in all_functions:
    #                 # print(function)
    #                 # print("-" * 100)
    #                 for line in function.splitlines():
    #                     value = self.getVar(line)
    #                     if value:
    #                         varSet.append(value)
    #
    #                         if len(varSet) > 10:
    #                             varSet = varSet[:10]
    #
    #             varSet = set(varSet)
    #
    #             all_functions_replace_block_pass = set()
    #
    #             if varSet:
    #                 # print(f'生成的变量定义{varSet}进行替换')
    #                 if var_number < 5:
    #                     code_list = self.ReplacevalueStatement(Function_Content_line_list, varSet, var_number)
    #
    #                     all_functions_replace_block_pass = self.jshint_check_function(code_list)
    #
    #                     function_list_to_write = makeFunctionListToWrite(
    #                         all_functions=all_functions_replace_block_pass,
    #                         SourceFun_id=self.Id,
    #                         mutation_type=3,
    #                         mutation_times=0,
    #                         Remark=None)
    #
    #                     write_to_Table_function(function_list_to_write)
    #
    #             end_time = time.time()
    #
    #             print(
    #                 f"生成了{len(all_functions_replace_block_pass)}个GPT变量替换用例，总耗时{int(end_time - start_time)}秒.")
    #
    #         else:
    #             print(f'用例{self.Id}没有变量定义，跳过变量替换变异')
    #
    #     def ReplacevalueStatement(self, test_str_line_list, valset, var_number):
    #         """
    #         正则匹配代码块,替换value值
    #         :param test_str_line_list: 代码源文件line_list
    #         :param valset: 生成的变量的字典
    #         :param var_number: 变量的数量
    #         :return:
    #         """
    #
    #         replaceLineDictList = []
    #
    #         valsetList = list(valset)
    #
    #         iterTimes = var_number
    #
    #         iterPlan = set()
    #
    #         for c in itertools.permutations(valsetList, iterTimes):
    #             iterPlan.add(c)
    #
    #         for c in itertools.combinations_with_replacement(valsetList, iterTimes):
    #             iterPlan.add(c)
    #
    #         for item in iterPlan:
    #             # print(item)
    #             # 生成迭代器，
    #             item_iter = iter(item)
    #
    #             regex = r'^ {4}var \S+ = \S+;\n'
    #             replaceLineDict = {}
    #             for old_value_statement_idx, line in enumerate(test_str_line_list):
    #                 # matches = re.finditer(regex, line, re.MULTILINE)
    #                 matches = re.search(regex, line, re.MULTILINE)
    #                 if matches:
    #                     old_value_statement = matches.group()
    #                     # 获得下一个值:
    #                     valset_Choice = next(item_iter)
    #                     value = old_value_statement.split('= ')[1].split(';')[0]
    #
    #                     new_value_statement = old_value_statement.replace(value, valset_Choice)
    #
    #                     replaceLineDict[old_value_statement_idx] = new_value_statement
    #
    #             replaceLineDictList.append(replaceLineDict)
    #             # print(replaceLineDictList)
    #
    #         codeList = []
    #         if replaceLineDictList:
    #             for replaceLineDict in replaceLineDictList:
    #                 # print(replaceLineDict)
    #                 test_str_line_list_copy = self.replaceLine(test_str_line_list, replaceLineDict)
    #                 code_string = ''
    #                 for block in test_str_line_list_copy:
    #                     code_string = code_string + block
    #                 codeList.append(code_string)
    #                 # return code_string
    #
    #         return codeList
    #
    #     def getVar(self, line):
    #         """
    #         正则匹配代码块,判断是否是赋值语句
    #         :param test_str_line_list: 代码源文件line_list
    #         :return:
    #         """
    #         # regex = r'^ {4}var .* = .*;$'
    #         regex = r'^ {4}var \S+ = \S+;'
    #
    #         matches = re.search(regex, line, re.MULTILINE)
    #         if matches:
    #             # print(line)
    #             old_value_statement = matches.group()
    #             value = old_value_statement.split('= ')[1].split(';')[0]
    #             return value
    #
    #     def countVarNumber(self, test_str_line_list):
    #         """
    #         正则匹配代码块,计算变量个数
    #         :param test_str_line_list: 代码源文件line_list
    #         :return:
    #         """
    #
    #         regex = r'^ {4}var \S+ = \S+;\n'
    #
    #         count = 0
    #
    #         for old_value_statement_idx, line in enumerate(test_str_line_list):
    #             # matches = re.finditer(regex, line, re.MULTILINE)
    #             matches = re.search(regex, line, re.MULTILINE)
    #             if matches:
    #                 count = count + 1
    #         return count
    #
    #     def replaceLine(self, test_str_line_list, replaceLineDict):
    #         test_str_line_list_copy = test_str_line_list.copy()
    #         for old_value_statement_idx, new_value_statement in replaceLineDict.items():
    #             test_str_line_list_copy[old_value_statement_idx] = new_value_statement
    #         return test_str_line_list_copy
    #
    def makeTestcasesListToWrite(self, all_testcases, SourceFun_id, SourceTestcase_id=0, Fuzzing_times=0,
                                 Mutation_method=0, Mutation_times=0, Interesting_times=0, engine_coverage=None,
                                 Engine_coverage_integration_source=None, Engine_coverage_integration_all=None,
                                 Probability=0,
                                 Remark=None) -> list:
        # 将生成的代码写入数据库

        lis = []

        for testcase in all_testcases:
            Testcases_content = testcase
            item = [Testcases_content, SourceFun_id, SourceTestcase_id, Fuzzing_times, Mutation_method,
                    Mutation_times, Interesting_times, engine_coverage,
                    Engine_coverage_integration_source, Engine_coverage_integration_all, Probability, Remark]
            lis.append(item)
        return lis

    def jshint_check_function(self, all_functions):
        """
        使用jshint对生成的用例进行检查\n
        过滤掉语法错误的用例\n
        保留正确的，再用于替换代码块变异\n
        去掉用例中最后一行的print
        :param all_functions: 所有方法的list
        :return:
        """
        start_time = time.time()
        # print("正在对生成的用例使用jshint进行语法检查")
        all_testcases_pass = set()
        for testcase in all_functions:
            # 通过with语句创建临时文件，with会自动关闭临时文件
            testcase_no_print = testcase[:testcase.rfind('\n')]
            testcase_no_print = testcase_no_print[:testcase_no_print.rfind('\n')]
            # print(testcase_no_print)

            with tempfile.NamedTemporaryFile(delete=True) as tmpfile:
                temp_file_path = tmpfile.name
                # print(temp_file_name)  # /tmp/tmp73zl8gmn
                tmpfile.write(testcase_no_print.encode())
                tmpfile.seek(0)
                # tmpTxt = tmpfile.read().decode()
                # print(tmpTxt)
                result = self.cmd_jshint(temp_file_path)
                if result:
                    all_testcases_pass.add(testcase)

        end_time = time.time()

        # print(
        #     f"共组装了{len(all_testcases)}个用例，其中语法正确的用例共{len(all_testcases_pass)}个，检测总耗时{int(end_time - start_time)}秒.")
        return all_testcases_pass

    def cmd_jshint(self, temp_file_path):
        """
        使用jshint对生成的function进行检查\n
        :param temp_file_path: 临时文件位置
        :return: 语法正确返回true,语法错误返回false
        """
        # cmd = ['timeout', '60s', 'jshint', temp_file_path]
        cmd = ['timeout', '60s', 'jshint', '-c', '/root/fuzzopt/data/.jshintrc', temp_file_path]
        if sys.platform.startswith('win'):  # 假如是windows
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        else:  # 假如是linux
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if stdout:
            print("stdout")
            print(stdout)
        if stderr:
            print("error")
            print(stderr)
        if stdout.__len__() > 0:
            jshint_flag = False
        else:  # 通过了检查，此时 test_file_name中就是美化后的代码
            jshint_flag = True
            # print(f"{temp_file_path}right!")
        return jshint_flag

    def assemble_to_testcase(self, times):
        """
        将function组装成用例
        :return:
        """
        callable_processor = CallableProcessor()
        try:
            function_assemle_list = set()

            # 连续组装times次
            for i in range(times):
                function_assemle = callable_processor.generate_self_calling(self.Function_content)
                function_assemle_list.add(function_assemle)

            testcases_list_to_write = self.makeTestcasesListToWrite(all_testcases=function_assemle_list,
                                                                    SourceFun_id=self.Id)
            # #
            table_Testcase = Table_Testcase()
            # #
            table_Testcase.insertManyDataToTableTestcase(testcases_list_to_write)
            return testcases_list_to_write
        except:
            pass
#
#
# def makeFunctionListToWrite(all_functions, SourceFun_id, mutation_type, mutation_times, Remark) -> list:
#     # 将生成的代码写入数据库
#
#     lis = []
#
#     for function in all_functions:
#         Function_content = function
#         item = [Function_content, SourceFun_id, mutation_type, mutation_times, Remark]
#         lis.append(item)
#     return lis
#
#
# def write_to_Table_function(*lis):
#     list_to_write = []
#
#     for item in lis:
#         list_to_write += item
#     # print(list_to_write)
#
#     table_Function = Table_Function()
#     table_Function.insertManyDataToTableFunction(list_to_write)
