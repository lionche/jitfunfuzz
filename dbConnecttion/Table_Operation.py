# 对表Table_Function进行操作
from dbConnecttion.MySqlConn import MyPymysqlPool


class Table_Function(object):
    def __init__(self):
        # 实例化 DataBaseHandle()
        self.__table = MyPymysqlPool()

    # 单行查询
    def selectOneFromTableFunction(self, id):
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = 'select * from Table_Function where id=%s'
        prames = (id)
        res = self.__table.getOne(sql, prames)
        self.__table.dispose()
        return res

    def selectIdFromTableFunction(self, id):
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = 'select * from Table_Function where id=%s'
        prames = (id)
        res = self.__table.getAll(sql, prames)
        self.__table.dispose()
        return res

    def selectSourceIdFromTableFunction(self, SourceFun_id):
        """
        条件查询全部符合的数据\n
        查询初始的用例即SourceFun_id==0用例\n
        :param SourceFun_id: 父用例id
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f'select * from Table_Function where SourceFun_id={SourceFun_id}'
        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

        # return self.__table.selectOne(sql, prames)

    # # ???从指定id开始查询Number条数据
    # def selectFromTableFunctionForNumber(self, id, number):
    #     sql = 'select * from Table_Function where id=%s limit %s'
    #     prames = (id, number)
    #     return self.__table.selectmany(sql, prames)

    # 全部查询
    def getAllFromTableFunction(self):
        sql = 'select * from Table_Function'
        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

    # 插入单行数据
    def insertDataToTableFunction(self, Function_Content, SourceFun_Id, Mutation_Method, Remark):
        """插入单行数据
        :param Id: 自增的主键id
        :param Function_Content: 方法内容
        :param SourceFun_Id: 源方法id
        :param Mutation_Method: 变异方法的序号，没有变异是0
        :param Remark:
        :return:
        """
        sql = 'INSERT INTO Table_Function(Function_content,SourceFun_id,Mutation_method,Remark) values(%s,%s,%s,%s)'
        prames = (Function_Content, SourceFun_Id, Mutation_Method, Remark)
        res = self.__table.insert(sql, prames)
        self.__table.dispose()
        return res

    # 插入多条数据,可避免数据库多次打开关闭。
    '''
    lis为一个数据列表，形式如：
    lis = [[id,catid,typeid,title],[id2,catid2,typeid2,title2]]
    '''

    def insertManyDataToTableFunction(self, lis):
        sql = 'insert into Table_Function(Function_content,SourceFun_id,Mutation_method,Mutation_times,Remark) values(%s,%s,%s,%s,%s)'
        res = self.__table.insertMany(sql, lis)
        self.__table.dispose()
        return res

    # 删除数据
    def deleteFromTableFunction(self, id):
        sql = 'delete from Table_Function where id=%s'
        prames = (id,)
        res = self.__table.delete(sql, prames)
        self.__table.dispose()
        return res

    # 删除全部
    def deleteAllFromTableFunction(self):
        sql = 'delete from Table_Function'
        res = self.__table.deleteAll(sql)
        self.__table.dispose()
        return res

    # 更改数据
    def updateDataBaseHandle(self, id, Function_content):
        sql = 'update Table_Function set Function_content= %s where id = %s'
        prames = (Function_content, id)
        res = self.__table.update(sql, prames)
        self.__table.dispose()
        return res

    def updateMutationTimes(self, MutationTimes, id):
        sql = 'update Table_Function set Mutation_times= %s where id = %s'
        prames = (MutationTimes, id)
        res = self.__table.update(sql, prames)
        self.__table.dispose()
        return res

    def selectMutationTimesFromTableFunction(self, Mutation_Times, SourceFun_id):
        """
        条件查询全部符合的数据\n
        查询初始的用例即SourceFun_id==0用例\n
        :param SourceFun_id: 父用例id
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f'select * from Table_Function where Mutation_times={Mutation_Times} AND SourceFun_id = {SourceFun_id} '
        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res


# 对表Table_Testcase进行操作
class Table_Testcase(object):
    '''
    Id：主键，自增\n
    Testcase_context：用例内容\n
    SourceFun_id：源方法id\n
    SourceTestcase_id：源用例id，0代表直接从方法组装的用例\n
    Mutation_method:0代表没有变异\n
    Remark
    '''

    def __init__(self):
        self.__table = MyPymysqlPool()

    # 单行查询
    def selectOneFromTableTestcase(self, id):
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = 'select * from Table_Testcase where id=%s'
        prames = (id)
        res = self.__table.getOne(sql, prames)
        self.__table.dispose()
        return res

    def selectIdFromTableTestcase(self, id):
        """
        条件查询全部符合的数据\n
        查询初始的用例即SourceFun_id==0用例\n
        :param SourceFun_id: 父用例id
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f'select * from Table_Testcase where Id={id}'
        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

    def getAllFromTableTestcase(self):
        """
        条件查询全部符合的数据\n
        查询初始的用例即SourceFun_id==0用例\n
        :param SourceFun_id: 父用例id
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f'select * from Table_Testcase'
        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

    def getIdLimitFromTableTestcase(self, start, end):
        """
        条件查询全部符合的数据\n
        查询初始的用例即SourceFun_id==0用例\n
        :param SourceFun_id: 父用例id
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f'select * from Table_Testcase where id between {start} and {end}'
        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

    def selectInterestingTimeFromTableTestcase(self, Interesting_times):
        """
        条件查询全部符合的数据\n
        查询初始的用例即SourceFun_id==0用例\n
        :param SourceFun_id: 父用例id
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f'select * from Table_Testcase where Interesting_times={Interesting_times}'
        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

    def selectFuzzingTimeFromTableTestcase(self, Fuzzing_times):
        """
        条件查询全部符合的数据\n
        查询初始的用例即SourceFun_id==0用例\n
        :param SourceFun_id: 父用例id
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f'select * from Table_Testcase where Fuzzing_times={Fuzzing_times}'
        res = self.__table.getAll(sql)
        self.__table.dispose()

        return res

    def selectFuzzingTimeDistributedFromTableTestcase(self, Fuzzing_times, DistributedStart, DistributedEnd):
        """
        条件查询全部符合的数据\n
        查询初始的用例即SourceFun_id==0用例\n
        :param SourceFun_id: 父用例id
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f'select * from Table_Testcase where Fuzzing_times={Fuzzing_times} and id BETWEEN {DistributedStart} AND {DistributedEnd}'
        res = self.__table.getAll(sql)
        self.__table.dispose()

        return res

    def selectMutationMethodFromTableTestcase(self, Mutation_method):
        sql = f'select * from Table_Testcase where Mutation_method!={Mutation_method}'
        res = self.__table.getAll(sql)
        self.__table.dispose()

        return res

    # 选择没有被变异过得最初的种子池
    def selectMutationTimeAndMutation_methodFromTableTestcase(self, Mutation_method, MutationTime):
        sql = f'select * from Table_Testcase where Mutation_method ={Mutation_method} and Mutation_times ={MutationTime}'
        res = self.__table.getAll(sql)
        self.__table.dispose()

        return res

    def selectSourceTestcaseIdFromTableTestcase(self, SourceTestcase_id):
        sql = f'select * from Table_Testcase where SourceTestcase_id={SourceTestcase_id}'
        res = self.__table.getAll(sql)
        self.__table.dispose()

        return res

    def selectEngine_coverage_integration_all_is_not_nullFromTableTestcase(self):
        sql = f'select * from Table_Testcase where Engine_coverage_integration_all is not null'
        res = self.__table.getAll(sql)
        self.__table.dispose()

        return res

    def selectEngine_coverage_integration_all_is_null_and_MutationTimeIsNOT0FromTableTestcase(self):
        sql = f'select * from Table_Testcase where Engine_coverage_integration_all is null and Mutation_method = 0 and Mutation_times !=0'
        self.__table.dispose()
        res = self.__table.getAll(sql)
        return res

    def selectEngine_coverage_integration_all_is_null_and_MutationTimeIsNOT0RangeFromTableTestcase(self, start, end):
        sql = f'select * from Table_Testcase where Engine_coverage_integration_all is null and Mutation_method = 0 and Mutation_times !=0 and id between {start} and {end}'
        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

    def selectSourceTestcaseIdNoFuzzingFromTableTestcase(self, SourceTestcase_id):
        sql = f'select * from Table_Testcase where SourceTestcase_id={SourceTestcase_id} and Fuzzing_times = 0'
        rse = self.__table.getAll(sql)
        self.__table.dispose()

        return rse

    # 插入单行数据
    def insertDataToTableTestcase(self, Testcase_context, SourceFun_id, SourceTestcase_id, Fuzzing_times,
                                  Mutation_method, Mutation_times, Interesting_times, engine_coverage,
                                  Engine_coverage_integration_source, Engine_coverage_integration_all, Probability,
                                  Remark):
        """插入单行数据
        :param Id: 自增的主键id
        :param Testcase_context: 用例内容
        :param SourceFun_Id: 源方法id
        :param SourceTestcase_id: 原用例id
        :param Mutation_Method: 变异用例的序号，没有变异是0
        :param engine_coverage 用例单独的覆盖率
        :param Engine_coverage_integration_source 用例和父用例的整合覆盖率
        :param Engine_coverage_integration_all 用例和所有子用例的整合覆盖率
        :param Remark:
        :return:
        """
        sql = 'INSERT INTO Table_Testcase(Testcase_context, SourceFun_id, SourceTestcase_id, Fuzzing_times,Mutation_method ,Mutation_times,Interesting_times,engine_coverage,Engine_coverage_integration_source,Engine_coverage_integration_all,Probability,Remark) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        prames = (Testcase_context, SourceFun_id, SourceTestcase_id, Fuzzing_times, Mutation_method, Mutation_times,
                  Interesting_times, engine_coverage, Engine_coverage_integration_source,
                  Engine_coverage_integration_all, Probability, Remark)
        res = self.__table.insert(sql, prames)
        self.__table.dispose()

        return res

    # 插入多条数据,可避免数据库多次打开关闭。
    '''
    lis为一个数据列表，形式如：
    lis = [[id,catid,typeid,title],[id2,catid2,typeid2,title2]]
    '''

    def insertManyDataToTableTestcase(self, lis):
        sql = 'INSERT INTO Table_Testcase(Testcase_context, SourceFun_id, SourceTestcase_id, Fuzzing_times,Mutation_method ,Mutation_times,Interesting_times,engine_coverage,Engine_coverage_integration_source,Engine_coverage_integration_all,Probability,Remark) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        res = self.__table.insertMany(sql, lis)
        self.__table.dispose()
        return res

    # 删除数据
    def deleteFromTableTestcase(self, id):
        sql = 'delete from Table_Testcase where id=%s'
        prames = (id,)
        res = self.__table.delete(sql, prames)
        self.__table.dispose()

        return res

    # 删除全部
    # def deleteAllFromTableTestcase(self):
    #     sql = 'delete from Table_Testcase'
    #     self.__table.dispose()
    #
    #     return self.__table.deleteAll(sql)

    # 更改数据
    def updateDataBaseHandle(self, id, Function_content):
        sql = 'update Table_Testcase set Testcase_context= %s where id = %s'
        prames = (Function_content, id)
        res = self.__table.update(sql, prames)
        self.__table.dispose()
        return res

    def updateFuzzingTimesInterestintTimesCovInfo(self, Fuzzing_times, Interesting_times, engine_coverage,
                                                  Engine_coverage_integration_source,
                                                  id):
        sql = 'update Table_Testcase set Fuzzing_times= %s ,Interesting_times = %s, engine_coverage= %s, Engine_coverage_integration_source = %s where id = %s'
        prames = (Fuzzing_times, Interesting_times, engine_coverage,
                  Engine_coverage_integration_source, id)
        res = self.__table.update(sql, prames)
        self.__table.dispose()
        return res

    def updateMutationTimes(self, MutationTimes, id):
        sql = 'update Table_Testcase set Mutation_times= %s where id = %s'
        prames = (MutationTimes, id)
        res = self.__table.update(sql, prames)
        self.__table.dispose()
        return res

    def updateSourceEngine_coverage_integration_all(self, Engine_coverage_integration_all, id):
        sql = 'update Table_Testcase set Engine_coverage_integration_all= %s where id = %s'
        prames = (Engine_coverage_integration_all, id)
        res = self.__table.update(sql, prames)
        self.__table.dispose()
        return res



# Table_Result
class Table_Result(object):
    '''
    Id：主键，自增\n
    Testcase_Id：用例id
    Testbed_Id：js引擎编号
    Returncode：返回值
    Stdout：输出
    Stderr：错误输出
    duration_ms：耗时
    seed_coverage：种子覆盖率
    engine_coverage：引擎覆盖率
    Remark：
    '''

    def __init__(self):
        # 实例化 DataBaseHandle()
        self.__table = MyPymysqlPool()

    # 按用例编号查询
    def selectTestcasesFromTableResult(self, Testcase_id):
        sql = f'select * from Table_Result where Testcase_id={Testcase_id}'
        get_all = self.__table.getAll(sql)
        self.__table.dispose()
        return get_all

    # def selectFuzzingTimeFromTableResult(self, Fuzzing_times):
    #     """
    #     条件查询全部符合的数据\n
    #     查询初始的用例即SourceFun_id==0用例\n
    #     :param SourceFun_id: 父用例id
    #     :return:所有符合条件的数据的List
    #     """
    #     # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
    #     sql = f'select * from Table_Result where Fuzzing_times={Fuzzing_times}'
    #     return self.__table.getAll(sql)

    # return self.__table.selectOne(sql, prames)

    # 全部查询
    def getAllFromTableResult(self):
        sql = 'select * from Table_Result'
        get_all = self.__table.getAll(sql)
        self.__table.dispose()
        return get_all

    # 插入单行数据

    def insertDataToTableResult(self, Testcase_Id, Testbed_Id, Returncode, Stdout, Stderr, duration_ms, seed_coverage,
                                Remark):
        """插入单行数据
        :param Id: 自增的主键id
        :param Testcase_context: 用例内容
        :param SourceFun_Id: 源方法id
        :param SourceTestcase_id: 原用例id
        :param Mutation_Method: 变异用例的序号，没有变异是0
        :param Remark:
        :return:
        """
        sql = 'INSERT INTO Table_Result(Testcase_Id, Testbed_Id, Returncode, Stdout,Stderr ,duration_ms,seed_coverage,Remark) values(%s,%s,%s,%s,%s,%s,%s,%s)'
        prames = (
            Testcase_Id, Testbed_Id, Returncode, Stdout, Stderr, duration_ms, seed_coverage, Remark)
        res = self.__table.insert(sql, prames)
        self.__table.dispose()
        return res

    # 插入多条数据,可避免数据库多次打开关闭。
    '''
    lis为一个数据列表，形式如：
    lis = [[id,catid,typeid,title],[id2,catid2,typeid2,title2]]
    '''

    def selectTestcaseIdFromTableResult(self, testcase_id):
        """
        条件查询全部符合的数据\n
        :param testcase_id: 用例id
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f'select * from Table_Result where Testcase_id={testcase_id}'
        res = self.__table.getAll(sql)
        self.__table.getAll(sql)
        return res

    def insertManyDataToTableResult(self, lis):
        sql = 'INSERT INTO Table_Result(Testcase_Id, Testbed_Id, Returncode, Stdout,Stderr ,duration_ms,seed_coverage,Remark) values(%s,%s,%s,%s,%s,%s,%s,%s)'
        res = self.__table.insertMany(sql, lis)
        self.__table.dispose()
        return res

    # 删除数据
    def deleteFromTableResult(self, id):
        sql = 'delete from Table_Result where id=%s'
        prames = (id,)
        res = self.__table.delete(sql, prames)
        self.__table.getAll(sql)
        return res

    # 根据testcases id删除数据
    def deleteByTestcaseIdFromTableResult(self, testcase_id):
        sql = f'delete from Table_Result where testcase_id={testcase_id}'
        res = self.__table.delete(sql)
        self.__table.dispose()
        return res

    # 删除全部
    def deleteAllFromTableResult(self):
        sql = 'delete from Table_Result'
        res = self.__table.deleteAll(sql)
        self.__table.dispose()
        return res

    # # 更改数据
    # def updateDataBaseHandle(self, id, Function_content):
    #     sql = 'update Table_Result set Testcase_context= %s where id = %s'
    #     prames = (Function_content, id)
    #     return self.__table.update(sql, prames)
#
#
class Table_Testbed(object):

    def __init__(self):
        # 实例化 DataBaseHandle()
        self.__table = MyPymysqlPool()

    def getAllFromTableTestbed(self):
        sql = 'select * from Table_Testbed'
        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

class Table_Suspicious_Result(object):

    def __init__(self):
        # 实例化 DataBaseHandle()
        self.__table = MyPymysqlPool()

    def insertDataToTableSuspiciousResult(self, Error_type, Testcase_id, Function_id, Testbed_id, Remark, Is_filtered):
        """插入单行数据
        :param Error_type: 错误类型
        :param Testcase_id: 用例ip
        :param Function_id: 方法id
        :param Testbed_id: 引擎id
        :param Remark:
        :param Is_filtered:是否有被过滤过，0是没有，1是有
        :return:
        """
        sql = 'INSERT INTO Table_Suspicious_Result( Error_type, Testcase_id, Function_id, Testbed_id,  Remark,Is_filtered) values(%s,%s,%s,%s,%s,%s)'
        prames = (Error_type, Testcase_id, Function_id, Testbed_id, Remark, Is_filtered)
        res = self.__table.insert(sql, prames)
        self.__table.dispose()

        return res

    def selectErrorTypeFromTableFunction(self, ErrorType):
        """
        条件查询全部符合的数据\n
        :param ErrorType: 错误类型
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f"select * from Table_Suspicious_Result where Error_type={ErrorType} ORDER BY Testcase_id"

        res = self.__table.getAll(sql)
        self.__table.dispose()

        return res

    def selectErrorTypeUnfilteredFromTableFunction(self, ErrorType):
        """
        条件查询全部符合的数据\n
        :param ErrorType: 错误类型
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f"select * from Table_Suspicious_Result where Error_type={ErrorType} And Is_filtered='0' ORDER BY Testcase_id"

        res = self.__table.getAll(sql)
        self.__table.dispose()

        return res

    def selectIdFromTable_Suspicious_Result(self, id):
        """
        条件查询全部符合的数据\n
        :param ErrorType: 错位类型
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f'select * from Table_Suspicious_Result where Id={id}'
        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

    def selectTestcseIdFromTable_Suspicious_Result(self, Testcase_id):
        """
        条件查询全部符合的数据\n
        :param ErrorType: 错位类型
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f'select * from Table_Suspicious_Result where Testcase_id={Testcase_id}'

        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

    def selectUnFilteredFromTable_Suspicious_Result_with_error_type(self, error_type):
        """
        条件查询全部符合的数据\n
        :param error_type: 错误类型
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f"select * from Table_Suspicious_Result where Is_filtered='0' AND error_type = {error_type}"

        # sql = f"# select * from Table_Suspicious_Result where error_type = {error_type}"
        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

    def selectUnFilteredFromTable_Suspicious_Result(self):
        """
        条件查询全部符合的数据\n
        :param error_type: 错误类型
        :return:所有符合条件的数据的List
        """
        # 注意在数据库操作时无 %d ,全部字段都用%s来匹配，无论哪种数据类型。
        sql = f"select * from Table_Suspicious_Result where Is_filtered='0'"
        # sql = f"select * from Table_Suspicious_Result where Is_filtered='0' LIMIT 0,50"

        res = self.__table.getAll(sql)
        self.__table.dispose()
        return res

    # 更改数据
    def updateIs_filtered(self, id, Is_filtered):
        sql = 'update Table_Suspicious_Result set Is_filtered= %s where id = %s'
        prames = (Is_filtered, id)

        res = self.__table.update(sql, prames)
        self.__table.dispose()
        return res

    # 根据 id删除数据
    def deleteByTestcaseIdFromTable_Suspicious_Result(self, id):
        sql = f'delete from Table_Suspicious_Result where id={id}'
        res = self.__table.delete(sql)
        self.__table.dispose()
        return res

# if __name__ == '__main__':
# table_testbed = Table_Testbed()
# print(table_testbed.getAllIdAndLocateFromTableTestbed())
# table_Function = Table_Function()

# 查询全部数据
# print(table_Function.getAllFromTableFunction())
# 删除全部数据
# table_Function.deleteAllFromTableFunction()
# 增加单条数据
# table_Function.insertDataToTableFunction(Function_content='Function(hello)',
#                                             SourceFun_id=0,
#                                             Mutation_method=0,
#                                             Remark='hello21')
# 增加多条数据
# lis = [('Function(hello1)', 1, 1, 1), ('Function(hello2)', 2, 2, 2)]
# table_Function.insertManyDataToTableFunction(lis)

# 单行查询
# print(table_Function.selectOneFromTableFunction(id=2))

# 单行查询
# print(table_Function.selectSourceIdFromTableFunction(SourceFun_id=0))
# 删除单条数据
# print(table_Function.deleteFromTableFunction(id=6))
# 更改数据
# print(table_Function.updateDataBaseHandle(5, 'Fuuu'))

# table_Testcases = Table_Testcase()
# #Testcase_context, SourceFun_id, SourceTestcase_id, Mutation_method, ,Fuzzing_times,Mutation_times,Interesting_times,Probability,Remark
# table_Testcases.insertDataToTableTestcase(Testcase_context='Testcase(hello)',
#                                           SourceFun_id=1,
#                                           SourceTestcase_id=0,
#                                           Mutation_method=0,
#                                           Fuzzing_times=0,
#                                           Mutation_times=0,
#                                           Interesting_times=0,
#                                           Probability=None,
#                                           Remark='hello')
