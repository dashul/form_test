# 1. Create and Execute a Real Time Report
# An application can request real-time data by calling the get method on the Analytics service object.
# The method requires an ids parameter which specifies from which view (profile) to retrieve data.
# For example, the following code requests real-time data for view (profile) ID 56789.
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2


def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
    credentials = ServiceAccountCredentials.from_p12_keyfile(
        service_account_email, key_file_location, scopes=scope)

    http = credentials.authorize(httplib2.Http())
    service = build(api_name, api_version, http=http)
    return service


# def get_first_profile_id(service):
#     # Use the Analytics service object to get the first profile id.
#
#     # Get a list of all Google Analytics accounts for this user
#     accounts = service.management().accounts().list().execute()
#
#     if accounts.get('items'):
#         # Get the first Google Analytics account.
#         account = accounts.get('items')[0].get('id')
#
#         # Get a list of all the properties for the first account.
#         properties = service.management().webproperties().list(
#             accountId=account).execute()
#
#         if properties.get('items'):
#             # Get the first property id.
#             property = properties.get('items')[0].get('id')
#
#             # Get a list of all views (profiles) for the first property.
#             profiles = service.management().profiles().list(
#                 accountId=account,
#                 webPropertyId=property).execute()
#
#             if profiles.get('items'):
#                 # return the first view (profile) id.
#                 return profiles.get('items')[0].get('id')
#     return None


# def get_results(service, profile_id):
#     return service.data().ga().get(
#         ids='ga:' + profile_id,
#         metrics='rt:goalCompletionsAll').execute()

def get_results(service, profile_id,metric,when):
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=when,
      end_date=when,
      metrics=metric,
      dimensions = 'ga:networkLocation').execute()


# def print_realtime_report(results):
#     print_report_info(results)
#     print_query_info(results.get('query'))
#     print_profile_info(results.get('profileInfo'))
#     print_column_headers(results.get('columnHeaders'))
#     print_data_table(results)
#     print_totals_for_all_results(results)


def print_data_table(results):
    print
    'Data Table:'
    # Print headers.
    output = []
    for header in results.get('columnHeaders'):
        output.append('%30s' % header.get('name'))
    print
    ''.join(output)
    # Print rows.
    if results.get('rows', []):
        for row in results.get('rows'):
            output = []
            for cell in row:
                output.append('%30s' % cell)
            print
            ''.join(output)
    else:
        print
        'No Results Found'



scope = ['https://www.googleapis.com/auth/analytics.readonly']
service_account_email = 'new-service-account@bookinghealth-167119.iam.gserviceaccount.com'
key_file_location = 'client_secrets.p12'
service = get_service('analytics', 'v3', scope, key_file_location,
                      service_account_email)
profile_ru = '108311826'
profile_en = '109979535'
metric_ru = 'ga:goal6Completions'
metric_en = 'ga:goal8Completions'
with open('log.txt','r') as f:
    en,ru = f.read()

if en == get_results(service, profile_en,metric_en,'yesterday')['totalsForAllResults'][metric_en]:
    print ('en == real yesterday')
else:
    print(en,'!= ',get_results(service, profile_en,metric_en,'yesterday')['totalsForAllResults'][metric_en])

if ru == get_results(service, profile_ru, metric_ru, 'yesterday')['totalsForAllResults'][metric_ru]:
    print('ru == real yesterday')
else:
    print(ru, '!= ', get_results(service, profile_ru, metric_ru, 'yesterday')['totalsForAllResults'][metric_ru])

with open('log.txt','w') as f:
    f.write(get_results(service, profile_en,metric_en,'today')['totalsForAllResults'][metric_en])
    f.write(get_results(service, profile_ru,metric_ru,'today')['totalsForAllResults'][metric_ru])
s = set()
print(get_results(service, profile_en,metric_en,'2017-05-10'))
print(get_results(service, '142533440', metric_en,'2017-05-10')['rows'])
for item in get_results(service, profile_en,metric_en,'2017-05-10')['rows']:
    s.add(item[0])

for item in get_results(service, '142533440', metric_en,'2017-05-10')['rows']:
    s.discard(item[0])
print (s)
