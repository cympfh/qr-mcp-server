#!/usr/bin/env python3
"""QR Code Generator MCP Server

FastMCPを使用したQRコード生成サーバー
"""

import base64
import io
import json
from pathlib import Path

import qrcode
import qrcode.image.svg
from fastmcp import FastMCP

# MCPサーバーの初期化
mcp = FastMCP("qr-mcp-server")


@mcp.tool()
def generate_qr_png(
    data: str,
    output_path: str,
    overwrite: bool = False,
    size: int = 10,
    border: int = 4,
) -> str:
    """QRコードをPNG画像として生成し、ファイルに保存します

    Args:
        data: QRコードに埋め込むデータ（テキスト、URL等）
        output_path: 保存先のファイルパス
        overwrite: 既存ファイルを上書きするか（デフォルト: False）
        size: QRコードのボックスサイズ（デフォルト: 10）
        border: QRコードの余白サイズ（デフォルト: 4）

    Returns:
        JSON形式の結果（success, format, output_path, message）
    """
    output_file = Path(output_path)

    # 既存ファイルのチェック
    if output_file.exists() and not overwrite:
        raise ValueError(
            f"ファイル '{output_path}' は既に存在します。上書きする場合は overwrite=True を指定してください。"
        )

    # QRコードの生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # PNG画像として保存
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(str(output_file))

    return json.dumps({
        "success": True,
        "format": "png",
        "output_path": str(output_path),
        "message": "QR code saved as PNG",
    }, ensure_ascii=False)


@mcp.tool()
def generate_qr_svg(
    data: str,
    output_path: str,
    overwrite: bool = False,
    border: int = 4,
) -> str:
    """QRコードをSVG画像として生成し、ファイルに保存します

    Args:
        data: QRコードに埋め込むデータ（テキスト、URL等）
        output_path: 保存先のファイルパス
        overwrite: 既存ファイルを上書きするか（デフォルト: False）
        border: QRコードの余白サイズ（デフォルト: 4）

    Returns:
        JSON形式の結果（success, format, output_path, message）
    """
    output_file = Path(output_path)

    # 既存ファイルのチェック
    if output_file.exists() and not overwrite:
        raise ValueError(
            f"ファイル '{output_path}' は既に存在します。上書きする場合は overwrite=True を指定してください。"
        )

    # QRコードの生成（SVG形式）
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # SVG画像として保存
    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    img.save(str(output_file))

    return json.dumps({
        "success": True,
        "format": "svg",
        "output_path": str(output_path),
        "message": "QR code saved as SVG",
    }, ensure_ascii=False)


@mcp.tool()
def generate_qr_base64_png(
    data: str,
    size: int = 10,
    border: int = 4,
) -> str:
    """QRコードをPNG画像として生成し、base64エンコードした文字列を返します

    Args:
        data: QRコードに埋め込むデータ（テキスト、URL等）
        size: QRコードのボックスサイズ（デフォルト: 10）
        border: QRコードの余白サイズ（デフォルト: 4）

    Returns:
        JSON形式の結果（success, format, encoding, data）
    """
    # QRコードの生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # PNG画像をメモリ上に生成
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # base64エンコード
    encoded = base64.b64encode(buffer.read()).decode("utf-8")

    return json.dumps({
        "success": True,
        "format": "png",
        "encoding": "base64",
        "data": encoded,
        "message": "QR code generated as PNG base64",
    }, ensure_ascii=False)


@mcp.tool()
def generate_qr_base64_svg(
    data: str,
    border: int = 4,
) -> str:
    """QRコードをSVG画像として生成し、base64エンコードした文字列を返します

    Args:
        data: QRコードに埋め込むデータ（テキスト、URL等）
        border: QRコードの余白サイズ（デフォルト: 4）

    Returns:
        JSON形式の結果（success, format, encoding, data）
    """
    # QRコードの生成（SVG形式）
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # SVG画像をメモリ上に生成
    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    buffer = io.BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # base64エンコード
    encoded = base64.b64encode(buffer.read()).decode("utf-8")

    return json.dumps({
        "success": True,
        "format": "svg",
        "encoding": "base64",
        "data": encoded,
        "message": "QR code generated as SVG base64",
    }, ensure_ascii=False)


@mcp.tool()
def generate_qr_ascii(
    data: str,
    border: int = 2,
) -> str:
    """QRコードをASCIIアートとして生成します

    この形式はコンソールやターミナル上で直接表示できるため、
    ファイル保存が不要な場合や即座に確認したい場合に最適です。

    Args:
        data: QRコードに埋め込むデータ（テキスト、URL等）
        border: QRコードの余白サイズ（デフォルト: 2）

    Returns:
        JSON形式の結果（success, format, data）
    """
    # QRコードの生成
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    ascii_data = f.read()

    return json.dumps({
        "success": True,
        "format": "ascii",
        "data": ascii_data,
        "message": "QR code generated as ASCII art",
    }, ensure_ascii=False)


def main():
    """サーバーを起動"""
    mcp.run()


if __name__ == "__main__":
    main()
