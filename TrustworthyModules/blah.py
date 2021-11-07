import requests

headers = {
    'Authorization': 'token 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',
}

response = requests.get('https://api.github.com/rate_limit', headers=headers)

print(response.text)