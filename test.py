import requests

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'http://127.0.0.1:5000',
    'Referer': 'http://127.0.0.1:5000/register',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'sec-ch-ua': '"Chromium";v="130", "DuckDuckGo";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'username': 'YWRtaW4=',
    'password': 'YWRtaW4=',
}

response = requests.post('http://127.0.0.1:5000/register', headers=headers, json=json_data)

print(response.text)