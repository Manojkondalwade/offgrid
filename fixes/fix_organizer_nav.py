import os
import re

frontend_dir = os.path.abspath('Frontend')

organizer_pages = [
    'dashboard.html',
    'event_manage.html',
    'sponsors.html',
    'analytics.html',
    'organizer_profile.html',
    'create_event.html',
    'proposals.html'
]

replacement_nav = """    <ul class="navbar-links">
      <li><a href="dashboard.html">📊 Dashboard</a></li>
      <li><a href="event_manage.html">📋 Events</a></li>
      <li><a href="sponsors.html">🤝 Sponsors</a></li>
      <li><a href="proposals.html">📋 Proposals</a></li>
      <li><a href="analytics.html">📈 Analytics</a></li>
    </ul>"""

def add_active_class(nav_html, page):
    if page == 'dashboard.html': return nav_html.replace('href="dashboard.html"', 'href="dashboard.html" class="active"')
    if page == 'event_manage.html': return nav_html.replace('href="event_manage.html"', 'href="event_manage.html" class="active"')
    if page == 'sponsors.html': return nav_html.replace('href="sponsors.html"', 'href="sponsors.html" class="active"')
    if page == 'proposals.html': return nav_html.replace('href="proposals.html"', 'href="proposals.html" class="active"')
    if page == 'analytics.html': return nav_html.replace('href="analytics.html"', 'href="analytics.html" class="active"')
    return nav_html

for page in organizer_pages:
    path = os.path.join(frontend_dir, page)
    if not os.path.exists(path): continue
    
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    new_nav = add_active_class(replacement_nav, page)
    
    html = re.sub(r'<ul class="navbar-links">.*?</ul>', new_nav, html, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Organizer navbars updated!")
