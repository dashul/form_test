import argparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
  """Get a service that communicates to a Google API.

  Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.

  Returns:
    A service that is connected to the specified API.
  """

  credentials = ServiceAccountCredentials.from_p12_keyfile(
    service_account_email, key_file_location, scopes=scope)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service

def get_first_profile_id(service):
  # Use the Analytics service object to get the first profile id.

  # Get a list of all Google Analytics accounts for this user
  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    # Get the first Google Analytics account.
    account = accounts.get('items')[0].get('id')

    # Get a list of all the properties for the first account.
    properties = service.management().webproperties().list(
        accountId=account).execute()

    if properties.get('items'):
      # Get the first property id.
      property = properties.get('items')[0].get('id')

      # Get a list of all views (profiles) for the first property.
      profiles = service.management().profiles().list(
          accountId=account,
          webPropertyId=property).execute()

      if profiles.get('items'):
        # return the first view (profile) id.
        return profiles.get('items')[0].get('id')

  return None

def get_results(service, profile_id):
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='today',
      end_date='today',
      metrics='rt:goalCompletionsAll').execute()

def print_results(results):
  # Print data nicely for the user.
  if results:
    print ('View (Profile): %s' % results.get('profileInfo').get('profileName'))
    print ('Total Sessions: %s' % results.get('rows')[0][0])

  else:
    print ('No results found')

def main():
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly']

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
  service_account_email = 'new-service-account@bookinghealth-167119.iam.gserviceaccount.com'
  key_file_location = 'client_secrets.p12'

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
  profile = get_first_profile_id(service)
  print_results(get_results(service, profile))

if __name__ == '__main__':
  main()



def print_column_headers(headers):
    print
    'Column Headers:'
    for header in headers:
        print
        'Column name           = %s' % header.get('name')
        print
        'Column Type           = %s' % header.get('columnType')
        print
        'Column Data Type      = %s' % header.get('dataType')


def print_query_info(query):
    if query:
        print
        'Query Info:'
        print
        'Ids                   = %s' % query.get('ids')
        print
        'Metrics:              = %s' % query.get('metrics')
        print
        'Dimensions            = %s' % query.get('dimensions')
        print
        'Sort                  = %s' % query.get('sort')
        print
        'Filters               = %s' % query.get('filters')
        print
        'Max results           = %s' % query.get('max-results')


def print_profile_info(profile_info):
    if profile_info:
        print
        'Profile Info:'
        print
        'Account ID            = %s' % profile_info.get('accountId')
        print
        'Web Property ID       = %s' % profile_info.get('webPropertyId')
        print
        'Profile ID            = %s' % profile_info.get('profileId')
        print
        'Profile Name          = %s' % profile_info.get('profileName')
        print
        'Table Id              = %s' % profile_info.get('tableId')


def print_report_info(results):
    print
    'Kind                    = %s' % results.get('kind')
    print
    'ID                      = %s' % results.get('id')
    print
    'Self Link               = %s' % results.get('selfLink')
    print
    'Total Results           = %s' % results.get('totalResults')


def print_totals_for_all_results(results):
    totals = results.get('totalsForAllResults')
    for metric_name, metric_total in totals.iteritems():
        print
        'Metric Name  = %s' % metric_name
        print
        'Metric Total = %s' % metric_total