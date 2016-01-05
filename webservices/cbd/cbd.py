# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging

import suds
from suds.plugin import MessagePlugin
from suds.client import Client

logging.basicConfig(level=logging.ERROR)
logging.getLogger('suds.client').setLevel(logging.ERROR)


class LoginError(Exception): pass


class MyPlugin(MessagePlugin):
    def marshalled(self, context):
        context.envelope = context.envelope.prune()


class CBD(object):
    """ Simple class for pragmatic access to the BenefitPoint
        Web Services through python.

        :param username: Username to login to Benefit Point
        :param password: Password to login to Benefit Point

        Usage:
            from webservices import webservices
            bp = webservices.BenefitPoint(username='you@me.net', password='password')
            ## Create the complex type to pass into the method
            accountsearch = bp.create_type('ns1:AccountSearchCriteria')
            accountsearch.active = True

            ## Call the method and pass in the type
            accounts = bp.call('findAccounts', accountsearch)
            print(accounts)

        Returns:
            BenefitPoint object

    """

    def __init__(self, username=0, password=0, machinename=0, wsdl_url=''):
        self.wsdl_file = wsdl_url
        self.client = Client(self.wsdl_file)

        token = self.create_type('AuthHeader')
        token.Username = username
        token.Password = password
        token.Machinename = machinename

        self.client.set_options(soapheaders=token)

    def create_type(self, type_name):
        ''' Provides short hand functions in creating Complex Types

            Usage:
                # Create the object with login creds.
                bp = webservices.BenefitPoint(username='you@me.net', password='password')

                # Create the type to pass into the search
                accountsearch = bp.create_type('ns1:AccountSearchCriteria')
                accountsearch.active = True

            Returns:
                Complex Type

        '''

        return self.client.factory.create(type_name)

    def list_methods(self):
        url = self.wsdl_file
        client = suds.client.Client(self.wsdl_file)
        for service in client.wsdl.services:
            for port in service.ports:
                methods = port.methods.values()
                for method in methods:
                    print(method.name)
                    for part in method.soap.input.body.parts:
                        part_type = part.type
                        if (not part_type):
                            part_type = part.element[0]
                        print('  ' + str(part.name) + ': ' + str(part_type))
                        o = client.factory.create(part_type)
                        print('    ' + str(o))

    def get_client(self):
        return self.client

    def call(self, func, *args):
        ''' Pass in the method name and the search type object
            to call the method.

            Usage:
                from webservices import BenefitPoint
                bp = webservices.BenefitPoint(username='you@me.net', password='password')
                resp = bp.call('getTeamMembers', 1346911)

            Returns:
                results from method call

        '''

        try:
            if args:
                resp = getattr(self.client.service, func)(args, )
            else:
                resp = getattr(self.client.service, func)

        except suds.WebFault as detail:
            return "ERROR", detail

        return resp


if __name__ == '__main__':
    cbd = CBD()
