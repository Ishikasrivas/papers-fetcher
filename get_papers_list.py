import click
from papers_fetcher import fetch
import pandas as pd
import sys

@click.command()
@click.argument('query', type=str)
@click.option('-d', '--debug', is_flag=True, help='Enable debug output.')
@click.option('-f', '--file', type=click.Path(), help='Output CSV file name. If not provided, prints to console.')
def main(query: str, debug: bool, file: str):
    """
    Fetch PubMed papers for a QUERY and output those with at least one non-academic (company) author.
    """
    if debug:
        import logging
        logging.basicConfig(level=logging.INFO)
        click.echo("Debug mode enabled.")
    click.echo(f"Fetching papers for query: {query}")
    papers = fetch.fetch_and_filter_papers(query, debug=debug)
    if not papers:
        click.echo("No papers found matching criteria.")
        sys.exit(0)
    df = pd.DataFrame([p.to_dict() for p in papers])
    if file:
        df.to_csv(file, index=False)
        click.echo(f"Results saved to {file}")
    else:
        click.echo(df.to_csv(index=False))

if __name__ == "__main__":
    main()
