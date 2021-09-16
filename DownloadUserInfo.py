import tableauserverclient as TSC
import csv

server_url = 'https://dub01.online.tableau.com'
PAT_name = 'RestAPI-UserManagementScript'
PAT_value = ''
site_name = 'tablonian'
csv_path = './users.csv'

server = TSC.Server(server_url, use_server_version=True)
tableau_auth = TSC.PersonalAccessTokenAuth(PAT_name, PAT_value, site_name)

print("Collecting the list of users...")
with server.auth.sign_in(tableau_auth):
    all_users, pagination_item = server.users.get()
    print("\nWriting {} users to file: ".format(pagination_item.total_available))
    #debug output
    #print([[user.name,user.site_role] for user in all_users])

    #write data to csv
    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id','Username','SiteRole'])
        for user in all_users:
            writer.writerow([user.id,user.name,user.site_role])

print("\nSuccess\nEnd of script")
