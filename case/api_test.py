# coding = utf-8
from datetime import datetime
import time
from util.request_util import RequestUtil
from config.excel_reader import ExcelReader
from util.send_mail import SendMail
from config.readconfig_yaml import ReadConfigYaml
import json
from util.log_util import Log
import jsonpath
import pytest


class CommonTestCase:
    # 1、根据用例id，更新响应内容和测试内容
    def __init__(self):
        log = Log()
        self.logger = log.get_log()

    def updateResultByCaseId(self, case_name, model, run_result, result_msg, response):
        """
        根据用例id，更新响应内容和测试内容
        :param case_name: 用例sheet名称
        :param model: 用例对象
        :param run_result: 执行结果
        :param result_msg: 结果详情
        :param response: 响应内容
        :return:
        """
        current_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        reader = ExcelReader()
        if run_result == 'pass':
            reader.update_case(case_name, model, run_result, result_msg, '', current_time)
            self.logger.info('用例{}执行结果更新完成'.format(model.case_id))


        else:
            reader.update_case(case_name, model, run_result, result_msg, json.dumps(response, ensure_ascii=False),
                               current_time)
            self.logger.info('用例{}执行结果更新完成'.format(model.case_id))

    # 2、执行全部用例的入口
    def runAllcase(self, case_name, models, **kwargs):
        """
        执行全部用例的入口
        :param case_name: 用例sheet名称
        :param models: 用例对象集合
        :param kwargs: 扩张参数
        :return:
        """
        for model in models:
            # print(model)
            if model.is_run == 'yes':
                try:
                    # 执行用例
                    response = self.runCase(models, model, **kwargs)
                    # 响应断言
                    if len(response) == 1:
                        # 更新结果储存数据库
                        self.updateResultByCaseId(case_name, model, 'fail', response['msg'], response)
                    else:
                        assert_msg = self.assertResponse(model, response)
                        # 更新结果储存数据库
                        self.updateResultByCaseId(case_name, model, assert_msg['is_pass'], assert_msg['msg'], response)
                except Exception as e:
                    self.logger.error("异常日志——用例编号：{0}, 用例标题：{1}, 异常：{2}".format(model.case_id, model.title, e))

        # 发送测试报告
        reader = ExcelReader()
        models = reader.reader('Sheet1')
        self.sendTestPeport(models)

    # 3、执行单个用例
    def runCase(self, models, model, **kwargs):
        """
        执行单个用例
        :param models: 用例对象集合
        :param model: 用例对象
        :param kwargs: 扩展参数
        :return:
        """
        # 是否有前置条件
        if model.pre_case_id > 0:
            self.logger.info('用例{0}有前置用例:用例{1}'.format(model.case_id,model.pre_case_id))
            pre_model = models[model.pre_case_id - 1]
            # 递归调用
            pre_response = self.runCase(models, pre_model, **kwargs)
            self.logger.info('前置用例{}请求完成'.format(model.pre_case_id))
            # 前置条件断言
            pre_assert_msg = self.assertResponse(pre_model, pre_response)
            response = {}
            if pre_assert_msg["is_pass"] != 'pass':
                # 前置条件不通过，直接返回
                response["msg"] = "前置用例执行不通过——" + pre_response["msg"]
                self.logger.info('前置用例{0}执行不通过：{1}'.format(model.pre_case_id,pre_response["msg"]))
                return response
            # 判断需要case前置条件的是哪个字段
            pre_fields = model.pre_fields
            for pre_field in pre_fields:
                # print(pre_field)
                if pre_field["scope"] == "header":
                    # 遍历headers，替换对应的字段值，即寻找同名的字段
                    for header in model.headers:
                        field_name = pre_field["field"]
                        if header == field_name:
                            field_value = pre_response["data"][field_name]
                            model.headers[field_name] = field_value
                            self.logger.info('用例{0}的请求头中前置参数：{1}_参数值：{2}获取成功'.format(model.case_id,field_name,field_value))
                            break
                elif pre_field["scope"] == "body":
                    for r_body in model.data:
                        field_name = pre_field["field"]
                        if r_body == field_name:
                            field_value = pre_response["data"][field_name]
                            model.data[field_name] = field_value
                            self.logger.info(
                                '用例{0}的请求参数中前置参数：{1}_参数值：{2}获取成功'.format(model.case_id, field_name, field_value))
                            break

        # 发起请求
        req = RequestUtil()
        response = req.send_rquest(model.method, model.url_host + model.url_adr, model.data, model.headers,
                                   model.req_param_type, **kwargs)
        self.logger.info('用例{0}请求完成,响应内容：{1}'.format(model.case_id,response))
        return response

    # 4、断言响应内容，更新用例执行情况
    def assertResponse(self, model, response):
        """
        断言响应内容，更新用例执行情况
        :param model: 用例对象
        :param response: 响应内容
        :return:
        """
        assert_type = model.assert_type
        assert_value = model.assert_value
        run_result = ''
        if assert_type == "code":
            response_code = response["code"]
            if int(assert_value) == response_code:
                run_result = 'pass'
                self.logger.info('用例{}测试通过'.format(model.case_id))
            else:
                run_result = 'fail'
                self.logger.info('用例{}测试不通过'.format(model.case_id))
        elif assert_type == "data_json_list":
            data_array = response["data"]
            if data_array is not None and isinstance(data_array, list) and len(data_array) == int(assert_value):
                run_result = 'pass'
                self.logger.info('用例{}测试通过'.format(model.case_id))
            else:
                run_result = 'fail'
                self.logger.info('用例{}测试不通过'.format(model.case_id))
        elif assert_type == "data_json_dict":
            data = response["data"]
            if data is not None and isinstance(data, dict) and len(data) == int(assert_value):
                run_result = 'pass'
                self.logger.info('用例{}测试通过'.format(model.case_id))
            else:
                run_result = 'fail'
                self.logger.info('用例{}测试不通过'.format(model.case_id))
        elif assert_type == "code&data_json_dict":
            response_code = response["code"]
            data = response["data"]
            if int(assert_value) == response_code:
                if data is not None and isinstance(data, dict) and len(data) > 0:
                    run_result = 'pass'
                    self.logger.info('用例{}测试通过'.format(model.case_id))
                else:
                    run_result = 'fail'
                    self.logger.info('用例{}测试不通过'.format(model.case_id))
            else:
                run_result = 'fail'
                self.logger.info('用例{}测试不通过'.format(model.case_id))
        elif assert_type == "code&data_json_list":
            response_code = response["code"]
            data_array = response["data"]
            if int(assert_value) == response_code:
                if data_array is not None and isinstance(data_array, list) and len(data_array) > 0:
                    run_result = 'pass'
                    self.logger.info('用例{}测试通过'.format(model.case_id))
                else:
                    run_result = 'fail'
                    self.logger.info('用例{}测试不通过'.format(model.case_id))
            else:
                run_result = 'fail'
                self.logger.info('用例{}测试不通过'.format(model.case_id))

        msg = "模块:{0}, 标题:{1}, 断言类型是:{2}, 响应msg:{3}".format(model.module, model.title,
                                                            model.assert_type, response["msg"])
        # 拼装信息
        assert_msg = {"is_pass": run_result, "msg": msg}
        self.logger.info('断言拼装信息：{}'.format(assert_msg))
        return assert_msg

    # 5、发送邮件，测试报告
    def sendTestPeport(self, models):
        """
        发送邮件，测试报告
        :param models: 用例对象集合
        :return:
        """
        content = """
        <html><body>
            <h1>{0} 接口测试报告：</h1>
            <h2>总用例数:{3} pass用例数:<span style="color:green">{4}</span> fail用例数:<span style="color:red">{5}</span> 通过率:<span style="color:blue">{6:.2f}%</span></h2>
            <h3>pass用例</h3>
            <table border="1">
            <tr>
              <th>编号</th>
              <th>模块</th>
              <th>标题</th>
              <th>是否通过</th>
              <th>备注</th>
              <th>响应</th>
            </tr>
            {1}
            </table>
            <h3>fail用例</h3>
            <table border="1">
            <tr>
              <th>编号</th>
              <th>模块</th>
              <th>标题</th>
              <th>是否通过</th>
              <th>备注</th>
              <th>响应</th>
            </tr>
            {2}
            </table>
            </body></html>  
        """
        template_true = ""
        template_false = ""
        total_num = len(models)
        pass_num = 0
        fail_num = 0
        for model in models:
            if model.run_result == 'pass':
                template_true += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>".format(
                    model.case_id, model.module, model.title, model.run_result, model.result_msg, model.response)
                pass_num += 1
            elif model.run_result == 'fail':
                template_false += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>".format(
                    model.case_id, model.module, model.title, model.run_result, model.result_msg, model.response)
                fail_num += 1
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = content.format(current_time, template_true, template_false, total_num, pass_num, fail_num,
                                 (pass_num / total_num) * 100)
        config_yaml = ReadConfigYaml()
        mail_host = config_yaml.get_db("Mail-Config", "mail_host")
        mail_title = config_yaml.get_db("Mail-Config", "mail_title")
        mail_sender = config_yaml.get_db("Mail-Config", "mail_sender")
        mail_auth_code = config_yaml.get_db("Mail-Config", "mail_auth_code")
        mail_receivers = config_yaml.get_db("Mail-Config", "mail_receivers")
        mail = SendMail(mail_host)
        mail.send(mail_title, content, mail_sender, mail_auth_code, mail_receivers)
        self.logger.info('测试结果邮件发送成功')
