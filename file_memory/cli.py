"""CLI commands for file-memory."""

import json
import sys
from pathlib import Path

import click

from file_memory import MemoryStore


@click.group()
@click.option(
    "--dir",
    "memory_dir",
    type=click.Path(path_type=Path),
    help="Custom memory directory",
)
@click.pass_context
def cli(ctx: click.Context, memory_dir: Path | None) -> None:
    """File memory for OpenCode - persistent storage for shared knowledge."""
    ctx.ensure_object(dict)
    ctx.obj["store"] = MemoryStore(base_dir=memory_dir)


@cli.command()
@click.argument("key")
@click.argument("value")
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["json", "markdown"]),
    default="json",
    help="Memory format",
)
@click.option(
    "--tags",
    help="Comma-separated tags",
)
@click.pass_context
def store(
    ctx: click.Context,
    key: str,
    value: str,
    fmt: str,
    tags: str | None,
) -> None:
    """Store a memory entry.

    KEY is the unique identifier.
    VALUE is the content (JSON string or markdown text).
    """
    store_obj: MemoryStore = ctx.obj["store"]

    if fmt == "json":
        try:
            content = json.loads(value)
        except json.JSONDecodeError as e:
            click.echo(f"Error: Invalid JSON: {e}", err=True)
            sys.exit(1)
    else:
        content = value

    tag_list = [t.strip() for t in tags.split(",")] if tags else []

    try:
        store_obj.store(key, content, format=fmt, tags=tag_list)
        click.echo(f"Stored: {key} ({fmt})")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("key")
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    help="Output as JSON",
)
@click.pass_context
def get(ctx: click.Context, key: str, json_output: bool) -> None:
    """Retrieve a memory entry by key."""
    store_obj: MemoryStore = ctx.obj["store"]

    try:
        entry = store_obj.get(key)
        if json_output:
            click.echo(json.dumps(entry.to_dict(), indent=2, default=str))
        else:
            click.echo(f"Key: {entry.metadata.key}")
            click.echo(f"Format: {entry.metadata.format}")
            click.echo(f"Created: {entry.metadata.created_at}")
            click.echo(f"Updated: {entry.metadata.updated_at}")
            if entry.metadata.tags:
                click.echo(f"Tags: {', '.join(entry.metadata.tags)}")
            click.echo("---")
            click.echo(entry.content)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--tag",
    help="Filter by tag",
)
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    help="Output as JSON",
)
@click.pass_context
def list_memories(
    ctx: click.Context,
    tag: str | None,
    json_output: bool,
) -> None:
    """List all memory entries."""
    store_obj: MemoryStore = ctx.obj["store"]

    entries = list(store_obj.list(tag=tag))

    if json_output:
        click.echo(json.dumps([e.to_dict() for e in entries], indent=2, default=str))
    else:
        if not entries:
            click.echo("No memories found.")
            return

        for entry in entries:
            tags_str = f" [{', '.join(entry.metadata.tags)}]" if entry.metadata.tags else ""
            click.echo(f"{entry.metadata.key} ({entry.metadata.format}){tags_str}")


@cli.command()
@click.argument("key")
@click.argument("value")
@click.option(
    "--tags",
    help="Comma-separated tags (keep existing if not provided)",
)
@click.pass_context
def update(ctx: click.Context, key: str, value: str, tags: str | None) -> None:
    """Update an existing memory entry."""
    store_obj: MemoryStore = ctx.obj["store"]

    try:
        existing = store_obj.get(key)
    except Exception:
        click.echo(f"Error: Memory '{key}' not found", err=True)
        sys.exit(1)

    if existing.metadata.format == "json":
        try:
            content = json.loads(value)
        except json.JSONDecodeError as e:
            click.echo(f"Error: Invalid JSON: {e}", err=True)
            sys.exit(1)
    else:
        content = value

    tag_list = [t.strip() for t in tags.split(",")] if tags else None

    try:
        store_obj.update(key, content, tags=tag_list)
        click.echo(f"Updated: {key}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("key")
@click.pass_context
def delete(ctx: click.Context, key: str) -> None:
    """Delete a memory entry."""
    store_obj: MemoryStore = ctx.obj["store"]

    try:
        store_obj.delete(key)
        click.echo(f"Deleted: {key}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("query")
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    help="Output as JSON",
)
@click.pass_context
def search(ctx: click.Context, query: str, json_output: bool) -> None:
    """Search memory entries by content."""
    store_obj: MemoryStore = ctx.obj["store"]

    results = list(store_obj.search(query))

    if json_output:
        click.echo(json.dumps([e.to_dict() for e in results], indent=2, default=str))
    else:
        if not results:
            click.echo(f"No results found for: {query}")
            return

        click.echo(f"Found {len(results)} result(s):\n")
        for entry in results:
            click.echo(f"Key: {entry.metadata.key}")
            click.echo(f"Content preview: {entry.content[:100]}...")
            click.echo("---")


@cli.command()
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    help="Output as JSON",
)
@click.pass_context
def list_tags(ctx: click.Context, json_output: bool) -> None:
    """List all unique tags."""
    store_obj: MemoryStore = ctx.obj["store"]

    tags = store_obj.tags()

    if json_output:
        click.echo(json.dumps(sorted(tags)))
    else:
        if not tags:
            click.echo("No tags found.")
        else:
            click.echo("Tags: " + ", ".join(sorted(tags)))


@cli.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize the memory directory."""
    store_obj: MemoryStore = ctx.obj["store"]
    click.echo(f"Memory directory: {store_obj.base_dir}")
    click.echo("Initialized successfully.")


def main() -> None:
    """Main entry point."""
    cli(obj={})


if __name__ == "__main__":
    main()
