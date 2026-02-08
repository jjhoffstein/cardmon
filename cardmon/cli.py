import asyncio, os, logging
import typer
from rich.console import Console
from rich.table import Table
from .models import Card
from .monitor import CardMonitor
from .repository import CardRepository

app = typer.Typer(help="Credit card benefits monitoring")
console = Console()

@app.command()
def add(name: str, url: str, issuer: str, selector: str|None = None, tcs_url: str|None = None, db: str = "cardmon.db"):
    repo = CardRepository(db)
    repo.add_card(Card(name=name, url=url, issuer=issuer, selector=selector, tcs_url=tcs_url))
    console.print(f"[green]Added {name}[/green]")

@app.command()
def ls(issuer: str|None = None, db: str = "cardmon.db"):
    repo = CardRepository(db)
    cards = repo.get_cards(issuer)
    if not cards: console.print("[yellow]No cards found[/yellow]"); return
    table = Table(title="Cards")
    for col in ["Name", "Issuer", "URL"]: table.add_column(col)
    for c in cards: table.add_row(c.name, c.issuer, c.url[:50] + "...")
    console.print(table)

@app.command()
def check(name: str|None = None, issuer: str|None = None, db: str = "cardmon.db", webhook: str|None = None, slack: bool = True):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    mon = CardMonitor(db, api_key)
    if name: results = [asyncio.run(mon.check_card(name))]
    else: results = asyncio.run(mon.check_all(issuer))
    for r in results:
        status = "[red]ERROR[/red]" if r.error else ("[yellow]CHANGED[/yellow]" if r.changed else "[green]OK[/green]")
        fee = r.schumer.annual_fee if r.schumer else "?"
        console.print(f"{r.name}: {status} (fee: {fee})")
    if webhook and any(r.changed for r in results): asyncio.run(mon.notify(results, webhook, slack))

@app.command()
def queue(db: str = "cardmon.db"):
    repo = CardRepository(db)
    items = repo.queue_list()
    if not items: console.print("[green]Queue empty[/green]"); return
    table = Table(title="Review Queue")
    for col in ["ID", "Name", "Timestamp"]: table.add_column(col)
    for i in items: table.add_row(str(i["id"]), i["name"], i["ts"])
    console.print(table)

@app.command()
def approve(id: int, db: str = "cardmon.db"):
    repo = CardRepository(db)
    repo.queue_approve(id)
    console.print(f"[green]Approved {id}[/green]")

if __name__ == "__main__": app()
