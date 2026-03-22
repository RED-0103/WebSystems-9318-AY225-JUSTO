import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_ea_games():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    games = []

    urls = [
        'https://www.ea.com/games/apex-legends',
        'https://www.ea.com/games/battlefield/battlefield-2042',
        'https://www.ea.com/games/the-sims/the-sims-4',
        'https://www.ea.com/games/fifa/fifa-23',
        'https://www.ea.com/games/need-for-speed/need-for-speed-unbound',
        'https://www.ea.com/games/dead-space',
        'https://www.ea.com/games/star-wars/star-wars-jedi/star-wars-jedi-survivor',
        'https://www.ea.com/games/ea-sports-fc/ea-sports-fc-24',
        'https://www.ea.com/games/dragon-age/dragon-age-the-veilguard',
        'https://www.ea.com/games/f1/f1-23',
    ]

    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get title
            title = soup.find('h1')
            title = title.get_text(strip=True) if title else 'Not Available'

            # Get description/features
            desc = soup.find('meta', attrs={'name': 'description'})
            features = desc['content'] if desc else 'Not Available'

            # Get platform
            platform_tag = soup.find('meta', attrs={'property': 'og:title'})
            platform = 'PC, PlayStation, Xbox' 

            # Get release date
            date_tag = soup.find('span', class_='release-date')
            release_date = date_tag.get_text(strip=True) if date_tag else 'Not Available'

            game = {
                'title': title,
                'release_date': release_date,
                'key_features': features[:200],
                'platforms': platform,
                'developer': 'Electronic Arts',
                'publisher': 'Electronic Arts'
            }

            games.append(game)
            print(f'Scraped: {title}')

        except Exception as e:
            print(f'Error scraping {url}: {e}')

    os.makedirs('data', exist_ok=True)
    with open('data/games.json', 'w') as f:
        json.dump(games, f, indent=4)

    print(f'\nTotal scraped: {len(games)} games!')
    return games

if __name__ == '__main__':
    scrape_ea_games()