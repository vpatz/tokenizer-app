#!/usr/bin/env python3
"""Tokenize text with Hugging Face tokenizers 0.23.1."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import tokenizers
from tokenizers import Tokenizer


def load_text(text: str | None, path: str | None) -> str:
    if text is not None and path is not None:
        raise SystemExit("Pass text or --file, not both.")
    if path is not None:
        return Path(path).read_text(encoding="utf-8")
    if text is not None:
        return text
    if sys.stdin.isatty():
        raise SystemExit("Pass text, --file, or pipe text on stdin.")
    return sys.stdin.read()


def short_error(exc: Exception) -> str:
    return str(exc).strip().splitlines()[0] or exc.__class__.__name__


def get_tokenizer(model: str, tokenizer_file: str | None) -> tuple[Tokenizer, str]:
    if tokenizer_file is not None:
        try:
            return Tokenizer.from_file(tokenizer_file), tokenizer_file
        except Exception as exc:
            raise SystemExit(
                f"Could not load tokenizer file {tokenizer_file!r}: {short_error(exc)}"
            ) from None
    try:
        return Tokenizer.from_pretrained(model), model
    except Exception as exc:
        raise SystemExit(
            f"Could not load pretrained tokenizer {model!r}: {short_error(exc)}"
        ) from None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Tokenize text with Hugging Face tokenizers 0.23.1."
    )
    parser.add_argument("text", nargs="?", help="Text to tokenize.")
    parser.add_argument("-f", "--file", help="Read text from this file.")
    parser.add_argument(
        "-m",
        "--model",
        default="bert-base-uncased",
        help="Pretrained tokenizer id (default: bert-base-uncased).",
    )
    parser.add_argument(
        "-t",
        "--tokenizer",
        help="Path to a tokenizer.json file. Overrides --model.",
    )
    parser.add_argument(
        "--ids-only",
        action="store_true",
        help="Print only the token ids, one per line.",
    )
    parser.add_argument(
        "--no-special-tokens",
        action="store_true",
        help="Do not add special tokens such as [CLS] and [SEP].",
    )
    args = parser.parse_args(argv)

    text = load_text(args.text, args.file)
    tokenizer, label = get_tokenizer(args.model, args.tokenizer)
    encoding = tokenizer.encode(text, add_special_tokens=not args.no_special_tokens)

    if args.ids_only:
        for token_id in encoding.ids:
            print(token_id)
        return 0

    print(f"package: tokenizers {tokenizers.__version__}")
    print(f"tokenizer: {label}")
    print(f"vocab: {tokenizer.get_vocab_size()}")
    print(f"characters: {len(text)}")
    print(f"tokens: {len(encoding.ids)}")
    print()
    for index, (token_id, token) in enumerate(zip(encoding.ids, encoding.tokens)):
        shown = token.replace("\n", "\\n")
        print(f"{index:4d}  {token_id:<8d}  {shown!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
