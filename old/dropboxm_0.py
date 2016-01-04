from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient
from dropbox import rest as dbrest

auth_flow = DropboxOAuth2FlowNoRedirect('pos53ybtbvmf2dc', 'akmlyilnzwmti9b')

authorize_url = auth_flow.start()
print "1. Go to: " + authorize_url
print "2. Click \"Allow\" (you might have to log in first)."
print "3. Copy the authorization code."
auth_code = raw_input("Enter the authorization code here: ").strip()

try:
    access_token, user_id = auth_flow.finish(auth_code)
except dbrest.ErrorResponse, e:
    print('Error: %s' % (e,))
    # return

client = DropboxClient(access_token)
print 'linked account: ', client.account_info()

f, metadata = client.get_file_and_metadata('/Work/Othodi/data/cities.txt')
# f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
out_fname = 'cities_from_dropbox.txt'
out = open('cities_from_dropbox.txt', 'wb')
out.write(f.read())
out.close()
print metadata

with open(out_fname,'r'):
    for line in f:
        print(line)