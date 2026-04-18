import os
import re

frontend_dir = os.path.abspath('Frontend')

student_pages = [
    'explore.html',
    'feed.html',
    'my_events.html',
    'event_detail.html',
    'vote.html',
    'notifications.html',
    'student_profile.html'
]

replacement_nav = """    <ul class="navbar-links">
      <li><a href="student_dashboard.html">🏠 Home</a></li>
      <li><a href="feed.html">📰 Feed</a></li>
      <li><a href="explore.html">🔍 Explore</a></li>
      <li><a href="my_events.html">📅 My Events</a></li>
      <li><a href="vote.html">🗳️ Vote</a></li>
    </ul>"""

def add_active_class(nav_html, page):
    # Depending on the page, inject class="active" into the correct anchor
    if page == 'explore.html': return nav_html.replace('href="explore.html"', 'href="explore.html" class="active"')
    if page == 'feed.html': return nav_html.replace('href="feed.html"', 'href="feed.html" class="active"')
    if page == 'my_events.html': return nav_html.replace('href="my_events.html"', 'href="my_events.html" class="active"')
    if page == 'vote.html': return nav_html.replace('href="vote.html"', 'href="vote.html" class="active"')
    if page == 'student_dashboard.html': return nav_html.replace('href="student_dashboard.html"', 'href="student_dashboard.html" class="active"')
    # notifications and event_detail and student_profile might not have a dedicated active state in this bar
    return nav_html

for page in student_pages:
    path = os.path.join(frontend_dir, page)
    if not os.path.exists(path): continue
    
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # The original nav might have 3 or 4 links depending on the file
    # We replace everything between <ul class="navbar-links"> and </ul>
    new_nav = add_active_class(replacement_nav, page)
    
    html = re.sub(r'<ul class="navbar-links">.*?</ul>', new_nav, html, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Student navbars updated!")
