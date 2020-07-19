from datagrab.retrieve_response.retrieve_response import RetrievedResponse
from datagrab.interpret_response.interpret_json_response import (
JsonResponseInterpreter)
from datagrab.RESTConnect.basicAuth import BasicAuth


class CHCompany(JsonResponseInterpreter, BasicAuth, RetrievedResponse):

    """
    Companies House Company

    A way of retrieving data about a target company using the Companies house
    REST API

    ------------------------
    args:

        appKey: string
        Your companies house API key

        company_query_string: string
        if by=="id" then this should be the companies house company ID of the
        target company, else if by=="friendly_string" then it's the long-form
        name of the target company.
    ------------------------
    kwargs:

        by: string
        Accepts: "id" if you are using the companies house ID or "friendly_string"
        if you are using the name of the target company

        zero_results_suppression: bool
        Accepts: True or False
        Default: False
        When set to true, this prints some troubleshooting tips if you run a
        company search which returns zero results. Setting to True is not
        recommended for production code.

    """

    def __init__(self, appKey: str, company_query_string: str, by="id",
                zero_results_suppression=False, additional_request_kwargs=None,
                request_timeout=15.):

        assert by == "id" or by == "friendly_string", \
            "CHCompany constructor accepts only 'friendly_string' to retrieve"\
            " a list of possible matches, or 'id' to retrieve information"\
            " on a specific company whose companies house company ID is already"\
            " known to you."

        #Create the headers based on the basicauth protocol
        BasicAuth.__init__(self, user=appKey)

        self.additional_request_kwargs = additional_request_kwargs

        self.company_query_string = company_query_string
        self.by                   = by
        self.zero_results_suppression = zero_results_suppression

        #Create the request url
        self.build_url()

        # add any additional required content to http request
        self.build_request_kwargs()

        # instantiate the RetrievedResponse class
        RetrievedResponse.__init__(self, url=self.request_url,
                                    request_kwargs=self.request_kwargs)

        # Request the data and validate the response
        # This is where HTTP reponse errors will be raised and handled by the
        # getResponse method of RetrievedResponse
        self.getValidate(timeout=request_timeout)

        # Instantiate JsonResponseInterpreter class
        JsonResponseInterpreter.__init__(self,self.response)

        # Remove superfluous information from the JSON tree
        # If we searched by the friendly string, then we get a list of dictionaries
        # each relating to a company on their books. This list, which is what we
        # want, is stored as the "items" item.

        if self.by == "friendly_string" and self.jsonDict["total_results"]<=0\
            and not self.zero_results_suppression:
            # This will be an empty list if the input string did not return
            # any companies.

            print("""We created a list of your results, but the list
            itself is empty. This is probably due to a company name that the
            Companies House search engine can't find any matches for.
            """)


    def build_url(self):
        """
        Creates self.request_url and adds parameters to request_kwargs if
        self.by is set to "friendly_string"

        Called when parent class is instantiated
        """

        # if we are querying by friendly_string then the URL will be to perform
        # a Search, but if we are querying by a specific company ID then we will
        # create an url to .query by company

        if self.by == "friendly_string":
            self.base_url = "https://api.companieshouse.gov.uk/search/companies?q="
            #self.request_kwargs["params"] = {"q":self.company_query_string}

        else:
            self.base_url = "https://api.companieshouse.gov.uk/company/"

        self.request_url = self.base_url + self.company_query_string


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
