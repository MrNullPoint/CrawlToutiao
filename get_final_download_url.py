from bs4 import BeautifulSoup
import requests
import random


def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


url = 'http://www.xicidaili.com/nn/'
headers = {
    # 'Host': 'm.toutiao.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Mobile Safari/537.36'
}
ip_list = get_ip_list(url, headers=headers)

f = open('url')
url_list = f.readlines()

headers = {
    'Host': 'm.toutiao.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Mobile Safari/537.36'
}
for url in url_list:
    proxies = get_random_ip(ip_list)
    r = requests.get(url.strip(), headers=headers, proxies=proxies, allow_redirects=False)
    try:
        print(r.headers['location'])
    except:
        continue
