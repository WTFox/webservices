import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

layoutTemplate = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body>{}</soap:Body></soap:Envelope>""".strip()
sagittaMemoImportTemplate = """<PassThroughImp><XMLinput><PassThroughImp><XMLinput><Account/><Username/><Password/><Accesscode/><Serverpool/><ImportCode value="WSIMPORT"/><ImportRecord><CLIENTS><ImportBlock guid=""><CLIENT value=""><ClientCd></ClientCd><Reference></Reference></CLIENT><MEMO value=""><MemoInfoDesc><v1></v1><v2></v2></MemoInfoDesc><OtherStaffToCd><v1></v1><v2></v2><v3></v3></OtherStaffToCd><DistributionCd></DistributionCd><NumMemoDays></NumMemoDays><MemoDt></MemoDt><CompletedDt></CompletedDt><LetterCd></LetterCd><ClientCd></ClientCd><ClientName></ClientName><InsurerCd></InsurerCd><InsurerName></InsurerName><AddInterestsCd></AddInterestsCd><AddInterestsName></AddInterestsName><OtherCorrespondentName></OtherCorrespondentName><DocumentFormatCd></DocumentFormatCd><ContactCd></ContactCd><ContactName></ContactName><Salutation></Salutation><SecurityInd></SecurityInd><DocumentTypeCd></DocumentTypeCd><DocWPTypeCd></DocWPTypeCd><LetterShell></LetterShell><AuthorCd></AuthorCd><StaffCd></StaffCd><PolicyNumber></PolicyNumber></MEMO></ImportBlock></CLIENTS></ImportRecord></XMLinput></PassThroughImp></XMLinput></PassThroughImp>""".strip()
sagittaMemoRequestTemplate = """<PassThroughReq><XMLinput><PassThroughReq><XMLinput><Account/><Username/><Password/><Accesscode/><Serverpool/><ImportCode value="WSIMPORT"/><ImportRecord><CLIENTS><ImportBlock guid=""><CLIENT value=""><ClientCd></ClientCd><Reference></Reference></CLIENT><MEMO value=""><MemoInfoDesc><v1></v1><v2></v2></MemoInfoDesc><OtherStaffToCd><v1></v1><v2></v2><v3></v3></OtherStaffToCd><DistributionCd></DistributionCd><NumMemoDays></NumMemoDays><MemoDt></MemoDt><CompletedDt></CompletedDt><LetterCd></LetterCd><ClientCd></ClientCd><ClientName></ClientName><InsurerCd></InsurerCd><InsurerName></InsurerName><AddInterestsCd></AddInterestsCd><AddInterestsName></AddInterestsName><OtherCorrespondentName></OtherCorrespondentName><DocumentFormatCd></DocumentFormatCd><ContactCd></ContactCd><ContactName></ContactName><Salutation></Salutation><SecurityInd></SecurityInd><DocumentTypeCd></DocumentTypeCd><DocWPTypeCd></DocWPTypeCd><LetterShell></LetterShell><AuthorCd></AuthorCd><StaffCd></StaffCd><PolicyNumber></PolicyNumber></MEMO></ImportBlock></CLIENTS></ImportRecord></XMLinput></PassThroughReq></XMLinput></PassThroughReq>""".strip()
tempTemplate = """<PassThroughReq><XMLinput><PassThroughReq><XMLinput><Account/><Username/><Password/><Accesscode/><Serverpool/><INPUT><Files><File name="ACF"><Items><Item key="SYS"></Item></Items></File></Files></INPUT></XMLinput></PassThroughReq></XMLinput></PassThroughReq>""".strip()


class Template(object):
    def __init__(self, template_name=None, **kw):
        self.template_name = template_name
        self.hashMap = dict(
            memoImport=sagittaMemoImportTemplate,
            memoRequest=sagittaMemoRequestTemplate,
            temp=tempTemplate
        )

        self.tree = ET.fromstring(self.hashMap[template_name])
        self.tree.attrib['xmlns'] = "http://amsservices.com/"

        try:
            self.tree.find("XMLinput").find("PassThroughImp").attrib['xmlns'] = "http://amsservices.com/"
            self.base = self.tree.find("XMLinput").find("PassThroughImp").find("XMLinput")

        except:
            self.tree.find("XMLinput").find("PassThroughReq").attrib['xmlns'] = "http://amsservices.com/"
            self.base = self.tree.find("XMLinput").find("PassThroughReq").find("XMLinput")

        self.base.find("Account").attrib['value'] = kw['account']
        self.base.find("Username").attrib['value'] = kw['username']
        self.base.find("Password").attrib['value'] = kw['password']
        self.base.find("Accesscode").attrib['value'] = kw['accessCode']
        self.base.find("Serverpool").attrib['value'] = kw['serverPool']

    @property
    def full_request(self):
        return layoutTemplate.format(str(self))

    def prettify_xml(self, elem):
        elem = ET.tostring(elem)
        xml = minidom.parseString(elem)
        pretty_xml_as_string = xml.toxml()
        return pretty_xml_as_string.replace('<?xml version="1.0" ?>', "")

    def __str__(self):
        return self.prettify_xml(self.tree)

    def __repr__(self):
        return "<Template %s at 0x%x>" % (repr(self.hashMap[self.template_name]), id(self))
