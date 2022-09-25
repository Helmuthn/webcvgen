import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author

############################################
########### High Level Functions ########### 
############################################

def generate_bibliography(filename, myname):
    """Generates a List of Publications from a Bibtex File

    # Arguments
     - filename: The name of the Bibtex file to be parsed
     - myname: The last name of the website owner

    # Returns
    A string of HTML including a heading and list of publications
    using the <details> and <summary> tags to include both the
    full IEEE formatted publication and the abstract.

    # Notes
    The header has the id 'publications'.
    The details tag has the class 'publication'.
    The abstract is in a div with class 'pub-details'.
    """
    def customizations(record):
        record = author(record)
        return record
    parser = BibTexParser()
    parser.customization = customizations
    parser.homogenize_fields = True

    with open(filename) as f:
        bib_database = bibtexparser.load(f, parser=parser)

    # Sort the list of publications by year
    bibliography = sorted(bib_database.entries, 
                          key=lambda d: d['year'],
                          reverse=True)

    # Get a list of publications without a year "i.e. under review"
    otherlabels = []
    otherentries = []
    for entry in bib_database.entries:
        if not entry['year'].isnumeric():
            status = entry['year'].title()
            if not status in otherlabels:
                otherlabels.append(status)
                otherentries.append([entry])
            else:
                otherentries[otherlabels.index(status)].append(entry)

    # Append fully published papers
    out = "<h2 id=\"publications\">Publications</h2>"
    for entry in bibliography:
        if entry['year'].isnumeric():
            out += generate_bibliography_entry(entry, myname)

    # Append other status papers
    for ind in range(len(otherlabels)):
        out += f"<h3>{otherlabels[ind]}</h3>"
        for entry in otherentries[ind]:
            out += generate_bibliography_entry(entry, myname)

    return out


def generate_bibliography_entry(entry, myname):
    """Generates HTML Entry From Bibtex Dict as summary and details

    Returns an html string using the <details> and <summary> tags containing
    an IEEE formatted reference and the abstract.

    # Arguments
     - entry: Dictionary containing the bibtex data
     - myname: The last name of the author

    # Returns
    A string containing the citation and abstract.
    """
    out = "<details class=\"publication\">\n"
    out += "<summary>"
    out += generate_bibliography_reference(entry, myname)
    out += "</summary>\n"
    out += "<br />\n"
    out += "<div class=\"pub-details\">\n"
    if 'abstract' in entry:
        out += "<strong>Abstract</strong>: "
        out += entry['abstract']
    else:
        out += "Abstract Coming Soon"
    out += "</div>\n"
    out += "\n</details><br />\n\n"
    return out

def generate_bibliography_reference(entry, myname):
    """Generates the IEEE reference from a Bibtex dict.

    # Arguments
     - entry: Dictionary containing the bibtex data
     - myname: The last name of the author

    # Returns
    A string containing the IEEE formatted citation.
    """
    if entry['ENTRYTYPE'] == 'inproceedings':
        return generate_bibliography_reference_conference(entry, myname)
    if entry['ENTRYTYPE'] == 'article':
        return generate_bibliography_reference_journal(entry, myname)
    return generate_bibliography_reference_misc(entry, myname) 
    
#################################################
########### Reference Type Formatting ########### 
#################################################

def generate_bibliography_reference_conference(entry, myname):
    """Generates HTML Conference Entry From Bibtex Dict

    # Arguments
     - entry: Dictionary containing the bibtex data
     - myname: The last name of the author

    # Returns
    An IEEE reference formatted string, with `myname` bold
    through the <strong> tag.

    # Notes
    Requires the following fields in entry
     - author: A list of author names
     - title: The title of the publication
     - booktitle: The publication venue
     - year: The year of publication
     - doi: The doi for identification
     - url: A link where the reference can be found

    If any fields are missing, the function will fail.
    """
    out = ""
    out += generate_bibliography_authors(entry['author'], myname)
    out += generate_bibliography_title(entry['title'])
    out += generate_bibliography_booktitle(entry['booktitle'])
    out += generate_bibliography_year(entry['year'])
    out += generate_bibliography_pages(entry['pages'])
    out += generate_bibliography_doi(entry['doi'], entry['url'])

    return out

def generate_bibliography_reference_journal(entry, myname):
    """Generates HTML Journal Entry From Bibtex Dict

    # Arguments
     - entry: Dictionary containing the bibtex data
     - myname: The last name of the author

    # Returns
    An IEEE referrence formatted string, with `myname` bold
    through the <strong> tag.

    # Notes
    Requires the following fields in entry
     - author: A list of author names
     - title: The title of the publication
     - journal: The journal name
     - volume: The journal volume
     - pages: The publication venue
     - year: The year of publication
     - doi: The doi for identification
     - url: A link where the reference can be found

    If any fields are missing, the function will fail.
    """
    out = ""
    out += generate_bibliography_authors(entry['author'], myname)
    out += generate_bibliography_title(entry['title'])
    out += generate_bibliography_journal(entry['journal'])
    out += generate_bibliography_volume(entry['volume'])
    out += generate_bibliography_pages(entry['pages'])
    out += generate_bibliography_year(entry['year'])
    out += generate_bibliography_doi(entry['doi'], entry['url'])

    return out

def generate_bibliography_reference_misc(entry, myname):
    """Generates HTML Misc Entry From Bibtex Dict

    # Arguments
     - entry: Dictionary containing the bibtex data
     - myname: The last name of the author

    # Returns
    An IEEE referrence formatted string, with `myname` bold
    through the <strong> tag.

    # Notes
    Requires the following fields in entry
     - author: A list of author names
     - title: The title of the publication

    If any fields are missing, the function will fail.
    """
    out = ""
    out += generate_bibliography_authors(entry['author'], myname)
    out += generate_bibliography_title(entry["title"], True)

    return out


#####################################################
########### Detailed Reference Formatting ########### 
#####################################################

def generate_bibliography_authors(authors, myname):
    """Generates HTML author list

    # Arguments
     - authors: A list of author names
     - myname: The last name of the website owner

    # Returns
    An HTML string representing the author list in the IEEE
    format, with `myname` made bold through the <strong> tag

    # Notes
    Only checks the last name. If you have a common last name,
    then this function may need to be modified.
    """
    out = ""
    for item, name in enumerate(authors):
        if item == len(authors) - 1:
            out += " and "
        elif item > 0:
            out += ", "
        names = name.split(', ')
        if names[0] == myname:
            out += """<strong>"""
            out += names[1][0] + """. """ + names[0]
            out += """</strong>"""
        else:
            for i in range(1, len(names)):
                out += names[i][0] + ". "
            out += names[0]
    out += ", "
    return out

def generate_bibliography_title(title, final = False):
    """Adds appropriate punctuation to the title for an IEEE citation

    # Arguments
     - title: A string containing the title
     - final: Boolean representing if the title is the final element

    # Returns
    The title string in unicode quotation marks, with a comma or
    period depending on if it is the final element or not.
    """
    if not final:
        return "“" + title + ",” "
    return "“" + title + ".”"

def generate_bibliography_booktitle(booktitle):
    """Adds appropriate punctuation to the venue for an IEEE citation

    # Arguments
     - booktitle: The publication venue

    # Returns
    A string with the additional punctuation
    """
    return booktitle + ", "

def generate_bibliography_journal(journal):
    """Adds appropriate punctuation to the journal name for an IEEE citation

    # Arguments
     - journal: The journal name

    # Returns
    A string with the additional formatting
    """
    return "in " + journal + ", "

def generate_bibliography_volume(volume):
    """Adds appropriate punctuation to the volume number for an IEEE citation

    # Arguments
     - volume: String containing the volume number

    # Returns
    A string with the additional formatting
    """
    return "vol. " + volume + ", "

def generate_bibliography_year(year):
    """Adds appropriate punctuation to the year for an IEEE citation

    # Arguments
     - year: String containing the publication year

    # Returns
    A string with the additional formatting
    """
    return year + ", "

def generate_bibliography_pages(pages):
    """Adds appropriate punctuation to the page numbers for an IEEE citation

    # Arguments
     - pages: String containing the publication page range

    # Returns
    A string with the additional formatting
    """
    return "pp. " + pages + ", "

def generate_bibliography_doi(doi, url):
    """Adds appropriate punctuation to the doi for an IEEE citation, with link

    # Arguments
     - doi: String containing the publication doi
     - url: A url (commonly the doi) where the publication can be accessed

    # Returns
    An HTML string with the reference format and the doi link
    """
    return "doi: <a href=\"" + url + "\">" + doi + "</a>."

