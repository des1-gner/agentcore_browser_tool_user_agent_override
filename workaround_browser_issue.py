# workaround_browser_issue.py
# This script works around the browser compatibility issue by overriding the User-Agent string
# and hiding automation indicators using Chrome DevTools Protocol (CDP).
# 
# Important: This approach removes the AWS identifier from the User-Agent.
# Consider whether this aligns with your organization's policies and the 
# target website's Terms of Service before using in production.

from bedrock_agentcore.tools.browser_client import browser_session
from playwright.sync_api import sync_playwright
import time

region = "us-east-1"

with browser_session(region) as client:
    ws_url, headers = client.generate_ws_headers()
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_url, headers=headers)
        
        if browser.contexts:
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
        else:
            print("No context available")
            exit(1)
        
        # Create CDP session to override browser properties
        cdp = context.new_cdp_session(page)
        
        # Override User-Agent to match a standard Chrome browser
        # This removes the "Amazon-Bedrock-AgentCore-Browser/1.0" identifier
        standard_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        
        cdp.send('Network.setUserAgentOverride', {
            'userAgent': standard_ua,
            'platform': 'Win32',
            'acceptLanguage': 'en-US,en;q=0.9'
        })
        
        # Hide automation signals that bot detection systems check
        cdp.send('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {
                            0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                            description: "Portable Document Format",
                            filename: "internal-pdf-viewer",
                            length: 1,
                            name: "Chrome PDF Plugin"
                        },
                        {
                            0: {type: "application/pdf", suffixes: "pdf", description: "Portable Document Format"},
                            description: "Portable Document Format", 
                            filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                            length: 1,
                            name: "Chrome PDF Viewer"
                        }
                    ]
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
                
                delete navigator.__proto__.webdriver;
                
                window.chrome = {
                    runtime: {},
                    loadTimes: function() {},
                    csi: function() {},
                    app: {}
                };
                
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            '''
        })
        
        user_agent = page.evaluate("() => navigator.userAgent")
        print(f"Modified User-Agent: {user_agent}")
        
        webdriver_status = page.evaluate("() => navigator.webdriver")
        print(f"navigator.webdriver: {webdriver_status}\n")
        
        print("Navigating to Chase pre-approval page...")
        page.goto(
            "https://secure.chase.com/web/oao/application/card?cfgCode=PREAPPROVEDCONCC&flowVersion=REACT&cellCode=6TKV#/origination/preapproved/index/index",
            wait_until="domcontentloaded",
            timeout=30000
        )
        
        time.sleep(3)
        page.screenshot(path="chase_working.png", full_page=True)
        
        title = page.title()
        print(f"Page title: {title}")
        
        if "System Requirements" not in title:
            print("Page loaded successfully without browser compatibility warnings")
        
        input("Press Enter to close...")