import requests
from bs4 import BeautifulSoup
from datetime import datetime
import extruct
import json

def fetch_webpage_data(url):
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise ValueError(f"Failed to retrieve webpage. Status code: {response.status_code}")

        page_content = response.text
        soup = BeautifulSoup(page_content, 'lxml')

        data = {
            'url': url,
            'title': soup.title.string if soup.title else None,
            'length': len(page_content),
            'fetch_date': datetime.now().isoformat(),
            'meta_tags': {tag.attrs['name']: tag.attrs['content'] for tag in soup.find_all('meta') if 'name' in tag.attrs and 'content' in tag.attrs},
        }

        jsonld_data = extruct.extract(page_content, base_url=url, syntaxes=['json-ld'])
        if 'json-ld' in jsonld_data and jsonld_data['json-ld']:
            data['json_ld_objects'] = jsonld_data['json-ld']

        opengraph_data = extruct.extract(page_content, base_url=url, syntaxes=['opengraph'])
        if 'opengraph' in opengraph_data and opengraph_data['opengraph']:
            data['opengraph_data'] = opengraph_data['opengraph']

        twitter_data = {tag.attrs['name']: tag.attrs['content'] for tag in soup.find_all('meta') if 'name' in tag.attrs and 'content' in tag.attrs and 'twitter:' in tag.attrs['name']}
        if twitter_data:
            data['twitter_data'] = twitter_data

        return data

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

def main():
    url = 'https://www.thetimes.co.uk/article/maggie-chapman-to-be-barred-from-holyrood-meeting-after-failing-to-reveal-link-to-rape-charity-3kgqqfcjf'
    data = fetch_webpage_data(url)
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
