from web_connect.retrieve_response.retrieve_response import RetrievedResponse
from web_connect.interpret_response.interpret_json_response import (
JsonResponseInterpreter)
from web_connect.RESTConnect.basicAuth import BasicAuth

class CHCompany:

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

    """

    def __init__(self, appKey, company_query_string, by="id"):

        assert by == "id" or by == "friendly_string", \
            "CHCompany constructor accepts only 'friendly_string' to retrieve"\
            " a list of possible companies, or 'id' to retrieve information"\
            " on a specific company whose companies house company ID is already"\
            " known to you."

        #Create the headers based on the basicauth protocol
        self.basicAuthHeader      = BasicAuth(appKey).basicAuthHeader
        self.request_kwargs       = {"headers": self.basicAuthHeader}

        self.company_query_string = company_query_string
        self.by                   = by

        #Create the request url
        self.build_url()

        # Get the data
        self.retrieve_company_data()

        # Turn the data into a JSON dictionary
        self.interpret_company_data()

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

    def retrieve_company_data(self, timeout=15):
        """
        Retrives and validates data using self.request_url and self.request
        kwargs built at instantiation and in build_url function

        Instantiates self.rr as RequestResponse instance
        Adds attribute self.ch_response as the raw http response from the API
        """

        #Instantiate RetrievedResponse class
        self.rr = RetrievedResponse(url=self.request_url,
                                    **self.request_kwargs)

        # Request the data and validate the response

        self.rr.getValidate(timeout=timeout)

        # Create the ch_response attribute as a view of the RetrievedResponse
        # .response attribute

        self.ch_response = self.rr.response

    def interpret_company_data(self):

        self.jri = JsonResponseInterpreter(self.ch_response)

# rr = RetrievedResponse("https://api.companieshouse.gov.uk/search/companies",
#         headers = {"Authorization":"***REMOVED***:"},
#         params={"q":"Alphabet"})
#
# ri = JsonResponseInterpreter(rr.response)
