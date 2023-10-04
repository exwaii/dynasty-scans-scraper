import json
import aiohttp
import asyncio
import os 
from download import download_file

semaphore = asyncio.Semaphore(5)  # Assuming 5 as a limit for concurrent downloads


async def check_and_download():
    with open('data/failed.json', 'r') as f:
        failed = json.load(f)
    # the initial download fails sometimes    
    with open('data/failed_images.json', 'r') as f:
        failed_images = json.load(f)
    # the images are sometimes truncated, pypdf will tell u if so
    
    tasks = [download_file(download_url, file_name) for download_url, file_name in downloads]
    await asyncio.gather(*tasks)

# Entry point
if __name__ == "__main__":
    asyncio.run(check_and_download())
