# coding = utf-8
class RequestModel:
    """
    case_id : 用例id
    url_host : 请求域名
    url_adr : 请求路径
    module : 模块
    title : 标题
    is_run : 是否执行
    method : 请求方法
    req_param_type : 传参方式
    pre_case_id :  前置用例id
    pre_fields : 前置的字段 获取请求结果的哪个字段，用于当前case的header还是body
    headers : 请求头
    data : 请求参数
    assert_type : 断言类型
    assert_value : 断言对比值
    run_result : 执行结果
    result_msg : 执行结果详情
    response : 响应内容 （用例执行失败时填充）
    update_time : 更新时间
    """

    case_id = None
    url_host = None
    url_adr = None
    module = None
    title = None
    is_run = None
    method = None
    req_param_type = None
    pre_case_id = None
    pre_fields = None
    headers = None
    data = None
    assert_type = None
    assert_value = None
    run_result = None
    result_msg = None
    response = None
    update_time = None

