import markdown
from yaml import load, Loader
from bibgen import generate_bibliography

def generate_research_summary(filename):
    """Generates Research Summary From a Markdown File

    # Arguments
     - filename: A markdown file containing a research summary

    # Returns
    An html string containing a header with id 'research' and the
    markdown converted to html encapsulated in a div with class 'research'.
    """
    out = "<h2 id=\"research\">Research</h2>\n"
    with open(filename) as f:
        text = f.read()
    out += "<div class=\"research\">\n"
    out += markdown.markdown(text)
    out += "\n</div>\n\n"
    return out

def generate_coursework(coursework):
    """ Generates an html list of the coursework, with a header

    # Arguments
     - coursework: A list of dicts containing the term and courses
    
    # Returns
    An html string representing the coursework

    # Notes
    The header has id 'graduate-level-coursework'.
    """
    out = "<h2 id=\"graduate-level-coursework\">Graduate Level Coursework</h2>\n"
    for school in coursework.values():
        out += "\n<h3>"+school['name']+"</h3>\n"
        for term in school['terms']:
            out += "\n<p>" + term['time'] + "</p>\n"
            out += "<ul>\n"
            for course in term.keys():
                if course != 'time':
                    out += "<li>"
                    out += term[course]['number']
                    out += " — "
                    out += term[course]['title']
                    out += "</li>\n"
            out += "</ul>\n"
    return out

def generate_service(service):
    """ Generates HTML section regarding service contributions

    # Arguments
     - service: A dictionary containing service contributions

    # Returns
    An html string representing the service contributions

    # Notes
    The `service` dictionary is formatted with two keys:
     - 'committees' - List of dictionaries with keys 'position', 'time', 'venue'
     - 'reviewer' - list of dictionaries with keys 'time', 'venue'

    If the dictionary is missing a key, the function will error.
    """

    out = "<h2 id=\"service\">Service</h2>\n\n"
    out += "<h3>Organizational</h3>\n"
    out += "<ul>\n"
    for role in service['committees']:
        out += "<li>"
        out += role['position'] + " — " + role['venue'] + " — " + role['time']
        out += "</li>\n"
    out += "</ul>\n"

    out += "\n<h3>Reviewer</h3>\n"
    out += "<ul>\n"
    for role in service['reviewer']:
        out += "<li>"
        out += role['time'] + " — " + role['venue']
        out += "</li>\n"
    out += "</ul>\n"
    return out

def generate_teaching(teaching, mentorship):
    """ Generates HTML section regarding teaching experience

    # Arguments
     - teaching: A list containing teaching contribution dicitonaries
     - mentorship: A list containing mentorship contributions

    # Returns
    An html string representing the teaching and mentorship contributions

    # Notes
    The `teaching` dictionaries are formatted with two keys:
     - 'name': String representing the name of the university
     - 'courses': list of dictionaries with representing courses taught

    Each course dictionary contains the following four keys:
     - 'position': Name of the position (i.e. Teaching Assistant)
     - 'number': Course number (i.e. "ECE 551")
     - 'title': Full title of the course
     - 'term': Term the course was taught

    If the dictionary is missing a key, the function will error.
    """

    out = "<h2 id=\"teaching\">Teaching</h2>\n\n"
    for school in teaching:
        out += "<h3>" + school['name'] + "</h3>\n\n"
        out += "<ul class=\"teachinglist\">\n"
        for course in school['courses']:
            out += "<li>"
            out += course['title'] + " — "
            out += course['number'] + " — "
            out += course['position'] + " — "
            out += course['term']
            out += "</li>\n"
        out += "</ul>\n\n"

    out += "<h3>Mentorship</h3>\n"
    out += "<ul class=\"teachinglist\">\n"
    for item in mentorship:
        out += "<li>"
        out += item
        out += "</li>\n"
    out += "</ul>\n"

    return out

def generate_other_research(research):
    """ Generates HTML section regarding unpublished research jobs

    # Arguments
     - research: A list containing research job dicitonaries

    # Returns
    An html string representing the research jobs

    # Notes
    The `research` dictionaries are formatted with two keys:
     - 'company': Name of the company
     - 'position': Name of the position
     - 'groupname': Name of the group
     - 'time': Time of the role
     - 'projects': List of projects completed

    If the dictionary is missing a key, the function will error.
    """

    out = """<h2 id="past-research-jobs">Past Research Jobs</h2>\n"""
    for role in research:
        out += "<h3>" + role['company'] + " — " + role['position'] + "</h3>\n"
        out += "<p><em>" + role['groupname'] + "</em> — "
        out += role['time'] + "</p>\n"
        out += "<ul>\n"
        for detail in role['projects']:
            out += "<li>" + detail + "</li>\n"
        out += "</ul>\n"
    return out
    
def generate_acknowledgements():
    """Returns an html string representing the acknowledgements"""

    out = """<div class="ack">This webpage uses the fonts <a href="https://github.com/source-foundry/Hack">Hack</a>, <a href="https://boxicons.com/">Boxicons</a>, <a href="https://jpswalsh.github.io/academicons/">Academicons</a> and color palette <a href="https://www.nordtheme.com/">Nord</a>.<br /><br />\n"""
    out += """This webpage is (mostly) generated from a yaml cv using <a href="https://github.com/Helmuthn/webcvgen">webcvgen</a>\n"""
    out += "</div>\n"
    return out

def generate_sidebar(about):
    """ Generates the sidebar based on a dictionary of information

    # Arguments
     - about: A dict containing the relevant information

    # Returns
    An html string containing the about information

    # Required Fields In about

     - profile: Relative path of the profile picture
     - name: Name of the website owner
     - job: A dict with information about the current job containing
         - position: The name of the role
         - company: The organization
     - interests: A dict containing a title and a list of interests
         - title: The title for the interest section (i.e. research interests)
         - interestlist: A list of interests to be included
     - education: A list of dicts with basic education information
         - description: Brief description, i.e. name of the degree
         - year: The year of the degree
         - school: The school name
     - linkedin: URL for the linkedin profile, string
     - github: URL of a Github profile, string
     - scholar: URL of a google scholar profile, string
     - email: contact email, string.

    """
    out = "<div class=\"sidebar\">\n"
    out += "<img src=\"" + about['profile'] + "\" alt=\"Profile Picture\">\n"
    out += "<h4>" + about['name'] + "</h4>\n"
    out += "<div class=\"sidetitle\"><strong>" + about['job']['position'] + "</strong></div><br />\n"
    out += "<div class=\"company\">\n"
    out += about['job']['company'].replace('\\','<br />\n')
    out += "</div><br />\n"
    out += "<hr>\n"
    out += "<div class=\"sidetitle\"><strong>" + about['interests']['title'] + "</strong></div></br />\n"
    for interest in about['interests']['interestlist']:
        out += "<div class=\"interest\">" + interest + "</div><br />"
    out += "<hr>\n"
    out += "<div class=\"sidetitle\"><strong>Education</strong></div><br />\n"
    for degree in about['education']:
        out += "<div class=\"degree\">\n"
        out += degree['description'] + ", "
        out += degree['year'] + "<br />"
        out += degree['school'] 
        out += "</div><br />\n"
    out += "<hr>\n"
    out += "<div class=\"linklist\">\n"
    out += "<a href=\"" + about['linkedin'] + "\">"
    out += "<i class=\"bx bxl-linkedin-square bx-md\"></i>"
    out += "</a>\n"
    out += "<a href=\"" + about['github'] + "\">"
    out += "<i class=\"bx bxl-github bx-md\"></i>"
    out += "</a>\n"
    out += "<a href=\"" + about['scholar'] + "\">"
    out += "<i class=\"ai ai-google-scholar-square ai-2x\"></i>"
    out += "</a>\n"
    out += "<a href=\"mailto:" + about['email'] + "\">"
    out += "<i class=\"bx bxs-envelope bx-md\"></i>"
    out += "</a>\n"
    out += "</div>\n"
    out += "</div>\n"

    return out
    
def generate_main_content(data):
    """ Generate the main html content

    # Arguments
     - data: A dictionary generated from a yaml file representing a cv

    # Returns
    A string of html representing the main content of a cv website

    # Notes
    The dictionary must have the following keys for the associated functions
     - about: generate_research_summary, generate_bibliography
     - teaching: generate_teaching
     - mentorship: generate_teaching
     - service: generate_service
     - coursework: generate_coursework
     - oldresearch: generate_other_research

    See associated functions for details on the values of the keys.
    """

    name = data['about']['name']
    name = name.split(' ')[-1] # Get the last name
    out = "<div class=\"main-content\">\n"
    out += generate_research_summary(data['about']['summary'])
    out += "<hr>\n\n"
    out += generate_bibliography(data['about']['bibtex'], name)
    out += "\n<hr>"
    out += generate_teaching(data['teaching'], data['mentorship'])
    out += "\n<hr>"
    out += generate_service(data['service'])
    out += "\n<hr>\n\n"
    out += generate_coursework(data['coursework'])
    out += "\n<hr>\n\n"
    out += generate_other_research(data['oldresearch'])
    out += "\n<hr>\n\n"
    out += generate_acknowledgements() 
    out += "</div>\n"

    return out

def generate_navigation():
    """ Returns the html for the navigation bar """

    out =  "<div class=\"navigation\">\n"
    out += "<ul class=\"navbar\">\n"
    out += "<li><a href=\"#research\">Research</a></li>\n"
    out += "<li><a href=\"#publications\">Publications</a></li>\n"
    out += "<li><a href=\"#teaching\">Teaching</a></li>\n"
    out += "<li><a href=\"#service\">Service</a></li>\n"
    out += "<li><a href=\"#graduate-level-coursework\">Coursework</a></li>\n"
    out += "<li><a href=\"#past-research-jobs\">Other</a></li>\n"
    out += "</ul>\n"
    out += "</div>\n"
    return out

def generate_website(savefile, cvfile):
    """ Generate and save a single page website based on a YAML cv

    # Arguments
     - cvfile: String containing the path to the yaml file
     - savefile: Location of file to save
    """

    with open(cvfile) as f:
        data = load(f, Loader=Loader)
    name = data['about']['name']
    out = f"""<!doctype html>
<html lang="en">
<head>
<title>{name}</title>
<meta charset="utf-8">
<meta name="description" content="{name}'s Online CV">
<meta name="viewport" content="initial-scale=1.0, maximum-scale=1.0, width=device-width, user-scalable=no">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/hack-font/3.3.0/web/hack-subset.css" integrity="sha512-/qDvulLjBL2EaRMJOIXQhkiKwhlkDdT2qY000siiuS02OOxbL8BrBOW1aJBjPkC/QJzc8VbnIe4zzGsISNnTHg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
<link href='https://unpkg.com/boxicons@2.1.2/css/boxicons.min.css' rel='stylesheet'>
<link rel="stylesheet" href="style/academicons/css/academicons.min.css"/>
<link rel="stylesheet" href="style/sheet.css">
</head>
<body>
<div class="container">"""
    out += generate_navigation()
    out += generate_sidebar(data['about'])
    out += generate_main_content(data)
    out += "</div>\n</body>\n</html>"
    with open(savefile, "w") as f:
        f.write(out)

if __name__=="__main__":
    generate_website("index.html", "data/cv.yaml")
