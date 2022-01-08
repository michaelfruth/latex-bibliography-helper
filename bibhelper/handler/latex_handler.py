import re
from typing import Union


def extract_booktitle_shortname(booktitle: str) -> Union[str, None]:
    """
    Tries to extract the shortname of the booktitle of a publication. Curly brackets around the title are ignored and
    won't be returned either.

    The following patterns will be recognized.:
    - Shortname followed by year: ... {SHORTNAME} YEAR ....
    - Example: 43rd {ACM/IEEE} Annual ..., {ISCA} 2016, Seoul, South Korea, June 18-22, 2016

    - Shortname at the end: ... {SHORTNAME}
    - Example: 2014 IEEE International Symposium on Workload Characterization {IISWC}

    - Shortname at the beginning: {SHORTNAME} 'YEAR...
    - Example: {PACT} '20: International Conference on Parallel Architectures and Compilation Techniques

    Returns the extracted shortname if found, None otherwise.
    """
    patterns = []

    shortname_year_pattern = re.compile(r'{?\w+}?(?=(\n|\r|\s)+[0-9]{4})')
    patterns.append(shortname_year_pattern)

    shortname_end_pattern = re.compile(r'{[^{]*}$')
    patterns.append(shortname_end_pattern)

    shortname_start_pattern = re.compile(r'(^{?.*}?)(?:(\n|\r|\s)+\'[0-9]{2,4})')
    patterns.append(shortname_start_pattern)

    for shortname_pattern in patterns:
        findings = re.search(shortname_pattern, booktitle)
        if findings:
            # TODO: What if multiple groups were found?
            shortname_groups = findings.groups()

            if len(shortname_groups) >= 1 and len(shortname_groups[0].strip()) > 0:
                # Use groups() for non-capturing groups
                shortname = shortname_groups[0]
            else:
                shortname = findings.group(0)

            # Remove curly braces
            if shortname.startswith("{"):
                shortname = shortname[1:]
            if shortname.endswith("}"):
                shortname = shortname[:-1]
            return shortname
    return None


def curlify(content: str) -> str:
    """
    Adds a pair of curly braces to the content. If the content already contains curly brackets, nothing will happen.

    Example:
    - curlify("Hello") returns "{Hello}".
    - curlify("{Hello}") returns "{Hello}".
    """
    curlify_pattern = re.compile(r'^{.*}$', re.DOTALL)
    # Check if curly brackets are already set
    if not re.fullmatch(curlify_pattern, content):
        # Add extra curly brackets to title. Preserves lowercase/uppercase in BIBTeX
        content = "{{{}}}".format(content)
    return content
