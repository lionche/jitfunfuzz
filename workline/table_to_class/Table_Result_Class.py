import sys
sys.path.append('/root/Comfort_all')

class Result_Object(object):

    def __init__(self, result_object):

        self.Id = result_object[0]
        self.Testcase_Id: str = result_object[1]
        self.Testbed_Id = result_object[2]
        self.Returncode = result_object[3]
        self.Stdout = result_object[4]
        self.Stderr = result_object[5]
        self.duration_ms = result_object[6]
        self.Remark = result_object[7]