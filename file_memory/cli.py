"""CLI commands for file-memory."""

import json
from pathlib import Path

import click

from file_memory import MemoryStore
from file_memory.store import (
    MemoryKeyError,
    MemoryStoreError,
)


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


def handle_error(e: Exception) -> None:
    """Print error and exit with appropriate code."""
    click.echo(f"Error: {e}", err=True)
    raise SystemExit(1)


@cli.command("list-memories")
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

    try:
        entries = list(store_obj.list(tag=tag))
    except MemoryStoreError as e:
        handle_error(e)

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
@click.argument("value", required=False)
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
@click.option(
    "--file",
    "file_path",
    type=click.Path(exists=True),
    help="Read content from file",
)
@click.pass_context
def store(
    ctx: click.Context,
    key: str,
    value: str | None,
    fmt: str,
    tags: str | None,
    file_path: Path | None,
) -> None:
    """Store a memory entry.

    KEY is the unique identifier.
    VALUE is the content (JSON string or markdown text).

    Use --file to read content from a file instead of argument.
    """
    store_obj: MemoryStore = ctx.obj["store"]

    if file_path:
        file_content = Path(file_path).read_text()
        if fmt == "json":
            try:
                content = json.loads(file_content)
            except json.JSONDecodeError as e:
                click.echo(f"Error: Invalid JSON in file: {e}", err=True)
                raise SystemExit(1)
        else:
            content = file_content
    elif value is not None:
        if fmt == "json":
            try:
                content = json.loads(value)
            except json.JSONDecodeError as e:
                click.echo(f"Error: Invalid JSON: {e}", err=True)
                raise SystemExit(1)
        else:
            content = value
    else:
        click.echo("Error: Either VALUE or --file must be provided", err=True)
        raise SystemExit(1)

    tag_list = [t.strip() for t in tags.split(",")] if tags else []

    try:
        store_obj.store(key, content, format=fmt, tags=tag_list)
    except (MemoryStoreError, MemoryKeyError) as e:
        handle_error(e)

    click.echo(f"Stored: {key} ({fmt})")


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
    except MemoryStoreError as e:
        handle_error(e)

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


@cli.command()
@click.argument("key")
@click.argument("value", required=False)
@click.option(
    "--tags",
    help="Comma-separated tags (keep existing if not provided)",
)
@click.option(
    "--file",
    "file_path",
    type=click.Path(exists=True),
    help="Read content from file",
)
@click.pass_context
def update(
    ctx: click.Context,
    key: str,
    value: str | None,
    tags: str | None,
    file_path: Path | None,
) -> None:
    """Update an existing memory entry."""
    store_obj: MemoryStore = ctx.obj["store"]

    try:
        existing = store_obj.get(key)
    except MemoryStoreError as e:
        handle_error(e)

    if file_path:
        file_content = Path(file_path).read_text()
        if existing.metadata.format == "json":
            try:
                content = json.loads(file_content)
            except json.JSONDecodeError as e:
                click.echo(f"Error: Invalid JSON in file: {e}", err=True)
                raise SystemExit(1)
        else:
            content = file_content
    elif value is not None:
        if existing.metadata.format == "json":
            try:
                content = json.loads(value)
            except json.JSONDecodeError as e:
                click.echo(f"Error: Invalid JSON: {e}", err=True)
                raise SystemExit(1)
        else:
            content = value
    else:
        click.echo("Error: Either VALUE or --file must be provided", err=True)
        raise SystemExit(1)

    tag_list = [t.strip() for t in tags.split(",")] if tags else None

    try:
        store_obj.update(key, content, tags=tag_list)
    except MemoryStoreError as e:
        handle_error(e)

    click.echo(f"Updated: {key}")


@cli.command()
@click.argument("key")
@click.pass_context
def delete(ctx: click.Context, key: str) -> None:
    """Delete a memory entry."""
    store_obj: MemoryStore = ctx.obj["store"]

    try:
        store_obj.delete(key)
    except MemoryStoreError as e:
        handle_error(e)

    click.echo(f"Deleted: {key}")


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

    try:
        results = list(store_obj.search(query))
    except MemoryStoreError as e:
        handle_error(e)

    if json_output:
        click.echo(json.dumps([e.to_dict() for e in results], indent=2, default=str))
    else:
        if not results:
            click.echo(f"No results found for: {query}")
            return

        click.echo(f"Found {len(results)} result(s):\n")
        for entry in results:
            preview = entry.content[:100].replace("\n", " ")
            click.echo(f"Key: {entry.metadata.key}")
            click.echo(f"Content preview: {preview}...")
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

    try:
        tags = store_obj.tags()
    except MemoryStoreError as e:
        handle_error(e)

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
