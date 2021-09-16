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
    #write data to csv
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                csv_id = row[0]
                csv_name = row[1]
                csv_role = row[2]
                print(f'\n{csv_name} has a role of {csv_role}')
                curr_user = server.users.get_by_id(csv_id)
                print('User {} has been found on server with role of {}'.format(curr_user.name,curr_user.site_role))
                if curr_user.site_role == csv_role:
                    print("roles match, skipping")
                else:
                    confirm_update = input("Mismatch - Enter y to update server to match csv\n")
                    if confirm_update == 'y':
                        print('Updating')
                        #update the user
                        curr_user.site_role = csv_role
                        curr_user = server.users.update(curr_user)
                    else:
                        print('Skipping')
                line_count += 1
        print(f'Processed {line_count-1} lines.')
print("\nSuccess\nEnd of script")
