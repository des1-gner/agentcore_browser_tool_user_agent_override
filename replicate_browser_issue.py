# replicate_browser_issue.py
# This script demonstrates the browser compatibility issue with Chase.com
# The AgentCore Browser includes an AWS identifier in its User-Agent string,
# which may cause Chase's website to show browser compatibility warnings.

from bedrock_agentcore.tools.browser_client import browser_session
from playwright.sync_api import sync_playwright
import time

region = "us-east-1"

with browser_session(region) as client:
    ws_url, headers = client.generate_ws_headers()
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_url, headers=headers)
        
        if browser.contexts:
            page = browser.contexts[0].pages[0] if browser.contexts[0].pages else browser.contexts[0].new_page()
        else:
            context = browser.new_context()
            page = context.new_page()
        
        # Check the default User-Agent string
        # This will show: "Amazon-Bedrock-AgentCore-Browser/1.0" which may trigger Chase's bot detection
        user_agent = page.evaluate("() => navigator.userAgent")
        print(f"User-Agent: {user_agent}\n")
        
        print("Navigating to Chase pre-approval page...")
        page.goto(
            "https://secure.chase.com/web/oao/application/card?cfgCode=PREAPPROVEDCONCC&flowVersion=REACT&cellCode=6TKV#/origination/preapproved/index/index",
            wait_until="domcontentloaded",
            timeout=30000
        )
        
        time.sleep(3)
        page.screenshot(path="chase_blocked.png", full_page=True)
        
        title = page.title()
        print(f"Page title: {title}")
        
        # Chase redirects to "System Requirements" page when it detects the AgentCore Browser identifier
        if "System Requirements" in title:
            print("Chase appears to be blocking the AgentCore Browser identifier")
        
        page_content = page.content()
        update_keywords = [
            "update your browser",
            "browser needs to be updated", 
            "unsupported browser",
            "outdated browser"
        ]
        
        found_issues = [keyword for keyword in update_keywords if keyword.lower() in page_content.lower()]
        if found_issues:
            print(f"Detected compatibility warnings: {found_issues}")
        
        input("Press Enter to close...")