# -*- coding: utf-8 -*-
import time, os, sys
from time import strftime

local_file_fname = 'cities_from_dropbox.txt'
print(os.path.abspath(local_file_fname))
import dropboxm
dropbox_filename = '/othodi/cities_few.txt'
dc = dropboxm.DropboxConnection()

if __name__ == "__main__":
    try:
        while True:
            # with dc.open_dropbox_file(dropbox_filename) as dropbox_file:
            #     address_list = [line.strip() for line in dropbox_file]
            
            if not os.path.isfile(local_file_fname):
                with open(local_file_fname,'w') as local_file:
                    pass
            address_list = []
            with dc.open_dropbox_file(dropbox_filename) as df:
                for line in df:
                    # print(line)
                    address_list.append(line.strip())
            rewrite = False
            local_address_list = []
            with open(local_file_fname,'r') as local_file:
                for line in local_file:
                    # print(line)
                    local_address_list.append(line.strip())
            
            if address_list != local_address_list:
                print('\n%s Files are not equal.\nRewriting local_file.\n' % strftime("%Y-%m-%d %H:%M:%S"))
            #     rewrite = True
            # if rewrite:
                with open(local_file_fname,'w') as local_file:
                    for address in address_list:
                        local_file.write(address+'\n')
                    # for line in address_list:
                #     local_file.write(line+'\n')
            else:
                pass
                sys.stdout.write('.')
                sys.stdout.flush()
                # print('All lines are the same.\t%s' % strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(2)
    except Exception as e:
        print('Error:\n%s\nQuitting.' % e)
        sys.exit(1)
            