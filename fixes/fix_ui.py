import os
import re

frontend_dir = os.path.abspath('Frontend')

def read_file(name):
    with open(os.path.join(frontend_dir, name), 'r', encoding='utf-8') as f:
        return f.read()

def write_file(name, content):
    with open(os.path.join(frontend_dir, name), 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Read source files
profile_src = read_file('profile.html')
explore_src = read_file('explore.html')
proposals_src = read_file('proposals.html')

# ---------------------------------------------------------
# Create student_profile.html
# ---------------------------------------------------------
student_prof = profile_src.replace('href="profile.html"', 'href="student_profile.html"')
write_file('student_profile.html', student_prof)

# ---------------------------------------------------------
# Create organizer_profile.html
# ---------------------------------------------------------
org_nav = """    <ul class="navbar-links">
      <li><a href="dashboard.html">📊 Dashboard</a></li>
      <li><a href="event_manage.html">📋 Events</a></li>
      <li><a href="sponsors.html">🤝 Sponsors</a></li>
      <li><a href="analytics.html">📈 Analytics</a></li>
    </ul>
    <div class="navbar-actions">
      <span class="badge badge-purple">Organizer</span>
      <div class="avatar" onclick="window.location='organizer_profile.html'" style="cursor:pointer;" title="Profile">CD</div>
    </div>"""
org_prof = profile_src.replace('AS', 'CD') # Change all AS to CD
org_prof = re.sub(r'<ul class="navbar-links">.*?</div>\n    </div>', org_nav, org_prof, flags=re.DOTALL)
org_prof = org_prof.replace('Arjun Sharma', 'CodeDecode Club')
org_prof = org_prof.replace('Student · CCE-3, SY2024', 'Verified Organizer · Technical')
# Change Quick links
org_quick_links = """<a href="event_manage.html" class="btn btn-ghost btn-sm" style="justify-content:flex-start;">📋 Manage Events</a>
            <a href="analytics.html" class="btn btn-ghost btn-sm" style="justify-content:flex-start;">📈 Analytics</a>
            <a href="login.html" class="btn btn-danger btn-sm" style="justify-content:flex-start;">🚪 Sign Out</a>"""
org_prof = re.sub(r'<a href="my_events\.html".*?Sign Out</a>', org_quick_links, org_prof, flags=re.DOTALL)
org_prof = org_prof.replace('First Name', 'Club Name')
org_prof = org_prof.replace('Arjun', 'CodeDecode')
org_prof = org_prof.replace('Last Name', 'Category')
org_prof = org_prof.replace('Sharma', 'Technical')
org_prof = org_prof.replace('arjun.sharma@college.edu', 'contact@codedecode.org')
write_file('organizer_profile.html', org_prof)

# ---------------------------------------------------------
# Create sponsor_profile.html
# ---------------------------------------------------------
sponsor_nav = """    <ul class="navbar-links">
      <li><a href="sponsor_dashboard.html">🏠 Dashboard</a></li>
      <li><a href="sponsor_events.html">🔍 All Events</a></li>
      <li><a href="sponsor_proposals.html">📋 Proposals</a></li>
    </ul>
    <div class="navbar-actions">
      <span class="badge badge-orange">Sponsor</span>
      <div class="avatar" onclick="window.location='sponsor_profile.html'" style="cursor:pointer;" title="Profile">TC</div>
    </div>"""
sp_prof = profile_src.replace('AS', 'TC')
sp_prof = re.sub(r'<ul class="navbar-links">.*?</div>\n    </div>', sponsor_nav, sp_prof, flags=re.DOTALL)
sp_prof = sp_prof.replace('Arjun Sharma', 'TechCorp India')
sp_prof = sp_prof.replace('Student · CCE-3, SY2024', 'Premium Corporate Sponsor')
sp_quick_links = """<a href="sponsor_events.html" class="btn btn-ghost btn-sm" style="justify-content:flex-start;">🔍 Browse Events</a>
            <a href="sponsor_proposals.html" class="btn btn-ghost btn-sm" style="justify-content:flex-start;">📋 My Proposals</a>
            <a href="login.html" class="btn btn-danger btn-sm" style="justify-content:flex-start;">🚪 Sign Out</a>"""
sp_prof = re.sub(r'<a href="my_events\.html".*?Sign Out</a>', sp_quick_links, sp_prof, flags=re.DOTALL)
sp_prof = sp_prof.replace('First Name', 'Company Name')
sp_prof = sp_prof.replace('val="Arjun"', 'val="TechCorp India"') # Will fix below properly
sp_prof = sp_prof.replace('value="Arjun"', 'value="TechCorp India"')
sp_prof = sp_prof.replace('Last Name', 'Industry')
sp_prof = sp_prof.replace('value="Sharma"', 'value="Software & IT"')
sp_prof = sp_prof.replace('arjun.sharma@college.edu', 'partnerships@techcorp.in')
write_file('sponsor_profile.html', sp_prof)

# ---------------------------------------------------------
# Create sponsor_events.html
# ---------------------------------------------------------
sp_events = explore_src.replace('Explore Events', 'Sponsor Events')
sp_events = sp_events.replace('Find your next favorite college event', 'Discover events matching your company interests')
# Replace the navbar entirely
sp_events = re.sub(r'<ul class="navbar-links">.*?</div>\n    </div>', sponsor_nav, sp_events, flags=re.DOTALL)
write_file('sponsor_events.html', sp_events)

# ---------------------------------------------------------
# Create sponsor_proposals.html
# ---------------------------------------------------------
sp_prop = proposals_src.replace('Incoming proposals for your events', 'Proposals you have sent to clubs')
sp_prop = sp_prop.replace('Pending Proposals', 'Pending Responses')
sp_prop = sp_prop.replace('Total Offered', 'Total Budget Invested')
sp_prop = sp_prop.replace('Active Sponsors', 'Accepted Agreements')
# Replace the navbar entirely
sp_prop = re.sub(r'<ul class="navbar-links">.*?</div>\n    </div>', sponsor_nav, sp_prop, flags=re.DOTALL)
write_file('sponsor_proposals.html', sp_prop)

# ---------------------------------------------------------
# Mass replace avatars and links in all 18 files
# ---------------------------------------------------------
student_avatar = r'<div class="avatar" onclick="window.location=\'student_profile.html\'" style="cursor:pointer;" title="Profile">AS</div>'
org_avatar = r'<div class="avatar" onclick="window.location=\'organizer_profile.html\'" style="cursor:pointer;" title="Profile">CD</div>'
sponsor_avatar = r'<div class="avatar" onclick="window.location=\'sponsor_profile.html\'" style="cursor:pointer;" title="Profile">TC</div>'

for f in os.listdir(frontend_dir):
    if not f.endswith('.html'): continue
    
    html = read_file(f)
    orig_html = html
    
    # 1. Convert simple <div class="avatar">AS</div> to clickable
    html = re.sub(r'<div class="avatar"( title="Profile")?>AS</div>', student_avatar, html)
    html = re.sub(r'<div class="avatar" onclick="window\.location=\'profile\.html\'"( title="Profile")?>AS</div>', student_avatar, html)
    
    # Convert CD to clickable
    html = re.sub(r'<div class="avatar">CD</div>', org_avatar, html)
    
    # Convert TC to clickable
    html = re.sub(r'<div class="avatar">TC</div>', sponsor_avatar, html)

    # 2. Convert standard href="profile.html" to student_profile.html inside student pages
    # Since only students had profile links before:
    html = html.replace('href="profile.html"', 'href="student_profile.html"')
    
    # 3. For Sponsor pages, fix navigation links
    if f in ['sponsor_dashboard.html', 'sponsor_events.html', 'sponsor_proposals.html']:
        # They should point to sponsor_events.html instead of sponsors.html
        html = html.replace('href="sponsors.html"', 'href="sponsor_events.html"')
        # They should point to sponsor_proposals.html instead of proposals.html
        html = html.replace('href="proposals.html"', 'href="sponsor_proposals.html"')

    if html != orig_html:
        write_file(f, html)

# Remove the old profile.html
try:
    os.remove(os.path.join(frontend_dir, 'profile.html'))
except: pass

print("Done generating profiles, sponsor pages, and fixing navbars!")
