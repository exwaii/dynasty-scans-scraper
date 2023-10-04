import requests
from bs4 import BeautifulSoup
import os
import re
import aiohttp
import asyncio
import json
from scraper import get_download_links
from download import download_file
from pdf import process_folder

link = input("Enter the dynasty scans link: ")
title = link.split("/")[-1]
downloads = get_download_links(link)

                
async def main():
    semaphore = asyncio.Semaphore(10)  
    tasks = []
    failed = []
    for (url, file_name) in downloads:
        task = download_file(url, file_name, semaphore)
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    for idx, success in enumerate(results):
        if not success:
            print(f"Download for {downloads[idx][0]} to {downloads[idx][1]} failed.")
            failed.append(downloads[idx])
    with open("data/failed.json", "w", encoding="utf-8") as f:
        json.dump(failed, f, indent=4) 
            
if __name__ == "__main__":
    asyncio.run(main())
    process_folder(f"manga/{title}", title)