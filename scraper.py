import requests
from bs4 import BeautifulSoup
import re
import os

def get_download_links(link):
    """enter dynasty series link to get out a list of (page save location, page image url)

    Args:
        link (str): dynasty series link

    Returns:
        List: list of (page save location, page image url)
    """
    title = link.split("/")[-1]
    if os.path.exists(f"manga/{title}"):
        if (
            input(f"You already have a folder for {title}. Do you wish to continue? (y/n) ")
            != "y"
        ):
            exit()
    else:
        os.makedirs(f"manga/{title}")
        
    r = requests.get(f"https://dynasty-scans.com/series/{title}")
    soup = BeautifulSoup(re.sub(r"\n+", "", r.text), "lxml")

    chapters = soup.select('dl[class="chapter-list"]')[0]
    curr_dir = f"manga/{title}/{title}"
    downloads = []

    for tag in chapters.contents:
        if not tag or tag.text.isspace():
            continue
        if tag.name == "dt" and not tag.text:
            curr_dir = f"manga/{title}/{tag.text}"
            if not os.path.exists(curr_dir):
                os.makedirs(curr_dir)
        else:
            link = tag.a['href']
            chapter_request = requests.get(f"https://dynasty-scans.com{link}")
            chapter_soup = BeautifulSoup(re.sub(r"\n+", "", chapter_request.text), "lxml")
            chapter = link.split('/')[-1]
            if not os.path.exists(f"{curr_dir}/{chapter}"):
                os.makedirs(f"{curr_dir}/{chapter}")
            pages = chapter_soup.select('div[class="pages-list"]')[0]
            img = chapter_soup.find(lambda x : x.name == "img" and "releases" in x["src"])
            img_format = img["src"].rsplit(".", maxsplit=1)[-1]
            img_base = img["src"].rsplit(".", maxsplit=1)[0].rsplit(pages.contents[1].text, maxsplit=1)[0]
            for page in pages.contents:
                if not page or page.text.isspace() or "class" not in page.attrs:
                    continue
                downloads.append((f"https://dynasty-scans.com{img_base}{page.text}.{img_format}", f"{curr_dir}/{chapter}/{page.text}.{img_format}"))
    return downloads

def main():
    downloads = get_download_links("https://dynasty-scans.com/series/adachi_and_shimamura_moke_ver")
    import json
    with open("downloads.json", "w", encoding="utf-8") as f:
        json.dump(downloads, f, indent=4)


if __name__ == "__main__":
    main()
