# dynasty-scans-scraper

I really wanted to read futaribeya on my kindle so I made this.

## Description

A [dynasty scans](https://dynasty-scans.com/) scraper that converts each volume of a series into a pdf for you.

## Why?

It's easy to read manga online, not so easy to find pdfs/epubs of them (light novels are easier). Especially because its yuri.

## Use

Run `main.py`, enter the link and it should be good.

Sometimes the images fail to download or are truncated, run `redownloader.py` to fix.

## How it works

`scraper.py` scrapes the image download links for each volume/chapter from dynasty-scans, `download.py` async downloads the images (this takes some time, you can increase number of simulteanous coroutines in `main.py` at `asyncio.Semaphore(10)`, but i believe this leads to higher chance of a truncated image being downloaded), and `pdf.py` uses PyPDF2 to convert each volume into a pdf (this takes slightly longer).

Find something fun to do in the meantime while waiting :D
