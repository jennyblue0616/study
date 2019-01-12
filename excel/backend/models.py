# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Dept(models.Model):
    no = models.IntegerField(primary_key=True, db_column='dno')
    name = models.CharField(max_length=10, db_column='dname')
    loc = models.CharField(max_length=20, db_column='dloc')

    class Meta:
        managed = False
        app_label = 'hrs'
        db_table = 'tb_dept'


class Emp(models.Model):
    no = models.IntegerField(primary_key=True, db_column='eno')
    name = models.CharField(max_length=20, db_column='ename')
    job = models.CharField(max_length=20)
    mgr = models.ForeignKey('self', models.PROTECT, db_column='mgr', blank=True, null=True)
    sal = models.IntegerField()
    comm = models.IntegerField(blank=True, null=True)
    dept = models.ForeignKey(Dept, models.DO_NOTHING, db_column='dno', blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'hrs'
        db_table = 'tb_emp'
