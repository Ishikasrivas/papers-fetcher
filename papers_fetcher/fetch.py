from typing import List, Dict, Optional
from .utils import is_non_academic_affiliation, extract_company_names
import requests
import logging
from lxml import etree

PUBMED_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

class Paper:
    """
    Data class for storing paper information.
    """
    def __init__(self, pubmed_id: str, title: str, pub_date: str, non_academic_authors: List[str],
                 company_affiliations: List[str], corresponding_email: Optional[str]):
        self.pubmed_id = pubmed_id
        self.title = title
        self.pub_date = pub_date
        self.non_academic_authors = non_academic_authors
        self.company_affiliations = company_affiliations
        self.corresponding_email = corresponding_email

    def to_dict(self) -> Dict[str, str]:
        return {
            "PubmedID": self.pubmed_id,
            "Title": self.title,
            "Publication Date": self.pub_date,
            "Non-academic Author(s)": "; ".join(self.non_academic_authors),
            "Company Affiliation(s)": "; ".join(self.company_affiliations),
            "Corresponding Author Email": self.corresponding_email or ""
        }

def fetch_pubmed_ids(query: str, max_results: int = 100, debug: bool = False) -> List[str]:
    """
    Fetch PubMed IDs for a given query using the ESearch API.
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    if debug:
        logging.info(f"Fetching PubMed IDs with query: {query}")
    resp = requests.get(PUBMED_ESEARCH_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data["esearchresult"]["idlist"]

def fetch_paper_details(pubmed_ids: List[str], debug: bool = False) -> List[etree._Element]:
    """
    Fetch paper details from PubMed using the EFetch API. Returns a list of XML elements.
    """
    if not pubmed_ids:
        return []
    ids_str = ",".join(pubmed_ids)
    params = {
        "db": "pubmed",
        "id": ids_str,
        "retmode": "xml"
    }
    if debug:
        logging.info(f"Fetching details for PubMed IDs: {ids_str}")
    resp = requests.get(PUBMED_EFETCH_URL, params=params)
    resp.raise_for_status()
    root = etree.fromstring(resp.content)
    return root.findall(".//PubmedArticle")

def parse_paper(article: etree._Element, debug: bool = False) -> Optional[Paper]:
    """
    Parse a PubMedArticle XML element and return a Paper object if it has at least one non-academic/company author.
    """
    try:
        pmid = article.findtext(".//PMID") or ""
        title = article.findtext(".//ArticleTitle") or ""
        pub_date_elem = article.find(".//PubDate")
        pub_date = ""
        if pub_date_elem is not None:
            year = pub_date_elem.findtext("Year")
            month = pub_date_elem.findtext("Month")
            day = pub_date_elem.findtext("Day")
            pub_date = "-".join(filter(None, [year, month, day]))
        authors = article.findall(".//Author")
        non_academic_authors = []
        company_affiliations = set()
        corresponding_email = None
        for author in authors:
            affiliations = [aff.text for aff in author.findall("AffiliationInfo/Affiliation") if aff.text]
            if not affiliations:
                continue
            # Check for non-academic affiliation
            for aff in affiliations:
                if is_non_academic_affiliation(aff):
                    lastname = author.findtext("LastName") or ""
                    firstname = author.findtext("ForeName") or ""
                    fullname = f"{firstname} {lastname}".strip()
                    non_academic_authors.append(fullname)
                    # Extract company names
                    for company in extract_company_names([aff]):
                        company_affiliations.add(company)
                # Try to extract email
                if not corresponding_email and "@" in aff:
                    # Simple heuristic: look for email in affiliation string
                    words = aff.split()
                    for word in words:
                        if "@" in word and "." in word:
                            corresponding_email = word.strip(';,.')
        if non_academic_authors and company_affiliations:
            return Paper(
                pubmed_id=pmid,
                title=title,
                pub_date=pub_date,
                non_academic_authors=non_academic_authors,
                company_affiliations=list(company_affiliations),
                corresponding_email=corresponding_email
            )
        return None
    except Exception as e:
        if debug:
            logging.error(f"Error parsing article: {e}")
        return None

def fetch_and_filter_papers(query: str, max_results: int = 100, debug: bool = False) -> List[Paper]:
    """
    Fetch and filter PubMed papers for a query, returning only those with at least one non-academic/company author.
    """
    pubmed_ids = fetch_pubmed_ids(query, max_results=max_results, debug=debug)
    articles = fetch_paper_details(pubmed_ids, debug=debug)
    papers = []
    for article in articles:
        paper = parse_paper(article, debug=debug)
        if paper:
            papers.append(paper)
    return papers
