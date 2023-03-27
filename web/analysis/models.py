from django.db import models


# Create your models here.
class Testbed(models.Model):
    Testbed_name = models.TextField('引擎名称', null=True)
    Testbed_version = models.TextField('引擎版本', null=True)
    Testbed_location = models.TextField('引擎位置', null=True)
    Remark = models.TextField('备注', null=True)

    def __str__(self):
        return self.Testbed_name

    # create_timestamp = models.DateTimeField(auto_now_add=True)
    # last_edit_timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "Table_Testbed"  # 表名
        verbose_name = "引擎"  # 显示名称
        verbose_name_plural = verbose_name


class Function(models.Model):
    Function_content = models.TextField(null=True)
    SourceFun_id = models.IntegerField(null=True)
    Mutation_method = models.IntegerField(null=True)
    Mutation_times = models.IntegerField(null=True)
    Remark = models.TextField(null=True)

    class Meta:
        db_table = "Table_Function"  # 表名


class Suspicious_Result(models.Model):
    Error_type = models.TextField(null=True)
    Testcase_id = models.IntegerField(null=True)
    Function_id = models.IntegerField(null=True)
    Testbed_id = models.IntegerField(null=True)
    Is_filtered = models.TextField(null=True)
    Remark = models.TextField(null=True)

    class Meta:
        db_table = "Table_Suspicious_Result"  # 表名


class Testcase(models.Model):
    Testcase_context = models.TextField(null=True)
    SourceFun_id = models.IntegerField(null=True)
    SourceTestcase_id = models.IntegerField(null=True)
    Fuzzing_times = models.IntegerField(null=True)
    Mutation_method = models.IntegerField(null=True)
    Mutation_times = models.IntegerField(null=True)
    Interesting_times = models.IntegerField(null=True)
    Engine_coverage = models.TextField(null=True)
    Engine_coverage_integration_source = models.TextField(null=True)
    Engine_coverage_integration_all = models.TextField(null=True)
    Probability = models.IntegerField(null=True)
    Remark = models.TextField(null=True)

    class Meta:
        db_table = "Table_Testcase"  # 表名


class Result(models.Model):
    Testcase_id = models.IntegerField(null=True)
    Testbed_id = models.IntegerField(null=True)
    Returncode = models.IntegerField(null=True)
    Stdout = models.TextField(null=True)
    Stderr = models.TextField(null=True)
    Duration_ms = models.IntegerField(null=True)
    Seed_coverage = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    # Engine_coverage = models.TextField(null=True)
    Remark = models.TextField(null=True)

    class Meta:
        db_table = "Table_Result"  # 表名
