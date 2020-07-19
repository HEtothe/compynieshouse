# compynieshouse - a convenient wrapper for the UK Companies House REST API
## Overview
The UK's Companies House publishes the financial returns, lists of officers
etc. of many of the companies registered with it. They now provide some of
that information conveniently over a REST API, which is a fantastic resource.

While the API and its documentation are fairly intuitive, this module seeks to
make it more "turnkey" for the user, avoiding headaches over basic auth, the
requests library etc.

Requirements:

1. Python 3
2. [datagrab](https://github.com/HEtothe/datagrab)
3. A [Companies House API](https://developer.companieshouse.gov.uk/api/docs/) key

## Getting it
To download datagrab, either fork this github repo or simply use Pypi via pip.

## Usage

### Retrieve the key information about a specific company

Let's say you're a BI developer and you want an easy way of refreshing your
the company key information in your CRM system. You'd first need a way of
easily checking the Companies House as a single source of truth.

Here's the docstring for the main class, CHCompany:

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

So you can see, you just need your Companies House API Key and the company number.    

    >>> from compynieshouse.company_query import CHCompany
    >>> ch = CHCompany("<my_companies_house_API_key",
                    company_query_string="02557590",   # What we ask for
                    by="id", # Search type - can be by "friendly_string", or "id"
                    )

    >>> ch.jsonDict

                  {'sic_codes': ['82990'],
                     'jurisdiction': 'england-wales',
                     'date_of_creation': '1990-11-12',
                     'type': 'ltd',
                     'undeliverable_registered_office_address': False,
                     'last_full_members_list_date': '2015-11-12',
                     'registered_office_address': {'postal_code': 'CB1 9NJ',
                      'address_line_2': 'Cambridge',
                      'address_line_1': '110 Fulbourn Road',
                      'locality': 'Cambridgeshire'},
                     'accounts': {'overdue': False,
                      'next_made_up_to': '2020-03-31',
                      'next_accounts': {'overdue': False,
                       'due_on': '2020-12-31',
                       'period_end_on': '2020-03-31',
                       'period_start_on': '2019-04-01'},
                      'accounting_reference_date': {'day': '31', 'month': '03'},
                      'last_accounts': {'period_start_on': '2018-04-01',
                       'period_end_on': '2019-03-31',
                       'made_up_to': '2019-03-31',
                       'type': 'group'},
                      'next_due': '2020-12-31'},
                     'company_number': '02557590',
                     'has_been_liquidated': False,
                     'company_name': 'ARM LIMITED',
                     'has_insolvency_history': False,
                     'etag': '7011282471135667318564d3ba8a2c3942359264',
                     'company_status': 'active',
                     'has_charges': True,
                     'previous_company_names': [{'effective_from': '1990-12-03',
                       'ceased_on': '1998-05-21',
                       'name': 'ADVANCED RISC MACHINES LIMITED'},
                      {'effective_from': '1990-11-12',
                       'ceased_on': '1990-12-03',
                       'name': 'WIDELOGIC LIMITED'}],
                     'confirmation_statement': {'next_made_up_to': '2020-11-14',
                      'overdue': False,
                      'last_made_up_to': '2019-11-14',
                      'next_due': '2020-11-28'},
                     'links': {'self': '/company/02557590',
                      'filing_history': '/company/02557590/filing-history',
                      'officers': '/company/02557590/officers',
                      'charges': '/company/02557590/charges',
                      'persons_with_significant_control': '/company/02557590/persons-with-significant-control',
                      'registers': '/company/02557590/registers'},
                     'registered_office_is_in_dispute': False,
                     'can_file': True}

`CHCompany` inherits JsonResponseInterpreter class, which is part of the [datagrab library](
  https://github.com/HEtothe/datagrab
  ).
So we can access attributes like jsonDict and the json_tree_traverse method.

This is pretty handy if, say, we want to find the city of the registered address.

    >>>>ch.json_tree_traverse(["registered_office_address","locality"])         
    'Cambridgeshire'

If we're new to the Companies House schema, we can use `ch.visualize_json()` to
see the structure.

    Root
    ├── accounts
    │   ├── accounting_reference_date
    │   │   ├── day
    │   │   └── month
    │   ├── last_accounts
    │   │   ├── made_up_to
    │   │   ├── period_end_on
    │   │   ├── period_start_on
    │   │   └── type
    │   ├── next_accounts
    │   │   ├── due_on
    │   │   ├── overdue
    │   │   ├── period_end_on
    │   │   └── period_start_on
    │   ├── next_due
    │   ├── next_made_up_to
    │   └── overdue
    ├── can_file
    ├── company_name
    ├── company_number
    ├── company_status
    ├── confirmation_statement
    │   ├── last_made_up_to
    │   ├── next_due
    │   ├── next_made_up_to
    │   └── overdue
    ├── date_of_creation
    ├── etag
    ├── has_been_liquidated
    ├── has_charges
    ├── has_insolvency_history
    ├── jurisdiction
    ├── last_full_members_list_date
    ├── links
    │   ├── charges
    │   ├── filing_history
    │   ├── officers
    │   ├── persons_with_significant_control
    │   ├── registers
    │   └── self
    ├── previous_company_names
    ├── registered_office_address
    │   ├── address_line_1
    │   ├── address_line_2
    │   ├── locality
    │   └── postal_code
    ├── registered_office_is_in_dispute
    ├── sic_codes
    ├── type
    └── undeliverable_registered_office_address


Let's imagine now that we want to see if a company name is available. In that
case, we'd need to search by a particular substring.

In that case, set the "by" keyword argument to "friendly_string":

    >>> ch = CHCompany("<my_companies_house_API_key>",
                    company_query_string="ARM",   # What we ask for
                    by="friendly_string", # Search type
                      )

    >>> ch.json_tree_traverse(["items"])[:2]
    [{'snippet': '',
      'company_number': '02557590',
      'description': '02557590 - Incorporated on 12 November 1990',
      'company_type': 'ltd',
      'title': 'ARM LIMITED',
      'date_of_creation': '1990-11-12',
      'company_status': 'active',
      'address_snippet': '110 Fulbourn Road, Cambridge, Cambridgeshire, CB1 9NJ',
      'address': {'premises': '110',
       'postal_code': 'CB1 9NJ',
       'address_line_2': 'Cambridge',
       'address_line_1': 'Fulbourn Road',
       'locality': 'Cambridgeshire'},
      'matches': {'title': [1, 3], 'snippet': []},
      'kind': 'searchresults#company',
      'links': {'self': '/company/02557590'},
      'description_identifier': ['incorporated-on']},
     {'links': {'self': '/company/11551941'},
      'description_identifier': ['incorporated-on'],
      'kind': 'searchresults#company',
      'matches': {'snippet': [1, 3]},
      'address': {'premises': '3000a',
       'country': 'United Kingdom',
       'postal_code': 'PO15 7FX',
       'address_line_1': 'Parkway Whiteley',
       'locality': 'Hampshire'},
      'address_snippet': '3000a Parkway Whiteley, Hampshire, United Kingdom, PO15 7FX',
      'company_status': 'active',
      'date_of_creation': '2018-09-04',
      'title': 'AMR CYBERSECURITY LTD',
      'company_type': 'ltd',
      'description': '11551941 - Incorporated on  4 September 2018',
      'company_number': '11551941',
      'snippet': 'ARM CYBERSECURITY '}]


It's also useful for identifying the company number of your target entity. So in
this case, if you were looking for the chip designer who revolutionised computing,
you would be looking for `02557590`.

Now, you've probably noticed that the main payload within the `jsonDict` is under
the `"items"` key. These `items` are contained in a list -
because it's the list of items returned by the search. That means that our method
`ch.visualize_json()` produces an `AttributeError`, because `visualize_json`
assumes a dictionary.

So `visualize_json` is available as a standalone function

    >>> from datagrab.interpret_response.json_visualize import visualize_json
    >>> visualize_json(ch.json_tree_traverse(["items"])[0])
    Root
    ├── address
    │   ├── address_line_1
    │   ├── address_line_2
    │   ├── locality
    │   ├── postal_code
    │   └── premises
    ├── address_snippet
    ├── company_number
    ├── company_status
    ├── company_type
    ├── date_of_creation
    ├── description
    ├── description_identifier
    ├── kind
    ├── links
    │   └── self
    ├── matches
    │   ├── snippet
    │   └── title
    ├── snippet
    └── title

## Who has a stake in this company?

Companies house provides an endpoint to find persons (natural or corporate) with
significant control.

Here's how to access that:

    >>> from compynieshouse.significant_control_query import SignificantControlQuery

    >>> scq = SignificantControlQuery(
        appKey="<my_companies_house_API_key>",
        company_code="02557590")

    >>> scq.visualize_json()
    Root
    ├── active_count
    ├── ceased_count
    ├── items
    ├── items_per_page
    ├── links
    │   └── self
    ├── start_index
    └── total_results

Note again that the key payload is under the `"items"`, which is effectively
a list of dictionaries.

This is what such a record looks like:

    >>> visualize_json(scq.json_tree_traverse(["items"])[0])
    Root
    ├── address
    │   ├── address_line_1
    │   ├── country
    │   ├── locality
    │   ├── postal_code
    │   └── premises
    ├── etag
    ├── identification
    │   ├── country_registered
    │   ├── legal_authority
    │   ├── legal_form
    │   ├── place_registered
    │   └── registration_number
    ├── kind
    ├── links
    │   └── self
    ├── name
    ├── natures_of_control
    └── notified_on

## Who are the company officers?

    >>> from compynieshouse.officer_query import CompanyOfficers
    >>> from datagrab.interpret_response.json_visualize import visualize_json

    >>> cos = CompanyOfficers("***REMOVED***",
                        "02557590",
                        )
    >>> cos.visualize_json()
    Root
    ├── active_count
    ├── etag
    ├── inactive_count
    ├── items
    ├── items_per_page
    ├── kind
    ├── links
    │   └── self
    ├── resigned_count
    ├── start_index
    └── total_results


    >>> officers_records = cos.json_tree_traverse(["items"])[0]

    >>> visualize_json(officers_records)
    Root
    ├── address
    │   ├── address_line_1
    │   ├── address_line_2
    │   ├── locality
    │   └── postal_code
    ├── appointed_on
    ├── links
    │   └── officer
    │       └── appointments
    ├── name
    └── officer_role

## What other appointments does this officer have?

First, we need the ID of the officer:

    >>> officers_records["links"]
    {'officer': {'appointments': '/officers/4yYi8Ok5MbG3QNg8t05GUZF-u-U/appointments'}}

    >>> from compynieshouse.officer_appointments import OfficerAppointments

    >>> oa = OfficerAppointments("<my_companies_house_API_key>",
                        "4yYi8Ok5MbG3QNg8t05GUZF-u-U", # officer ID
                        )
    >>> oa.visualize_json()
    Root
    ├── etag
    ├── is_corporate_officer
    ├── items
    ├── items_per_page
    ├── kind
    ├── links
    │   └── self
    ├── name
    ├── start_index
    └── total_results

    >>> oa.jsonDict["name"]
    'Carolyn HERZOG'

How many appointments does Carolyn Herzog have?

    >>> len(oa.json_tree_traverse(["items"]))
    1

Just the one.
What details about that appointment does Companies House provide us?

    >>> visualize_json(oa.json_tree_traverse(["items"])[0])
    Root
    ├── address
    │   ├── address_line_1
    │   ├── address_line_2
    │   ├── locality
    │   └── postal_code
    ├── appointed_on
    ├── appointed_to
    │   ├── company_name
    │   ├── company_number
    │   └── company_status
    ├── links
    │   └── company
    ├── name
    ├── name_elements
    │   ├── forename
    │   ├── surname
    │   └── title
    └── officer_role
