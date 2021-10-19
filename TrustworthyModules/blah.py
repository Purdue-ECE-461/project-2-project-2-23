import requests

headers = {
    'Authorization': 'token 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',
}

response = requests.get('https://api.github.com/rate_limit', headers=headers)

print(response.text)