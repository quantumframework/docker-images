#!/usr/bin/python
import yaml
from lxml import etree
from io import StringIO, BytesIO


class FilterModule(object):
    nsmap = {
        'dsig': "http://www.w3.org/2000/09/xmldsig#"
    }

    def filters(self):
        return {
            'parse_idpsso': self.parse_idpsso
        }

    def parse_idpsso(self, xml):
        root = etree.fromstring(xml.encode())
        idp = {
            'entity_id': root[0].attrib['entityID'],
            'x509cert': root.xpath('//*[local-name()="X509Certificate"]')[0].text,
            'url': self.get_sso_url(root.xpath('//*[local-name()="SingleSignOnService"][@Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"]'))
        }
        return idp

    def get_sso_url(self, elements):
        return elements[0].attrib['Location']
