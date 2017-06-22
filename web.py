#!/usr/bin/python
# -*- coding: UTF-8 -*-
''' web module. use to receive web request '''

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  # 导入HTTP处理相关的模块
from dns import Dns
from properties import load_properties_dict
import logger

# 自定义处理程序，用于处理HTTP请求

PROPS = load_properties_dict('setting.properties')


class HTTPHandler(BaseHTTPRequestHandler):
    '''handle the htpp request'''
    _dns = Dns(PROPS.get('region'), PROPS.get('key'), PROPS.get('secret'))
    _addr_record = {}
    _record_ip = {}

    def do_GET(self):
        '''处理GET请求'''

        # easy to use
        dns = HTTPHandler._dns
        addr_record = HTTPHandler._addr_record
        record_ip = HTTPHandler._record_ip
        html = 'sucess'

        # resolve request info: client ip and request params
        request_ip = str(self.client_address[0])
        query_str = self.path[2:].strip().split('&')
        params = {}  # request parameters dictionary
        for param in query_str:
            key_val = param.strip().split('=')
            if len(key_val) > 1:
                params[key_val[0]] = key_val[1]
            else:
                params[key_val[0]] = ''

        token = params.get('token')  # verify is the token valide
        record = params.get('record')
        host = params.get('host')
        domain = params.get('domain')

        if not token or token != PROPS.get('token'):
            html = 'invalid request'
        elif not host:
            html = 'dns host is necessary'
        else:
            passed = 1  # If the parameter is not complete, will not update
            if not record:  # get record
                if not domain:
                    html = 'missing dns record and domain'
                    passed = 0 # will not update dns record
                else:
                    host_domain = '%s.%s' % (host, domain)
                    if addr_record.has_key(host_domain):
                        record = addr_record.get(host_domain)
                    else:
                        record = self._dns.get_dns_record(host, domain)
                        # add in address record dictionary
                        addr_record[host_domain] = record
            if passed == 1:
            # update dns record
                try:
                    if not record_ip.has_key(record):
                        record_ip[record] = dns.get_dns_ip(
                            record)  # get dns ip and store it
                    if record_ip[record] != request_ip:
                        dns.update(record, host, request_ip)
                        record_ip[record] = request_ip
                except Exception, ex:
                    html = 'failure:' + str(ex)

        # 页面输出模板字符串
        self.send_response(200)  # 设置响应状态码
        self.send_header("text", "Contect")  # 设置响应头
        self.end_headers()
        self.wfile.write(html)  # 输出响应内容


def start_server(ipaddress, port):
    '''启动服务函数'''
    http_server = HTTPServer((ipaddress, int(port)), HTTPHandler)
    http_server.serve_forever()  # 设置一直监听并接收请求


start_server(PROPS.get('ipaddress'), PROPS.get('port'))  # 启动服务，监听8001端口
