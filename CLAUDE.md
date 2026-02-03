# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FastMCPを使用したQRコード生成MCPサーバー。PNG、SVG、Base64エンコード画像、ASCIIアートなど、複数の出力形式に対応したQRコード生成ツールを提供します。

## Development Environment

- Python 3.13+
- Package manager: `uv`
- Main dependencies:
  - `fastmcp>=0.3.0` - MCP server framework
  - `qrcode[pil]>=8.2` - QR code generation with PIL support

## Common Commands

### Setup and Running

```bash
# Install dependencies
uv sync

# Run the MCP server
uv run main.py

# Test with MCP Inspector
npx @modelcontextprotocol/inspector uv run main.py
```

### Testing

```bash
# Run tests (when implemented)
uv run pytest

# Run specific test file
uv run pytest tests/test_<name>.py -v
```

## Architecture

### MCP Server Structure (main.py)

FastMCPを使用した単一ファイル構成：

- **Server initialization**: `mcp = FastMCP("qr-mcp-server")`
- **Tool registration**: `@mcp.tool()` decorator for each QR generation function
- **Entry point**: `mcp.run()` starts the server

### Available Tools

5つのQR生成ツールを提供：

1. **generate_qr_png**: PNG画像としてファイルに保存
2. **generate_qr_svg**: SVG画像としてファイルに保存
3. **generate_qr_base64_png**: Base64エンコードされたPNG文字列を返す
4. **generate_qr_base64_svg**: Base64エンコードされたSVG文字列を返す
5. **generate_qr_ascii**: ASCIIアートとして文字列を返す

### Key Implementation Details

**File Operations**:
- `pathlib.Path` を使用してファイルパスを扱う
- `overwrite` パラメータで既存ファイルの上書きを制御
- 既存ファイルがあり `overwrite=False` の場合は `ValueError` を発生

**QR Code Generation**:
```python
qr = qrcode.QRCode(
    version=1,              # Auto-fit enabled with qr.make(fit=True)
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=size,          # PNG only
    border=border,
)
qr.add_data(data)
qr.make(fit=True)
```

**Output Formats**:
- PNG: `qr.make_image(fill_color="black", back_color="white")`
- SVG: `qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)`
- Base64: PIL image → `io.BytesIO()` → `base64.b64encode()`
- ASCII: `qr.get_matrix()` で行列を取得し、手動で `"██"` と `"  "` に変換

## Code Conventions

- Type hints for all function parameters and return values
- Docstrings in Japanese (Google style)
- Error handling: Raise `ValueError` with Japanese error messages
- File operations: Use `pathlib.Path` instead of `os.path`

## Adding New Features

When adding new QR generation options:

1. Add parameters to existing tools (e.g., error correction level, colors)
2. Ensure backward compatibility with default parameter values
3. Update docstrings with new parameter descriptions
4. Update README.md with new usage examples

## Testing Strategy

When implementing tests:

- Test each tool independently
- Cover edge cases: empty string, very long data, invalid paths
- Test file operations: overwrite behavior, permission errors
- Validate output formats: PNG/SVG validity, Base64 encoding correctness
- Test ASCII output rendering
