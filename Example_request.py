import requests

url = "https://www.notexponential.com/aip2pgaming/api/index.php"

payload={'name': 'Tianheng',
'type': 'team'}
files=[

]
headers = {
  'x-api-key': 'ca8eb275449c03fd1f5f',
  'userId': '1111',
  'Content-Type': 'application/x-www-form-urlencoded',
  'User-Agent': 'PostmanRuntime/7.29.0'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)