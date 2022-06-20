# coding = utf-8
import json

import requests
from config.excel_reader import ExcelReader
import urllib3

urllib3.disable_warnings()


class RequestUtil:
    def send_rquest(self, method, url, data=None, headers=None, req_params_type=None, **kwargs):
        # if method == 'post':
        #     if req_params_type == 'json':
        #         response = getattr(requests, method)(url, json=data, headers=headers, verify=False, **kwargs).json()
        #     else:
        #         response = getattr(requests, method)(url, data=data, headers=headers, verify=False, **kwargs).json()
        # else:
        #     response = getattr(requests, method)(url, params=data, headers=headers, verify=False, **kwargs).json()
        # return response

        if req_params_type == 'json':
            try:
                data_str = json.dumps(data, ensure_ascii=False)  # 要求不要把汉字变成ASCII码
                data = eval(data_str)
            except Exception as e:
                raise Exception("无法转换为JSON格式，请检查你输入参数_{}".format(e))
            response = getattr(requests, method)(url, json=data, headers=headers, verify=False, **kwargs).json()
        elif req_params_type == 'data':
            response = getattr(requests, method)(url, data=data, headers=headers, verify=False, **kwargs).json()
        else:
            response = getattr(requests, method)(url, params=data, headers=headers, verify=False, **kwargs).json()
        return response


if __name__ == '__main__':
    reader = ExcelReader()
    models = reader.reader('Sheet1')
    for model in models:
        request_test = RequestUtil()
        response = request_test.send_rquest(model.method, model.url_host + model.url_adr, model.data, model.headers,
                                            model.req_param_type)
        print(response)
