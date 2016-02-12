import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

layoutTemplate = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body>{}</soap:Body></soap:Envelope>""".strip()
sagittaMemoImportTemplate = """<PassThroughImp><XMLinput><PassThroughImp><XMLinput><Account/><Username/><Password/><Accesscode/><Serverpool/><ImportCode value="WSIMPORT"/><ImportRecord><CLIENTS><ImportBlock guid=""><CLIENT value=""><ClientCd></ClientCd><Reference></Reference></CLIENT><MEMO value=""><MemoInfoDesc><v1></v1><v2></v2></MemoInfoDesc><OtherStaffToCd><v1></v1><v2></v2><v3></v3></OtherStaffToCd><DistributionCd></DistributionCd><NumMemoDays></NumMemoDays><MemoDt></MemoDt><CompletedDt></CompletedDt><LetterCd></LetterCd><ClientCd></ClientCd><ClientName></ClientName><InsurerCd></InsurerCd><InsurerName></InsurerName><AddInterestsCd></AddInterestsCd><AddInterestsName></AddInterestsName><OtherCorrespondentName></OtherCorrespondentName><DocumentFormatCd></DocumentFormatCd><ContactCd></ContactCd><ContactName></ContactName><Salutation></Salutation><SecurityInd></SecurityInd><DocumentTypeCd></DocumentTypeCd><DocWPTypeCd></DocWPTypeCd><LetterShell></LetterShell><AuthorCd></AuthorCd><StaffCd></StaffCd><PolicyNumber></PolicyNumber></MEMO></ImportBlock></CLIENTS></ImportRecord></XMLinput></PassThroughImp></XMLinput></PassThroughImp>""".strip()
sagittaMemoRequestTemplate = """<PassThroughReq><XMLinput><PassThroughReq><XMLinput><Account/><Username/><Password/><Accesscode/><Serverpool/><ImportCode value="WSIMPORT"/><ImportRecord><CLIENTS><ImportBlock guid=""><CLIENT value=""><ClientCd></ClientCd><Reference></Reference></CLIENT><MEMO value=""><MemoInfoDesc><v1></v1><v2></v2></MemoInfoDesc><OtherStaffToCd><v1></v1><v2></v2><v3></v3></OtherStaffToCd><DistributionCd></DistributionCd><NumMemoDays></NumMemoDays><MemoDt></MemoDt><CompletedDt></CompletedDt><LetterCd></LetterCd><ClientCd></ClientCd><ClientName></ClientName><InsurerCd></InsurerCd><InsurerName></InsurerName><AddInterestsCd></AddInterestsCd><AddInterestsName></AddInterestsName><OtherCorrespondentName></OtherCorrespondentName><DocumentFormatCd></DocumentFormatCd><ContactCd></ContactCd><ContactName></ContactName><Salutation></Salutation><SecurityInd></SecurityInd><DocumentTypeCd></DocumentTypeCd><DocWPTypeCd></DocWPTypeCd><LetterShell></LetterShell><AuthorCd></AuthorCd><StaffCd></StaffCd><PolicyNumber></PolicyNumber></MEMO></ImportBlock></CLIENTS></ImportRecord></XMLinput></PassThroughReq></XMLinput></PassThroughReq>""".strip()
sagittaClientImportTemplate = """<PassThroughImp><XMLinput><PassThroughImp><XMLinput><Account/><Username/><Password/><Accesscode/><Serverpool/><ImportCode value="WSIMPORT"/><ImportRecord><CLIENTS><ImportBlock guid=""><CLIENT value=""><ClientCd></ClientCd><ClientName></ClientName><BillToCd></BillToCd><Addr1></Addr1><Addr2></Addr2><PostCd><PostalCode></PostalCode><PostalExtensionCode></PostalExtensionCode></PostCd><City></City><StateProvCd></StateProvCd><Phone1Number></Phone1Number><Phone2Number></Phone2Number><ReferenceCd></ReferenceCd><StatusCd><v1></v1><v2></v2><v3></v3></StatusCd><ProducerCd><Producer1Cd></Producer1Cd><Producer2Cd></Producer2Cd><Producer3Cd></Producer3Cd></ProducerCd><ServicerCd><Servicer1Cd></Servicer1Cd><Servicer2Cd></Servicer2Cd><Servicer3Cd></Servicer3Cd></ServicerCd><CreditTerms></CreditTerms><SourceCd></SourceCd><SourceDt></SourceDt><CatCd><Cat1Cd></Cat1Cd><Cat2Cd></Cat2Cd><Cat3Cd></Cat3Cd><Cat4Cd></Cat4Cd><Cat5Cd></Cat5Cd></CatCd><NetCommissionPct></NetCommissionPct><SICCd><v1></v1><v2></v2><v3></v3><v4></v4></SICCd><CommentaryRemarkText></CommentaryRemarkText><Phone1ExtensionNumber></Phone1ExtensionNumber><Phone2ExtensionNumber></Phone2ExtensionNumber><FaxNumber></FaxNumber><DateBusinessStarted></DateBusinessStarted><BusinessNature><v1></v1></BusinessNature><InspectionContact></InspectionContact><InspectionPhoneNumber></InspectionPhoneNumber><InspectionPhoneExtensionNumber></InspectionPhoneExtensionNumber><AccountingContact></AccountingContact><AccountingPhoneNumber></AccountingPhoneNumber><AccountingPhoneExtensionNumber></AccountingPhoneExtensionNumber><LegalEntityCd></LegalEntityCd><EmailAddr></EmailAddr><DivisionNumber></DivisionNumber><ContactMethod></ContactMethod><WebSiteLink></WebSiteLink></CLIENT></ImportBlock></CLIENTS></ImportRecord></XMLinput></PassThroughImp></XMLinput></PassThroughImp>""".strip()
sagittaPolicyRWLImportTemplate = """<PassThroughImp><XMLinput><PassThroughImp><XMLinput><Account/><Username/><Password/><Accesscode/><Serverpool/><ImportCode value="WSIMPORT" /><ImportRecord><CLIENTS><ImportBlock guid=""><CLIENT value=""><ClientCd></ClientCd><Reference></Reference></CLIENT><POLICY value=""><TransactionInformation><Guid></Guid><TransactionType>RWL</TransactionType><TransactionDate></TransactionDate><FollowupDays></FollowupDays></TransactionInformation><PolicyNumber></PolicyNumber><PolicyDesc></PolicyDesc><BillToCd></BillToCd><ClientCd></ClientCd><ClientName></ClientName><NamedInsured></NamedInsured><PolicyRemarkText><v1></v1><v2></v2><v3></v3><v4></v4></PolicyRemarkText><InsurerName></InsurerName><CoverageCd></CoverageCd><PolicyContractTermCd></PolicyContractTermCd><PolicyEffectiveDt></PolicyEffectiveDt><PolicyEffectiveLocalStandardTimeInd></PolicyEffectiveLocalStandardTimeInd><PolicyExpirationDt></PolicyExpirationDt><PolicyExpirationLocalStandardTimeInd></PolicyExpirationLocalStandardTimeInd><PolicyOriginalInceptionDt></PolicyOriginalInceptionDt><BinderEffectiveDt></BinderEffectiveDt><BinderStartTimeInd></BinderStartTimeInd><BinderExpirationDt></BinderExpirationDt><BinderExpirationTimeInd></BinderExpirationTimeInd><BillTypeCd></BillTypeCd><BinderPurposeCd></BinderPurposeCd><LastCommissionPct></LastCommissionPct><Producer><Producer1Cd></Producer1Cd><Producer2Cd></Producer2Cd><Producer3Cd></Producer3Cd></Producer><DivisionCd></DivisionCd><StateProvCd></StateProvCd><AuditTermCd></AuditTermCd><ServicerCd></ServicerCd><DepartmentCd></DepartmentCd><SICCd></SICCd><DateBusinessStarted></DateBusinessStarted><NatureBusinessCd><v1></v1><v2></v2><v3></v3></NatureBusinessCd><GeneralInfoRemarkText><v1></v1><v2></v2><v3></v3><v4></v4></GeneralInfoRemarkText><PersonalSupplementalInfo><NumCurrentAddrYrs></NumCurrentAddrYrs><PreviousAddr1></PreviousAddr1><PreviousAddr2></PreviousAddr2><PreviousPostalCd><PreviousPostalCode></PreviousPostalCode><PreviousPostalExtensionCode></PreviousPostalExtensionCode></PreviousPostalCd><PreviousCity></PreviousCity><PreviousStateProvCd></PreviousStateProvCd><CurrentResidenceDt></CurrentResidenceDt><PreviousResidenceDt></PreviousResidenceDt></PersonalSupplementalInfo><InsuredInfo><BirthDt></BirthDt><TaxId></TaxId><NumResidentsInHousehold></NumResidentsInHousehold><NamedIndividuals></NamedIndividuals><MaritalStatusCd></MaritalStatusCd><OccupationClassCd></OccupationClassCd><OccupationDesc></OccupationDesc><LengthTimeEmployed></LengthTimeEmployed><HouseholdIncomeAmt></HouseholdIncomeAmt><CommercialName></CommercialName><LengthTimeWithPreviousEmployer></LengthTimeWithPreviousEmployer><LengthTimeCurrentOccupation></LengthTimeCurrentOccupation></InsuredInfo><General1QuestionCd><NumVehsInHousehold></NumVehsInHousehold><LengthTimeKnownByAgentBroker></LengthTimeKnownByAgentBroker><AutoClubMemberYesNoCd></AutoClubMemberYesNoCd><UMPDRejectionYesNoCd></UMPDRejectionYesNoCd><UnderinsMotoristRejectionYesNoCd></UnderinsMotoristRejectionYesNoCd><AnyLossesAccidentsConvictionsIndYesNoCd></AnyLossesAccidentsConvictionsIndYesNoCd><ResidenceOwnedRentedCd></ResidenceOwnedRentedCd></General1QuestionCd><CoInsuredInfo><CoInsuredBirthDt></CoInsuredBirthDt><CoInsuredTaxId></CoInsuredTaxId><CoInsuredMaritalStatusCd></CoInsuredMaritalStatusCd><CoInsuredOccupationClassCd></CoInsuredOccupationClassCd><CoInsuredOccupationDesc></CoInsuredOccupationDesc><CoInsuredLengthTimeWithCurrentEmployer></CoInsuredLengthTimeWithCurrentEmployer><CoInsuredCommercialName></CoInsuredCommercialName><CoInsuredLengthTimeWithPreviousEmployer></CoInsuredLengthTimeWithPreviousEmployer><CoInsuredLengthTimeCurrentOccupation></CoInsuredLengthTimeCurrentOccupation></CoInsuredInfo><BusinessIncomeTypeBusinessCd></BusinessIncomeTypeBusinessCd><PolicyTypeCd></PolicyTypeCd><PayeeCd></PayeeCd><PolicySource></PolicySource><CarrierProducerSubCode></CarrierProducerSubCode></POLICY></ImportBlock></CLIENTS></ImportRecord></XMLinput></PassThroughImp></XMLinput></PassThroughImp>""".strip()
tempTemplate = """<PassThroughReq><XMLinput><PassThroughReq><XMLinput><Account/><Username/><Password/><Accesscode/><Serverpool/><INPUT><Files><File name="ACF"><Items><Item key="SYS"></Item></Items></File></Files></INPUT></XMLinput></PassThroughReq></XMLinput></PassThroughReq>""".strip()


class Template(object):
    def __init__(self, template_name=None, **kw):
        self.template_name = template_name
        self.hashMap = dict(
            memoImport=sagittaMemoImportTemplate,
            memoRequest=sagittaMemoRequestTemplate,
            clientImport=sagittaClientImportTemplate,
            policyRWLImport=sagittaPolicyRWLImportTemplate,
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
