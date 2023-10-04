import os
import aiohttp
import asyncio
from aiohttp.client_exceptions import ClientConnectionError

async def download_file(url, file_name, semaphore, retries=4):
    if os.path.exists(file_name):
        return

    temp_file_name = file_name + ".temp"
    dir_name = os.path.dirname(file_name)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)

    async with semaphore:
        for attempt in range(retries):
            try:
                async with aiohttp.ClientSession() as session:
                    timeout = aiohttp.ClientTimeout(total=120)
                    async with session.get(url, timeout=timeout) as response:
                        
                        if response.status == 200:
                            with open(temp_file_name, 'wb') as f:
                                while True:
                                    chunk = await response.content.read(8192)
                                    if not chunk:
                                        break
                                    f.write(chunk)

                            os.rename(temp_file_name, file_name)
                            print(f"Downloaded {file_name} successfully.")
                            return True

                        elif response.status == 404:
                            if url.endswith('.png'):
                                new_url = url[:-4] + '.jpg'
                            elif url.endswith('.jpg'):
                                new_url = url[:-4] + '.png'
                            else:
                                print(f"Failed to download {file_name}. Status code: {response.status}")
                                return False

                            print(f"URL {url} returned 404. Retrying with {new_url[-4:]} instead.")
                            url = new_url  
                            continue

                        else:
                            print(f"Failed to download {file_name}. Status code: {response.status}")
                            return False

            except ClientConnectionError as e:
                print(f"Connection error for {file_name}. Check your network or the server might be temporarily down.")
                if attempt < retries - 1:
                    delay = 5
                    await asyncio.sleep(delay)

            except Exception as e:
                print(f"Error {e} for {file_name}.")
                return False

        print(f"Failed to download {file_name} after {retries} attempts.")
        return False
