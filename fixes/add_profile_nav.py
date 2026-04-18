import os
import re

frontend_dir = os.path.abspath('Frontend')

student_pages = ['explore.html', 'feed.html', 'my_events.html', 'event_detail.html', 'vote.html', 'notifications.html', 'student_profile.html', 'student_dashboard.html']
organizer_pages = ['dashboard.html', 'event_manage.html', 'sponsors.html', 'analytics.html', 'organizer_profile.html', 'create_event.html', 'proposals.html']
sponsor_pages = ['sponsor_dashboard.html', 'sponsor_events.html', 'sponsor_proposals.html', 'sponsor_profile.html']

for f in os.listdir(frontend_dir):
    if not f.endswith('.html'): continue
    path = os.path.join(frontend_dir, f)
    with open(path, 'r', encoding='utf-8') as file:
        html = file.read()
    
    orig_html = html

    # Find the navbar-links closing tag and inject the profile link right before it
    if f in student_pages:
        # Check if already has profile
        if 'href="student_profile.html"' not in html.split('navbar-links')[1].split('</ul>')[0]:
            html = re.sub(r'(<li><a href="vote\.html".*?</a></li>\s*)(</ul>)', r'\1  <li><a href="student_profile.html">👤 Profile</a></li>\n    \2', html)
            # Sometimes vote isn't the last (like student_profile itself might have been messed up)
            # Let's just do a robust insertion before </ul> for student pages
            html = re.sub(r'(</ul\s*>)', r'  <li><a href="student_profile.html">👤 Profile</a></li>\n    \1', html)
            
    elif f in organizer_pages:
        html = re.sub(r'(</ul\s*>)', r'  <li><a href="organizer_profile.html">👤 Profile</a></li>\n    \1', html)

    elif f in sponsor_pages:
        html = re.sub(r'(</ul\s*>)', r'  <li><a href="sponsor_profile.html">👤 Profile</a></li>\n    \1', html)
        
    # Let's clean up double insertions just in case
    html = re.sub(r'(<li><a href=".*?_profile\.html">👤 Profile</a></li>\s*)+', r'\1', html)

    # Active states
    if f == 'student_profile.html': html = html.replace('href="student_profile.html">👤', 'href="student_profile.html" class="active">👤')
    if f == 'organizer_profile.html': html = html.replace('href="organizer_profile.html">👤', 'href="organizer_profile.html" class="active">👤')
    if f == 'sponsor_profile.html': html = html.replace('href="sponsor_profile.html">👤', 'href="sponsor_profile.html" class="active">👤')

    if orig_html != html:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(html)

print("Profile links added to navbars!")
