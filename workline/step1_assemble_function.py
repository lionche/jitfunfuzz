import os
import sys
from multiprocessing.pool import ThreadPool
from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parent.parent)
sys.path.append(BASE_DIR)

from dbConnecttion.Table_Operation import Table_Function
from workline.table_to_class.Table_Function_Class import Function_Object
from tqdm import tqdm

# Function_content_list = Table_Function().selectIdFromTableFunction(7)
Function_content_list = Table_Function().getAllFromTableFunction()
pbar = tqdm(total=len(Function_content_list))


# for Function_content in Function_content_list:
#     FUNCTION = Function_Object(Function_content)
#     for function in FUNCTION.assemble_to_testcase(1):
#         pbar.update(1)
        # print(function[0])


def muti_assemble(Function_content):
    function_Object = Function_Object(Function_content)
    assemble_to_testcase = function_Object.assemble_to_testcase(1)
    # print(assemble_to_testcase[0][0])
    pbar.update(1)


pool = ThreadPool()
results = pool.map(muti_assemble, Function_content_list)
pool.close()
pool.join()
pbar.close()
