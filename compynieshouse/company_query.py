from web_connect.retrieve_response.retrieve_response import RetrievedResponse
from web_connect.interpret_response.interpret_json_response import (
JsonResponseInterpreter)

rr = RetrievedResponse("https://api.companieshouse.gov.uk/search/companies",
        headers = {"Authorization":"***REMOVED***:"},
        params={"q":"Alphabet"})

ri = JsonResponseInterpreter(rr.response)
