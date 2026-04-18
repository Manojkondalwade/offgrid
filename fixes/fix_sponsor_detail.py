import os
import re

frontend = r'c:\Users\MANOJ KONDALWADE\OneDrive\Desktop\offgrid-platform\Frontend'

with open(os.path.join(frontend, 'sponsor_dashboard.html'), 'r', encoding='utf-8') as f:
    dashboard_html = f.read()

# Extract Sponsor Nav
match = re.search(r'<nav class="navbar">.*?</nav>', dashboard_html, re.DOTALL)
sponsor_nav = match.group(0) if match else ''

# Open event_detail.html
with open(os.path.join(frontend, 'event_detail.html'), 'r', encoding='utf-8') as f:
    event_detail_html = f.read()

# Replace Nav
new_html = re.sub(r'<nav class="navbar">.*?</nav>', sponsor_nav, event_detail_html, flags=re.DOTALL)

# Fix back buttons
new_html = new_html.replace('href="feed.html"', 'href="sponsor_events.html"').replace('← Back to Feed', '← Back to Events')

# Wait, check if event_manage click also goes to event_detail? Yes, let's also fix organizer_event_detail!
# First finish sponsor
with open(os.path.join(frontend, 'sponsor_event_detail.html'), 'w', encoding='utf-8') as f:
    f.write(new_html)

# Update sponsor_events.html
with open(os.path.join(frontend, 'sponsor_events.html'), 'r', encoding='utf-8') as f:
    events_html = f.read()

events_html = events_html.replace('href="event_detail.html"', 'href="sponsor_event_detail.html"')

with open(os.path.join(frontend, 'sponsor_events.html'), 'w', encoding='utf-8') as f:
    f.write(events_html)
