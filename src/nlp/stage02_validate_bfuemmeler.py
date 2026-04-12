"""
src/nlp/stage02_validate_bfuemmeler.py - Validate Stage

Source: Raw HTML string
Sink:   BeautifulSoup object (in memory)
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from bs4 import BeautifulSoup

# ============================================================
# Section 2. Define Run Validate Function
# ============================================================


def run_validate(
    html_content: str,
    LOG: logging.Logger,
) -> BeautifulSoup:
    """Inspect and validate HTML structure.

    Args:
        html_content (str): The raw HTML content from the Extract stage.
        LOG (logging.Logger): The logger instance.

    Returns:
        BeautifulSoup: The validated BeautifulSoup object.
    """
    LOG.info("========================")
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("========================")

    LOG.info("HTML STRUCTURE INSPECTION:")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Log the type of the top-level HTML structure
    LOG.info(f"Top-level type: {type(soup).__name__}")

    # Log the top-level elements in the HTML document
    top_level_elements = [element.name for element in soup.find_all(recursive=False)]
    LOG.info(f"Top-level elements: {top_level_elements}")

    # ============================================================
    # VALIDATE EXPECTATIONS
    # ============================================================

    # More flexible checks for a Gutenberg HTML page
    page_title = soup.find("title")
    headings = soup.find_all(["h1", "h2", "h3"])
    paragraphs = soup.find_all("p")
    images = soup.find_all("img")

    LOG.info("VALIDATE: <title> found: %s", page_title is not None)
    LOG.info("VALIDATE: headings found: %s", len(headings) > 0)
    LOG.info("VALIDATE: paragraphs found: %s", len(paragraphs) > 0)
    LOG.info("VALIDATE: images found: %s", len(images) > 0)

    missing = []

    # Require a page title
    if not page_title:
        missing.append("title")

    # Require readable page content
    if not headings and not paragraphs:
        missing.append("readable content (headings or paragraphs)")

    if missing:
        raise ValueError(
            f"VALIDATE: Required elements missing: {missing}. "
            "Page structure may have changed or selectors may not match this source."
        )

    LOG.info("VALIDATE: HTML structure is valid.")
    LOG.info("Sink: validated BeautifulSoup object")

    return soup
