'''
差分测试
'''
import time
# export LC_ALL=C
import sys
from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parent.parent)
sys.path.append(BASE_DIR)
from multiprocessing.dummy import Pool as ThreadPool
import sys
from pathlib import Path
from tqdm import tqdm

from dbConnecttion.Table_Operation import Table_Testcase

BASE_DIR = str(Path(__file__).resolve().parent.parent)
sys.path.append(BASE_DIR)
from workline.table_to_class.Table_Testcase_Class import Testcase_Object

table_Testcases = Table_Testcase()

# 获取未差分过得测试用例,进行差分，并将差分后的结果插入到数据库中

# list_unharness = table_Testcases.selectIdFromTableTestcase(1)
list_unharness = table_Testcases.selectFuzzingTimeFromTableTestcase(0)
# list_unharness = table_Testcases.getIdLimitFromTableTestcase(1000, 1000)
# pbar = tqdm(total=len(list_unharness))

print("一共有%d条未差分的测试用例" % len(list_unharness))


def muti_harness(testcase):
    testcase_object = Testcase_Object(testcase)

    # print('*' * 25 + f'差分用例{testcase_object.Id}' + '*' * 25)
    # pbar.update(1)
    # start_time = time.time()
    # # 获得差分结果，各个引擎输出
    # try:
    #     harness_result = testcase_object.engine_run_testcase()
    #     different_result_list = harness_result.differential_test()
    #     if len(different_result_list):
    #         for interesting_test_result in different_result_list:
    #             # print(interesting_test_result)
    #             if interesting_test_result.testbed_name == "d8" and "use asm" in harness_result.testcase_context:
    #                 pass
    #             elif interesting_test_result.testbed_name == "chakra" and interesting_test_result.error_type == "crash" and "The futex facility returned an unexpected error code" in harness_result.outputs[2]:
    #                 pass
    #             else:
    #                 print(
    #                     f"用例id:{interesting_test_result.testcase_id}，错误类型{interesting_test_result.error_type},错误引擎{interesting_test_result.testbed_name}, http://10.15.0.38:18887/analysis/harness?id={interesting_test_result.testcase_id}")
    # except:
    #     print(f"-----{testcase_object.Id}-----")

    harness_result = testcase_object.engine_run_testcase()
    # different_result_list = harness_result.differential_test()
    # if len(different_result_list):
    #     for interesting_test_result in different_result_list:
            # print(interesting_test_result)
            # if interesting_test_result.testbed_name == "d8" and "use asm" in harness_result.testcase_context:
            #     pass
            # elif interesting_test_result.testbed_name == "chakra" and interesting_test_result.error_type == "crash" and "The futex facility returned an unexpected error code" in harness_result.outputs[2]:
            #     pass
            # elif interesting_test_result.testbed_name == "chakra" and interesting_test_result.error_type == "crash" and "Unexpected identifier after numeric literal" in harness_result.outputs[2]:
            #     pass
            # elif interesting_test_result.testbed_name == "chakra" and interesting_test_result.error_type == "Most JS engines pass" and "BigUint64Array" in harness_result.testcase_context:
            #     pass
            # elif interesting_test_result.testbed_name == "chakra" and interesting_test_result.error_type == "Majority JS engines throw runtime error/exception" and "u" in harness_result.testcase_context:
            #     pass
            # elif interesting_test_result.testbed_name == "chakra" and interesting_test_result.error_type == "Majority JS engines throw runtime error/exception" and "BigInt" in harness_result.testcase_context:
            #     pass
            # elif interesting_test_result.testbed_name == "chakra" and interesting_test_result.error_type == "Most JS engines pass" and ".matchAll" in harness_result.testcase_context:
            #     pass
            # elif interesting_test_result.testbed_name == "jsc" and interesting_test_result.error_type == "Most JS engines pass" and ' "returncode": -9,' in harness_result.outputs[1]:
            #     pass
            # else:
            #     print(
            #         f"用例id:{interesting_test_result.testcase_id}，错误类型{interesting_test_result.error_type},错误引擎{interesting_test_result.testbed_name}, http://10.15.0.38:18887/analysis/harness?id={interesting_test_result.testcase_id}")
    # print(harness_result)

    # Cov_info = testcase_object.getCov()
    # OwnCov = Cov_info[0]
    # SourceCov = Cov_info[1]
    # AllCov = Cov_info[2]
    # print('自身覆盖率：', OwnCov)
    # print('和父用例共同的覆盖率: ', SourceCov)
    # 父用例和所有子用例的覆盖率存入父用例属性中
    # print('父用例和所有子用例的覆盖率: ', AllCov)

    save2TestcaseTable = False

    # if save2TestcaseTable:
    #     # 根据用例id往用例表中添加自身覆盖率，和父用例共同的覆盖率,父用例和所有子用例的覆盖率
    #     testcase_object.Engine_coverage = OwnCov
    #     testcase_object.Engine_coverage_integration_source = SourceCov
    #     testcase_object.Engine_coverage_integration_all = AllCov
    #
    #     if len(AllCov) != 0:
    #         testcase_object.updateSourceEngine_coverage_integration_all()

    # 把结果插入到result数据库中

    # 是否存入数据库
    save2ResultTable = True
    if save2ResultTable:

        # 投票
        different_result_list = harness_result.differential_test()

        # 如果一个用例
        if len(different_result_list):

            # 触发问题之后再保存可疑结果
            try:
                # print('触发问题，存入数据库')
                harness_result.save_to_table_result()
            except:
                pass

            # print("共触发了{}个引擎错误".format(len(different_result_list)))

            testcase_object.add_interesting_times(1)

            # print(f'Inconsistent behaviour found by differential testing:')

            # print(f"------------------------------------------------------\n")

            # 可疑结果存入数据库
            for interesting_test_result in different_result_list:
                print(
                    f"用例id:{interesting_test_result.testcase_id}，错误类型{interesting_test_result.error_type},错误引擎{interesting_test_result.testbed_name}, http://10.15.0.38:18887/analysis/harness?id={interesting_test_result.testcase_id}")

                # print(interesting_test_result)
                interesting_test_result.save_to_table_suspicious_Result()
                # print(interesting_test_result)

            # unfiltered_list = Table_Suspicious_Result().selectTestcseIdFromTable_Suspicious_Result(testcase_object.Id)
            # for suspicious_testcase in unfiltered_list:
            #     # print(suspicious_testcase)
            #     suspicious_result = Suspicious_Result_Object(suspicious_testcase)
            # suspicious_result.analysis()

            # print(f"JS engines running results:")

            # print(f"------------------------------------------------------\n")

            # print(f"{harness_result}")

            # print(f"------------------------------------------------------\n")

        # print(f'共耗时{int(time.time() - start_time)}秒')
        # 更新testcases表中的fuzzing次数和interesting次数,覆盖率信息
        testcase_object.updateFuzzingTimesInterestintTimesCovInfo()


pool = ThreadPool()
results = pool.map(muti_harness, list_unharness)
pool.close()
pool.join()

# pbar.close()
