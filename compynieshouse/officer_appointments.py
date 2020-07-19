from datagrab.retrieve_response.retrieve_response import RetrievedResponse
from datagrab.interpret_response.interpret_json_response import (
JsonResponseInterpreter)
from datagrab.RESTConnect.basicAuth import BasicAuth

class OfficerAppointments(JsonResponseInterpreter):
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

    def __init__(self, appKey: str, officer_id: str, request_timeout=15.,
                additional_request_kwargs=None):

        self.basicAuthHeader      = BasicAuth(appKey).basicAuthHeader
        self.request_kwargs       = {"headers": self.basicAuthHeader}

        if additional_request_kwargs:
            if'headers' not in additional_request_kwargs.keys():
                self.request_kwargs   = {**self.request_kwargs,
                                     **additional_request_kwargs}
            else:
                raise Exception("""BasicAuth provides the header based on the appkey
                                that you provide as first argument in CompanyOfficers""")
        else:
            pass


        self.officer_id         = officer_id
        self.request_timeout    = request_timeout

        self.build_url()
        self.retrieve_officer_data()

        super().__init__(self.appointments_response)

    def build_url(self):
        """
        Creates self.request_url and adds parameters to request_kwargs if
        self.by is set to "friendly_string"

        Called when parent class is instantiated
        """

        self.request_url = "https://api.companieshouse.gov.uk/officers/"\
                           "{officer_id}/appointments".format(
                    officer_id=self.officer_id
                    )

    def retrieve_officer_data(self):
        """

        """

        self.rr = RetrievedResponse(url=self.request_url,
                                    request_kwargs=self.request_kwargs)

        self.rr.getResponse(timeout=self.request_timeout)

        self.appointments_response = self.rr.response
