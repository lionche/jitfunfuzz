import os
import subprocess
import sys
from multiprocessing.pool import ThreadPool

from tqdm import tqdm


def Accuractrate(cmd):
    # 使用v8执行用例，其中return值为0的用例是没有语法错误的用例。 判断数量

    global testPassRateSet

    pro = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                           stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = pro.communicate()
    pbar.update(1)
    if pro.returncode == 0:
        testPassRateSet.add(cmd)
    else:
        pass
        # print(pro.stderr)


if __name__ == '__main__':
    v8_cmd = '/root/engine/v8-debug/v8-debug --allow-natives-syntax '

    # 考虑内存溢出
    testPassRateSet = set()
    cmdlist = []
    count = 0

    for name in ['comfort', 'die', 'fuzzilli', 'codealchemest']:
        path = f"/root/fuzzopt/experiments/corpus/{name}/"
        for file in os.listdir(path):  # file 表示的是文件名
            cmd = v8_cmd + path + file
            if file.endswith('.js'):
                cmdlist.append(cmd)
                count += 1;
        pbar = tqdm(total=count)
        pool = ThreadPool()
        pool.map(Accuractrate, cmdlist)
        pool.close()
        pool.join()
        # print("处理了" + str(count) + "个函数文件！")
        print(name + "生成的用例语法正确率为{:.2%},".format(len(testPassRateSet) / count))
        pbar.close()
