import sys
from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parent.parent)
sys.path.append(BASE_DIR)
print(BASE_DIR)
from MySqlConn import MyPymysqlPool

mysql = MyPymysqlPool()

sql = 'insert into Table_Testbed (Testbed_name, Testbed_version,Testbed_location,Remark) VALUES (%s,%s,%s,%s);'

args = [('d8', '11.3.70', '/root/engine/v8-debug/v8-debug --allow-natives-syntax', None),
        ('spiderMonkey', 'JavaScript-C112.0a1',
         '/root/engine/spm  --baseline-warmup-threshold=10 --ion-warmup-threshold=100 --ion-check-range-analysis --ion-extra-checks --fuzzing-safe',
         None),
        ('chakra', 'ch version 1.13.0.0-beta',
         '/root/engine/ch --maxinterpretcount:20 --maxsimplejitruncount:100 --bgjit --oopjit', None),
        ('jsc', 'WebKit-7616.1.4',
         '/root/engine/jsc --validateOptions=true --thresholdForJITSoon=20 --thresholdForJITAfterWarmUp=20 --thresholdForOptimizeAfterWarmUp=100 --thresholdForOptimizeAfterLongWarmUp=100 --thresholdForOptimizeSoon=100 --thresholdForFTLOptimizeAfterWarmUp=1000 --thresholdForFTLOptimizeSoon=1000 --validateBCE=true',
         None)]

result = mysql.insertMany(sql, args)
# print(result)

# 释放资源
mysql.dispose()
