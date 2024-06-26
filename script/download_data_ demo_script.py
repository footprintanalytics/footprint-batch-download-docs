# Python download data demo script

import requests
import json
import os
import sys


def download(chain, table, file_path='', is_download=True):
		# please contact Footprint to get the information with domain & psk
    domain = ""
    psk = ''
    metadata_headers = {
        'X-Custom-PSK': psk,
        'X-Custom-Chain': chain,
        'X-Custom-Table': table,
        'X-Custom-FilePath': file_path
    }

    data_headers = {
        'X-Custom-PSK': psk,
    }

    download_path = "./r2_download/r2/prod"

    rep = requests.get(domain, headers=metadata_headers)
    if rep.status_code >= 400:
        print("Response status code: {}, message: {}".format(rep.status_code, rep.text))
        sys.exit(1)

    resp_object = rep.json()['objects']
    if not is_download:
        return resp_object
    if not resp_object:
        print("The {} chain {} table does not have data for {}".format(chain, table, file_path))
    else:
        metadata_path = f"./r2_download/{chain}/{table}/"
        if not os.path.exists(metadata_path):
            os.makedirs(metadata_path)
        # Save metadata
        with open(f"{metadata_path}/metadata_file.json", 'w') as f:
            f.write(rep.text)
            f.close()
        # Save file
        for obj in resp_oject:
            r2_path = domain + obj['key']
            download_file_folder = obj['key'].rsplit('/', 1)[0]
            if not os.path.exists(f"./r2_download/{download_file_folder}"):
                os.makedirs(f"./r2_download/{download_file_folder}")
            with open(f'./r2_download/{obj["key"]}', 'wb') as f:
                resp = requests.get(r2_path, headers=data_headers, stream=True)
                for chunk in resp.iter_content(chunk_size=102400):
                    if chunk:
                        f.write(chunk)
                print("File downloaded: " + r2_path)

        # Next, you can process the downloaded data in conjunction with your business needs,
        # such as performing ETL operations to your database.



# date: datetime: yyyy-mm-dd
# e.g: date = 2024-01-01
def download_daily_data(chain, table, date):
    download(chain, table, f"date={date}")

def download_static_data(chain, table):
    download(chain, table)

def download_static_patch_data(chain, table):
    download_static_data(chain, table)

def download_daily_patch_data(chain, table, date):
    download_daily_data(chain, table, date)

def download_daily_latest_full_data(chain, table):
    download(chain, table, "/latest")

def get_all_filename_by_table_name(chain, table):
    object_list = download(chain, table, '', False)
    print(f"{chain} {table} contain the following file:")
    for obj in object_list:
        print(f"file name: {obj['key']}")

def main(chain, table):
    file_path = ''
    download(chain, table, file_path)


if __name__ == '__main__':
    download_daily_patch_data('sui', 'sui_nft_transactions')
