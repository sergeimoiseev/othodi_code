# -*- coding: utf-8 -*-
import dropboxm
    dr_fname = '/othodi/cities_few.txt'
    dc = dropboxm.DropboxConnection()
    with dc.open_dropbox_file(dr_fname) as dropbox_file:
        address_list = [line.strip() for line in dropbox_file]

if __name__ == "__main__":
    