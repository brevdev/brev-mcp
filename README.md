# Brev MCP server

This is a MCP server implementation for Brev.

## Configuration

The MCP server uses the Brev CLI's API access token and currently set org. 

Follow the [Brev documentation](https://www.brev.dev/docs/reference/brev-cli) to download the CLI and login if you haven't already.

If you want to switch your Brev org, run `brev set <org-name>`

The CLI access token expires every hour. If you have any 403 errors, simply run `brev ls` to refresh the access token.

## Quickstart

### Setup repository locally

`git clone git@github.com:brevdev/brev-mcp.git`

### Install uv

Follow the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

Add the following to your `claude_desktop_config.json`:

<details>
  <summary>Development/Unpublished Servers Configuration</summary>

  ```json
  "mcpServers": {
    "brev_mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "<path-to-repo>",
        "run",
        "brev-mcp"
      ]
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /Users/tmontfort/Brev/repos/brev_mcp run brev-mcp
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.