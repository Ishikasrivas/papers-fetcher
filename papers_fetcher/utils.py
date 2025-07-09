from typing import List

# List of keywords that suggest an academic affiliation
ACADEMIC_KEYWORDS = [
    "university", "institute", "college", "hospital", "school", "center", "centre", "faculty", "department", "academy", "lab", "laboratory"
]

# List of keywords that suggest a company affiliation (expand as needed)
COMPANY_KEYWORDS = [
    "pharma", "biotech", "inc", "ltd", "llc", "gmbh", "corp", "company", "co.", "s.a.", "s.p.a.", "plc", "ag", "industries"
]

def is_non_academic_affiliation(affiliation: str) -> bool:
    """
    Heuristic to determine if an affiliation is non-academic (likely a company).
    Returns True if affiliation does not contain academic keywords.
    """
    affiliation_lower = affiliation.lower()
    return not any(keyword in affiliation_lower for keyword in ACADEMIC_KEYWORDS)

def extract_company_names(affiliations: List[str]) -> List[str]:
    """
    Extract company names from a list of affiliations using company-related keywords.
    Returns a list of unique company names found.
    """
    companies = set()
    for aff in affiliations:
        aff_lower = aff.lower()
        if is_non_academic_affiliation(aff) and any(kw in aff_lower for kw in COMPANY_KEYWORDS):
            companies.add(aff.strip())
    return list(companies)
