import requests

import gopac

pac_path = gopac.download_pac_file(
    'https://antizapret.prostovpn.org/proxy.pac'
)
proxy = gopac.find_proxy(pac_path, 'https://www.linkedin.com')
response = requests.get('https://www.linkedin.com', proxies=proxy)
print(response.text)
