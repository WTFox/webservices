# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
import html

import requests
import xmltodict
import suds
from suds.plugin import MessagePlugin
from suds.client import Client

from .sagittaImportTemplates import *

logging.basicConfig(level=logging.CRITICAL)
logging.getLogger('suds.client').setLevel(logging.CRITICAL)


class LoginError(Exception): pass


class RemoveEmptyElements(MessagePlugin):
    def marshalled(self, context):
        context.envelope = context.envelope.prune()

    def sending(self, context):
        return context.envelope


class Sagitta(object):
    def __init__(self, account='', username='', password='', accessCode='', serverPool='', onlineCode='', wsServer=''):
        """
            A suds-jurko wrapper to allow interfacing with Sagitta SOAP services easier.
            This currently only supports in house installations

        :param account: Usually 'gemdata'.
        :param username: Sagitta username
        :param password: Sagitta password
        :param accessCode: I believe this is used only for hosted Sagitta.
        :param serverPool: The name of the pool set in your Sagitta IIS box.
        :param onlineCode: I believe this is used only for hosted Sagitta.
        :param wsServer: If in-house, name of sagitta web services server.
        """

        self.account = account
        self.username = username
        self.password = password
        self.accessCode = accessCode
        self.serverPool = serverPool
        self.onlineCode = onlineCode

        self.loginCreds = dict(
            account=account,
            username=username,
            password=password,
            accessCode=accessCode,
            serverPool=serverPool,
            onlineCode=onlineCode
        )

        self.TRANSPORTER_WSDL = "http://{}/sagittaws/transporter.asmx?wsdl".format(wsServer)

        self.client = Client(self.TRANSPORTER_WSDL, plugins=[RemoveEmptyElements()])
        self.client.set_options(nosend=True)
        self.create_auth_header()
        return

    def create_auth_header(self):
        """
            Creates the authentication header to be injected into each request.

            ex:
                <soapenv:Header>
                  <ams:AuthenticationHeader>
                     <!--Optional:-->
                     <ams:Account></ams:Account>
                     <!--Optional:-->
                     <ams:Username></ams:Username>
                     <!--Optional:-->
                     <ams:Password></ams:Password>
                     <!--Optional:-->
                     <ams:Accesscode></ams:Accesscode>
                     <!--Optional:-->
                     <ams:Serverpool></ams:Serverpool>
                     <!--Optional:-->
                     <ams:Onlinecode></ams:Onlinecode>
                  </ams:AuthenticationHeader>
               </soapenv:Header>

        :return:
            Returns the header if needed.
        """

        token = self.client.factory.create('AuthenticationHeader')
        token.Account = self.account
        token.Username = self.username
        token.Password = self.password
        token.Accesscode = self.accessCode
        token.Serverpool = self.serverPool

        self.client.set_options(soapheaders=token)
        return token

    def create_type(self, type_name):
        """
            Creates a complex type of 'type_name'

        :param type_name: a complex type that the wsdl supports
        :return: the complex type object to be modified
        """

        return self.client.factory.create(type_name)

    def list_methods(self):
        """
            prints methods available
        :return: a list of methods in a python list object if needed.
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
        """
            To be used if there is an issue with the Sagitta class 'call' function
        :return:
        """
        return self.client

    def call(self, func, *args):
        """
            Pass in the method name and the search type object
            to call the method.

            Usage:
                from webservices import Sagitta
                s = Sagitta(**logins.sagitta)
                resp = s.call('rolodexStartsWith', 'deed')

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
        return Template(template_name, **self.loginCreds)

    def passthrough(self, template_obj):
        url = self.TRANSPORTER_WSDL
        headers = {'content-type': 'text/xml'}
        request = template_obj.full_request

        response = requests.post(url, data=request, headers=headers)
        unescaped = html.unescape(response.text).replace('<?xml version="1.0"?>', '').replace('http://amsservices.com/', '')
        response = ET.fromstring(unescaped)

        try:
            return xmltodict.parse(ET.tostring(response), process_namespaces=False)['ns0:Envelope']['ns0:Body']['PassThroughReqResponse']
        except:
            return xmltodict.parse(ET.tostring(response), process_namespaces=False)
