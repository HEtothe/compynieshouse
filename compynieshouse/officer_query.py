from datagrab.retrieve_response.retrieve_response import RetrievedResponse
from datagrab.interpret_response.interpret_json_response import (
JsonResponseInterpreter)
from datagrab.RESTConnect.basicAuth import BasicAuth

class CompanyOfficers(JsonResponseInterpreter):
    """
    Company officers

    Class to retrieve data about the officers of a given company using the
    Companies House REST API.
    ----------------------------------------------------------------------
    args:
        appKey: string
        Your companies house API key

        company_code: string
        The companies house company code of the target entity

    """

    def __init__(self, appKey: str, company_code: str, request_timeout=15.):

        self.basicAuthHeader      = BasicAuth(appKey).basicAuthHeader
        self.request_kwargs       = {"headers": self.basicAuthHeader}
        self.target_entity_code   = company_code
        self.request_timeout      = request_timeout

        self.build_url()
        self.retrieve_officer_data()

        super().__init__(self.officers_response)

    def build_url(self):
        """
        Creates self.request_url and adds parameters to request_kwargs if
        self.by is set to "friendly_string"

        Called when parent class is instantiated
        """

        self.request_url = "https://api.companieshouse.gov.uk/company/"\
                    "{company_number}/officers".format(
                    company_number=self.target_entity_code
                    )

    def retrieve_officer_data(self):
        """

        """

        self.rr = RetrievedResponse(url=self.request_url,
                                    request_kwargs=self.request_kwargs)

        self.rr.getResponse(timeout=self.request_timeout)

        self.officers_response = self.rr.response
