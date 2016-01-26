# Include the Dropbox SDK
import dropbox
import os

class DropboxConnection(object):
    """DropboxConnection class"""
    def __init__(self, *arg, **kwargs):
        self._arg = arg
        self._client = self._connect(kwargs)
    def _connect(self,kwargs):        
        # Get your app key and secret from the Dropbox developer website
        app_key = 'lf7drg20ucmhiga'
        app_secret = '1uf7e8o5eu2pqe9'

        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        authorize_url = flow.start()

        # Have the user sign in and authorize this token
        authorize_url = flow.start()
        print ('1. Go to: \n%s' % authorize_url)
        print ('2. Click "Allow" (you might have to log in first)')
        print ('3. Copy the authorization code.')
        if kwargs['copy2clipboard']:
            import pyperclip
            pyperclip.copy(authorize_url)
            # spam = pyperclip.paste()

        try: 
            if kwargs['copy2clipboard']:
                print("Authorization url is copied to clipboard")
            code = raw_input("Enter the authorization code here: ").strip()
        except Exception as e:
            print('Error using raw_input() - trying input()')
            code = input("Enter the authorization code here: ").strip()
        # This will fail if the user enters an invalid authorization code
        access_token, user_id = flow.finish(code)

        client = dropbox.client.DropboxClient(access_token)
        print('linked account user: %s' % client.account_info()['display_name'])
        # print 'linked account: ', client.account_info()
        return client
    def open_dropbox_file(self,full_file_path_name):
        f, metadata = self._client.get_file_and_metadata(full_file_path_name)
        return f

if __name__ == "__main__":
    dr_fname = '/othodi/settings.txt'
    print('reading file \'%s\' from dropbox' % dr_fname)
    dc = DropboxConnection()
    out_fname = 'cities_from_dropbox.txt'
    if not os.path.isfile(out_fname):
        with open(out_fname,'w'):
            pass
    lines_list = []
    with dc.open_dropbox_file(dr_fname) as dr_f:
        with open(out_fname,'r'):
            for line in dr_f:
                print(line)
                lines_list.append(line)

