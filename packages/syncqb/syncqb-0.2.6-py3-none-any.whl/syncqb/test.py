import qb_client

def main():
    client = qb_client.get_client(True, creds={
        'QB_URL': 'https://rmcgroup.quickbase.com',
        'QB_USERTOKEN': 'b46fjf_ictm_0_c6ikfnbcer5zzpcvkhaynddjctsq'
    })
    data = [
        {
            '6': '4'
        },
    ]
    record = {
        '6': 3
    }



    response = client.delete_record(database='bnj3ts22e', record=116)
    print(response)




if __name__ == '__main__':
    main()