# Notifications

this is a notification service that listens to an Eventstream and sends notifications.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

Install the project dependencies, including test dependencies:

```bash
uv sync
```

Run the test suite:

```bash
uv run pytest
```

Todos:

- eventstream polling
