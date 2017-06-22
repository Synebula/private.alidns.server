#!/usr/bin/python
#-*- coding:utf-8 -*-
'''update the ali dns'''

import json
import logger
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordInfoRequest


class Dns(object):
    '''update dns'''

    def __init__(self, region, key, secret):
        self._region = region
        self._key = key  # Access Key ID
        self._secret = secret  # Access Key Secret
        self._client = client.AcsClient(self._key, self._secret, self._region)

    def get_dns_record(self, host, domain):
        '''as name'''
        request = DescribeSubDomainRecordsRequest.DescribeSubDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_SubDomain(host + '.' + domain)
        response = self._client.do_action_with_exception(request)
        logger.log(response)
        return json.loads(response)['DomainRecords']['Record'][0]['RecordId']

    def get_dns_ip(self, record):
        '''print the log'''
        request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
        request.set_RecordId(record)
        request.set_accept_format('json')
        response = self._client.do_action_with_exception(request)
        logger.log(response)
        return json.loads(response)['Value']

    def update(self, record, host, update_ip):
        '''update record'''
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_RecordId(record)
        request.set_RR(host)  # RR is the Host record
        request.set_Type('A')
        request.set_Value(update_ip)
        request.set_accept_format('json')
        response = self._client.do_action_with_exception(request)
        logger.log(response)
        return response
