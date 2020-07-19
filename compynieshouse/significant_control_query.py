from datagrab.retrieve_response.retrieve_response import RetrievedResponse
from datagrab.interpret_response.interpret_json_response import (
JsonResponseInterpreter)
from datagrab.RESTConnect.basicAuth import BasicAuth


class SignificantControlQuery(BasicAuth, RetrievedResponse, JsonResponseInterpreter):

    def __init__(self, appKey: str, company_code: str, person_type="all",
                request_timeout=15.,additional_request_kwargs=None,
                 person_id=None):

        assert person_type in ["all", "individual", "corporate-entity"],\
            "kwarg person_type must be one of 'all', 'individual', 'corporate-entity'"

        BasicAuth.__init__(self, user=appKey)

        self.company_code   = company_code
        self.person_type    = person_type
        self.person_id      = person_id
        self.additional_request_kwargs = additional_request_kwargs

        # Ensure that we incorporate other kwargs like params, proxies etc.
        # are included in the http request
        self.build_request_kwargs()


        # Build the URL based on the person_type that the user is interested in
        self.build_url()

        # Submit the get request and generate the response
        RetrievedResponse.__init__(self, self.request_url,
                                    request_kwargs=self.request_kwargs)
        self.getValidate()

        JsonResponseInterpreter.__init__(self, self.response)

    def build_url(self):

        base = "https://api.companieshouse.gov.uk/company/"\
                    "{company_number}/persons-with-significant-control"\
                        .format(company_number=self.company_code)

        if self.person_id:
            suffix = "/".join([self.person_type, self.person_id])
            self.request_url = "/".join([base, suffix])

        else:
            self.request_url = base

    def build_request_kwargs(self):

        if self.additional_request_kwargs:

            if "headers" not in self.additional_request_kwargs.keys():
                self.request_kwargs = {**{'headers':self.basicAuthHeader},
                                       **self.additional_request_kwargs}

            else:
                raise Exception("""BasicAuth provides the header based on the appkey
                that you provide as first argument in CompanyOfficers""")

        else:
            self.request_kwargs = {'headers':self.basicAuthHeader}
