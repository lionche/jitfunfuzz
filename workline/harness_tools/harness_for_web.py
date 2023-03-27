from workline.table_to_class.Table_Testcase_Class import Testcase_Object


def harness_testcase(testcase):
    # print(testcase)
    testcase_object = Testcase_Object(testcase)

    # 获得差分结果，各个引擎输出
    harness_result = testcase_object.engine_run_testcase(timeout="30")
    different_result_list = harness_result.differential_test()
    # print(harness_result)
    return harness_result, different_result_list
