# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
import os


import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

import suds
from suds.plugin import MessagePlugin
from suds.client import Client

from .sagittaImportTemplates import *

logging.basicConfig(level=logging.CRITICAL)
logging.getLogger('suds.client').setLevel(logging.CRITICAL)


class LoginError(Exception): pass


class MyPlugin(MessagePlugin):
    def marshalled(self, context):
        context.envelope = context.envelope.prune()


# def sending(self, context):
#         context.envelope = re.sub('\s+<.*?/>', '', str(context.envelope))


class Sagitta(object):
    """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ams="http://amsservices.com/">
           <soapenv:Header>
              <ams:AuthenticationHeader>
                 <!--Optional:-->
                 <ams:Account>Live</ams:Account>
                 <!--Optional:-->
                 <ams:Username>afox</ams:Username>
                 <!--Optional:-->
                 <ams:Password>JAF1834</ams:Password>
                 <!--Optional:-->
                 <ams:Accesscode></ams:Accesscode>
                 <!--Optional:-->
                 <ams:Serverpool>websvc</ams:Serverpool>
                 <!--Optional:-->
                 <ams:Onlinecode></ams:Onlinecode>
              </ams:AuthenticationHeader>
           </soapenv:Header>
           <soapenv:Body>
              <ams:rolodexContains>
                 <!--Optional:-->
                 <ams:searchCriteria>deeds</ams:searchCriteria>
              </ams:rolodexContains>
           </soapenv:Body>
        </soapenv:Envelope>

        token = self.client.factory.create('SessionIdHeader')
        token.sessionId = self.sessionID
        self.client.set_options(soapheaders=token)
    """

    def __init__(self, account='', username='', password='', accessCode='', serverPool='', onlineCode='', wsServer=''):
        self.account = account
        self.username = username
        self.password = password
        self.accessCode = accessCode
        self.serverPool = serverPool
        self.onlineCode = onlineCode

        self.TRANSPORTER_WSDL = "http://{}/sagittaws/transporter.asmx?wsdl".format(wsServer)
        self.CLIENT_IMPORT_TEMPLATE = "sagitta/sagittaImportTemplates/Client Import Template.XML"
        self.CONTACT_IMPORT_TEMPLATE = "sagitta/sagittaImportTemplates/Contact Import Template.XML"
        self.MEMO_IMPORT_TEMPLATE = "sagitta/sagittaImportTemplates/Memo Import Template.XML"

        self.client = Client(self.TRANSPORTER_WSDL, plugins=[MyPlugin()])
        self.create_auth_header()

    def create_auth_header(self):
        token = self.client.factory.create('AuthenticationHeader')
        token.Account = self.account
        token.Username = self.username
        token.Password = self.password
        token.Accesscode = self.accessCode
        token.Serverpool = self.serverPool

        self.client.set_options(soapheaders=token)
        return token

    def logout(self):
        pass

    def create_type(self, type_name):
        return self.client.factory.create(type_name)

    def list_methods(self):
        """
            prints methods available
        :return:
        """

        output = []
        url = self.TRANSPORTER_WSDL
        client = suds.client.Client(url)
        for service in client.wsdl.services:
            for port in service.ports:
                methods = port.methods.values()
                for method in methods:
                    print(method.name)
                    output.append(method.name)
                    for part in method.soap.input.body.parts:
                        part_type = part.type
                        if (not part_type):
                            part_type = part.element[0]
                        print('  ' + str(part.name) + ': ' + str(part_type))
                        output.append('  ' + str(part.name) + ': ' + str(part_type))
                        o = client.factory.create(part_type)
                        print('    ' + str(o))
                        output.append('    ' + str(o))

        return '\n'.join(output)

    def get_client(self):
        return self.client

    def call(self, func, *args):
        """
            Pass in the method name and the search type object
            to call the method.

            Usage:
                from webservices import BenefitPoint
                bp = webservices.BenefitPoint(username='you@me.net', password='password')
                resp = bp.call('getTeamMembers', 1346911)

            Returns:
                results from method call

        """

        try:
            if args:
                resp = getattr(self.client.service, func)(args, )
            else:
                resp = getattr(self.client.service, func)

        except suds.WebFault as detail:
            return "ERROR", detail

        return resp

    def create_template(self, template_name=False):
        if template_name == 'memo':
            tree = ET.fromstring(sagittaMemoTemplate)
            return tree

    def prettify_xml(self, elem):
        elem = ET.tostring(elem)
        xml = minidom.parseString(elem)
        pretty_xml_as_string = xml.toxml()
        return pretty_xml_as_string.replace('<?xml version="1.0" ?><root>', '').replace('</root>', '').strip()