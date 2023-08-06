# -*- coding: utf-8 -*

import pysnooper
import random
import requests
import datetime
import json
import time
import consul
import random
import re

from retrying import retry

from .consul_support import ConsulClient

stop_max_delay = 5400000
stop_max_attempt_number = 3
wait_fixed = 180000


def retry_if_result_none(result_flag):
    if result_flag[0]:
        return not result_flag[0]
    return True


def get_hive_config(server_app_name):
    consul_client = ConsulClient(application_name=server_app_name)
    spark_api_info = {}
    c_keys = ['spark.services_name', 'spark.spark_token', 'spark.mysql_query_path', 'spark.mysql_query_result_path',
              'spark.task_run_path', 'spark.describe_query_path', 'spark.seq_sql_path', 'spark.get_partitions_path',
              'retry.stop_max_delay', 'retry.stop_max_attempt_number', 'retry.wait_fixed'
              ]
    services_name, spark_token, mysql_query_path, mysql_query_result_path, task_run_path, describe_query_path, seq_sql_path, \
    get_partitions_path, stop_max_delay, stop_max_attempt_number, wait_fixed = consul_client.get_consul_kv(*c_keys)
    head = {"spark-token": spark_token}
    service_address, service_port = consul_client.consul_server_discovery(services_name)
    url_prefix = f"http://{service_address}:{service_port}"
    spark_api_info.setdefault('url_prefix', url_prefix)
    spark_api_info.setdefault('head', head)
    spark_api_info.setdefault('mysql_query_path', mysql_query_path)
    spark_api_info.setdefault('mysql_query_result_path', mysql_query_result_path)
    spark_api_info.setdefault('task_run_path', task_run_path)
    spark_api_info.setdefault('describe_query_path', describe_query_path)
    spark_api_info.setdefault('seq_sql_path', seq_sql_path)
    spark_api_info.setdefault('get_partitions_path', get_partitions_path)
    spark_api_info.setdefault('stop_max_delay', stop_max_delay)
    spark_api_info.setdefault('stop_max_attempt_number', stop_max_attempt_number)
    spark_api_info.setdefault('wait_fixed', wait_fixed)
    return spark_api_info


class SparkHqlHandler(object):
    def __init__(self, spark_api_info, **kwargs):
        self._url_prefix = spark_api_info.get('url_prefix')
        self._head = spark_api_info.get('head')
        self.mysql_query_path = spark_api_info.get('mysql_query_path')
        self.mysql_query_result_path = spark_api_info.get('mysql_query_result_path')
        self.task_run_path = spark_api_info.get('task_run_path')
        self.describe_query_path = spark_api_info.get('describe_query_path')
        self.seq_sql_path = spark_api_info.get('seq_sql_path')
        self.get_partitions_path = spark_api_info.get('get_partitions_path')
        self.stop_max_delay = stop_max_delay if spark_api_info.get('stop_max_delay') is None else spark_api_info.get(
            'stop_max_delay')
        self.stop_max_attempt_number = stop_max_attempt_number if spark_api_info.get(
            'stop_max_attempt_number') is None else spark_api_info.get(
            'stop_max_attempt_number')
        self.wait_fixed = wait_fixed if spark_api_info.get('wait_fixed') is None else spark_api_info.get(
            'wait_fixed')

    @retry(wait_fixed=wait_fixed, stop_max_attempt_number=stop_max_attempt_number)
    def sending_request(self, url, headers, json_data, date_type=1):
        result_flag = False
        res = None
        if date_type == 1:
            response = requests.post(url=url, headers=headers,
                                     json=json_data)
        else:
            response = requests.post(url=url, headers=headers,
                                     data=json_data)
        res = json.loads(response.text)
        if res.get('code') == 200:
            result_flag = True
        return result_flag, res

    def query_mysql(self, sql, task_name, relate_id=None, template=None, properties=None, alarm_user_id=None):
        url = self._url_prefix + self.mysql_query_path
        parameter_json = dict()
        parameter_json['taskName'] = task_name
        parameter_json['sql'] = sql
        if template:
            parameter_json['template'] = template
        if properties:
            parameter_json['properties'] = properties
        if relate_id:
            parameter_json['relateId'] = relate_id
        if alarm_user_id:
            parameter_json.setdefault('alarmUserId', alarm_user_id)
        result_flag, response = self.sending_request(url=url, headers=self._head, json_data=parameter_json)
        parameter_json.clear()
        return result_flag, response

    @retry(wait_fixed=wait_fixed, stop_max_attempt_number=stop_max_attempt_number)
    def query_describe(self, json_res):
        describe_flag = False
        fail_result = list()
        parameter_json = dict()
        clusterType = re.findall(r"'clusterType': '(.*?)'", str(json_res))
        clusterId = re.findall(r"'clusterId': '(.*?)'", str(json_res))
        taskId = re.findall(r"'taskId': '(.*?)'", str(json_res))
        url = self._url_prefix + self.describe_query_path
        parameter_json['clusterType'] = clusterType[0]
        parameter_json['clusterId'] = clusterId[0]
        parameter_json['taskId'] = taskId[0]
        while True:
            result_flag, response = self.sending_request(url=url, headers=self._head, json_data=parameter_json)
            if result_flag:
                if response.get("code") == 200:
                    if response.get("data").get("finished") == True:
                        if response.get("data").get("hasFailure") == False:
                            describe_flag = True
                            break
                        else:
                            fail_result = re.findall(r"'failureDetail': '(.*?)'", str(response))
                            break
                    else:
                        time.sleep(150)
                else:
                    break
            else:
                break
        parameter_json.clear()
        return describe_flag, fail_result

    def seq_sql(self, sqls, task_name, flag, relate_id=None, alarm_user_id=None, properties=None, template=None):
        url = self._url_prefix + self.seq_sql_path
        parameter_json = dict()
        parameter_json['taskName'] = task_name
        parameter_json['sqls'] = sqls
        parameter_json['flag'] = flag
        if alarm_user_id:
            parameter_json.setdefault('alarmUserId', alarm_user_id)
        if template:
            parameter_json['template'] = template
        if properties:
            parameter_json['properties'] = properties
        if relate_id:
            parameter_json['relateId'] = relate_id
        result_flag, response = self.sending_request(url=url, headers=self._head, json_data=parameter_json)
        parameter_json.clear()
        return result_flag, response

    def get_partitions(self, db, table, index=None, expr=None):
        partitions = None
        date_type = 0
        parameter_json = dict()
        url = self._url_prefix + self.get_partitions_path
        parameter_json.setdefault('db', db)
        parameter_json.setdefault('table', table)
        if expr:
            parameter_json.setdefault('expr', expr)
        result_flag, response = self.sending_request(url=url, headers=self._head, json_data=parameter_json,
                                                     date_type=date_type)
        parameter_json.clear()
        if result_flag:
            partitions = response.get('data')
            if partitions:
                result = sorted(sum(partitions, []), reverse=True)
                if index:
                    return result[index]
                else:
                    return result
        else:
            return partitions

    def task_run(self, main, jar, task_name, relate_id=None, flag=None, alarm_user_id=None, properties=None,
                 template=None):
        parameter_json = dict()
        url = self._url_prefix + self.task_run_path
        parameter_json['taskName'] = task_name
        parameter_json['main'] = main
        parameter_json['jar'] = jar
        parameter_json['flag'] = flag
        if alarm_user_id:
            parameter_json['alarmUserId'] = alarm_user_id
        if template:
            parameter_json['template'] = template
        if properties:
            parameter_json['properties'] = properties
        if relate_id:
            parameter_json['relateId'] = relate_id
        result_flag, response = self.sending_request(url=url, headers=self._head, json_data=parameter_json)
        parameter_json.clear()
        return result_flag, response

    def query_mysql_result(self, json_res):
        result = None
        parameter_json = dict()
        url = self._url_prefix + self.mysql_query_result_path
        parameter_json['uniqueId'] = re.findall(r"'uniqueId': '(.*?)'", str(json_res))[0]
        result_flag, response = self.sending_request(url=url, headers=self._head, json_data=parameter_json, date_type=0)
        parameter_json.clear()
        if result_flag:
            # uniqueId\jsonResult
            result = response.get('data').get('jsonResult')
        return result

    def inspection_operating_conditions(self, sql, task_name, relate_id=None, alarm_user_id=None, properties=None,
                                        template=None):
        res_flag = False
        result = None
        result_flag, response = self.query_mysql(sql=sql, task_name=task_name, relate_id=relate_id, template=template,
                                                 alarm_user_id=alarm_user_id, properties=properties)
        if result_flag:
            describe_flag, fail_result = self.query_describe(response)
            if describe_flag:
                result = self.query_mysql_result(response)
                res_flag = True
            else:
                raise Exception(f"spark describe api failed and return failureDetail:{result}")
        return res_flag, result

    def execute_hql_handler(self, sql_list, task_name, flag, relate_id=None, alarm_user_id=None, properties=None,
                            template=None):
        res_flag = False
        result = None
        result_flag, response = self.seq_sql(sqls=sql_list, task_name=task_name, flag=flag, relate_id=relate_id,
                                             template=template, alarm_user_id=alarm_user_id, properties=properties)
        if result_flag:
            describe_flag, result = self.query_describe(response)
            if describe_flag:
                res_flag = True
            else:
                raise Exception(f"spark describe api failed and return failureDetail:{result}")
        return res_flag, result
