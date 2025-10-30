

"""
_run_test_id is always passed to all the methods that you create
"""
import httpx
import requests
import subprocess
import argparse
import asyncio
import logging
import sys
import ssl
import types
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import socket

from web_status_checker.WebCrawler import LinkChecker, LinkInfo

async def run_link_checker(**kwargs):
    """
    Runs an asynchronous link check on the provided website URL.

    Prompt example:
        "Run the link checker on [link_here] with internal link crawling enabled (max depth 2).
        Return a list of all links found with their HTTP status, note, and source URL as text output.
        Also include conclusions like amount of links checked, percentage passed/failed."

    Parameters (passed via kwargs):
        website_url (str): The URL to start crawling from. Required.
        follow_internal (bool): Whether to follow internal links. Default: False.
        max_depth (int): Maximum depth for internal crawling. Default: 1.

    Returns:
        List[dict]: A list of dictionaries containing:
            - url (str): The URL that was checked.
            - status (int or str): The HTTP status code or 'ERROR' if unreachable.
            - note (str): A human-readable explanation of the status.
            - source (str): The URL where the link was found.
            - type (str): 'Internal', 'External', or 'Form'.

        Or dict with error key if missing argument or failure.
    """
    print(f"[DEBUG] run_link_checker() called on machine: {socket.gethostname()}")
    website_url = kwargs.get("website_url")
    print(f"[DEBUG] website_url: {website_url}")
    if not website_url:
        return {"error": "Missing required argument 'website_url'."}

    follow_internal = kwargs.get("follow_internal", False)
    max_depth = kwargs.get("max_depth", 1)
    timeout = kwargs.get("timeout", 300)
    only_broken = kwargs.get("only_broken", False)

    # Optional: enforce max_depth limit to avoid huge crawls
    # if max_depth > 2:
        # max_depth = 2  # limit max_depth to 2 inside AI environment

    try:
        checker = LinkChecker()
        user_agent = kwargs.get("user_agent") or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
        print(f"[DEBUG] Using User-Agent: {user_agent}")

        original_extract_links = checker.extract_links

        def patched_extract_links(self, url, attempts=3):
            headers = {
                'User-Agent': user_agent,
                'Referer': url,
                'Accept': 'text/html,application/xhtml+xml',
            }
            for attempt in range(attempts):
                try:
                    response = httpx.get(url, headers=headers, timeout=300, follow_redirects=True)
                    if "html" not in response.headers.get("Content-Type", ""):
                        logging.warning(f"Non-HTML content from {url}. Skipping.")
                        return set(), "Non-HTML content"

                    soup = BeautifulSoup(response.text, 'html.parser')
                    links = {
                        urljoin(url, link.get('href'))
                        for link in soup.find_all('a')
                        if link.get('href')
                    }

                    logging.info(f"Extracted {len(links)} links from {url}")
                    return links, None

                except httpx.RequestError as e:
                    logging.warning(f"Request failed for {url}: {str(e)}")
                    if attempt == attempts - 1:
                        return set(), str(e)
                except Exception as e:
                    logging.warning(f"Error extracting links from {url}: {str(e)}")
                    if attempt == attempts - 1:
                        return set(), str(e)

        checker.extract_links = types.MethodType(patched_extract_links, checker)
        results = await asyncio.wait_for(
            checker.crawl_and_check_links(
                start_url=website_url,
                follow_internal_links=follow_internal,
                max_depth=max_depth
            ),
            timeout=timeout
        )
        print(f"[DEBUG] crawl_and_check_links returned {len(results)} links")
        if not results:
            return {
                "error": (
                    f"No links found when crawling {website_url}. "
                    f"Make sure extract_links() sets headers like User-Agent correctly."
                )
            }


    except asyncio.TimeoutError:

        return {"error": f"Timed out after {timeout}s."}

    except Exception as e:

        return {"error": f"Exception: {str(e)}"}

    formatted = [{

        "url": r.url,

        "status": r.status_code,

        "note": r.note,

        "source": r.source_url,

        "type": r.source_type

    } for r in results]

    if only_broken:
        formatted = [r for r in formatted if r["status"] != 200]

    passed = sum(1 for r in formatted if r["status"] == 200)

    failed = len(formatted) - passed

    summary = {

        "total_links": len(formatted),

        "passed": passed,

        "failed": failed,

        "pass_rate": round(passed / len(formatted) * 100, 2) if formatted else 0

    }

    return {"results": formatted, "summary": summary}
