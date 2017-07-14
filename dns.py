#!/usr/bin/python
#-*- coding:utf-8 -*-
'''update the ali dns'''

import json
import logger
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import AddDomainRecordRequest
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

    def add_dns_record(self, host, domain, record_ip):
        '''as name'''
        request = AddDomainRecordRequest.AddDomainRecordRequest()
        request.set_DomainName(domain)
        request.set_RR(host)
        request.set_Type('A') # can add A record only
        request.set_Value(record_ip)
        response = self._client.do_action_with_exception(request)
        logger.log(response)
        return json.loads(response)['RecordId']

    def get_dns_record(self, host, domain):
        '''as name'''
        request = DescribeSubDomainRecordsRequest.DescribeSubDomainRecordsRequest()
        request.set_SubDomain(host + '.' + domain)
        response = self._client.do_action_with_exception(request)
        logger.log(response)
        record = json.loads(response)['DomainRecords']['Record']
        if not record:
            return None
        else:
            return record[0]['RecordId']

    def get_dns_ip(self, record):
        '''print the log'''
        request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
        request.set_RecordId(record)
        response = self._client.do_action_with_exception(request)
        logger.log(response)
        return json.loads(response)['Value']

    def update(self, record, host, record_ip):
        '''update record'''
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_RecordId(record)
        request.set_RR(host)  # RR is the Host record
        request.set_Type('A')
        request.set_Value(record_ip)
        response = self._client.do_action_with_exception(request)
        logger.log(response)
        return response
