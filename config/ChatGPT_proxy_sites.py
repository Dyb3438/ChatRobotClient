import json
from transformers import GPT2Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")


proxy_sites = [
    {
        'web': 'https://chat.forchange.cn/',
        'url': 'https://api.forchange.cn/',
        'method': 'post',
        'data': lambda question: json.dumps({
            'prompt': "Human:{question}\nAI:".format(question=question),
            'tokensLength': tokenizer("Human:{question}\nAI:".format(question=question))['input_ids'].__len__()
        }),
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Host': 'api.forchange.cn',
            'Origin': 'https://chat.forchange.cn',
            'Referer': 'https://chat.forchange.cn/',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        }
    },
]


if __name__ == '__main__':
    import requests

    question = "How old are you?"

    site = proxy_sites[0]

    req = getattr(requests, site['method'])(
        site['url'], 
        data=site['data'](question),
        headers=site['headers']
        )
    print(f'From site: {site["web"]}')
    print(req.text)