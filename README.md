## README.md

```markdown
# AgentCore Browser User-Agent Workaround

This repository contains example code demonstrating a browser compatibility issue that can occur when using Amazon Bedrock AgentCore Browser with certain websites, and provides a workaround solution.

## Overview

The AgentCore Browser includes an AWS identifier in its User-Agent string for transparency and compliance purposes. I believe what's going on is that some websites have strict bot detection may show browser compatibility warnings when they encounter this identifier, even though the AgentCore Browser runs a reasonably new version of Chrome: [https://chromereleases.googleblog.com/2025/09/stable-channel-update-for-desktop.html](https://developer.chrome.com/release-notes/140)

## Prerequisites

- AWS account with credentials configured
- Python 3.10 or higher
- IAM permissions for Bedrock AgentCore Browser
- Required Python packages:
  ```bash
  pip install bedrock-agentcore playwright
  ```

## Files

- `replicate_browser_issue.py` - Demonstrates the browser compatibility issue
- `workaround_browser_issue.py` - Provides a workaround using CDP to override the User-Agent
- `chase_blocked.png` - Screenshot showing the browser compatibility warning
- `chase_working.png` - Screenshot showing successful page load after applying workaround

## Usage

Run the replication script to see the issue:
```bash
python replicate_browser_issue.py
```

This will generate a screenshot (`chase_blocked.png`) showing the browser compatibility warning:

![Browser Compatibility Issue](chase_blocked.png)

Run the workaround script to bypass the compatibility warning:
```bash
python workaround_browser_issue.py
```

This will generate a screenshot (`chase_working.png`) showing the page loading successfully:

![Successful Page Load](chase_working.png)

## Important Notes

The workaround uses Chrome DevTools Protocol (CDP) to override the User-Agent string and hide automation indicators. Before using this approach in production, consider:
- Your organisation's policies regarding browser identification
- The target website's Terms of Service (ToS)
- Whether transparent identification of automated traffic is required for your use case

## Related Documentation

- [AgentCore Browser Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/browser-tool.html)
- [Playwright Documentation](https://playwright.dev/python/)
```
