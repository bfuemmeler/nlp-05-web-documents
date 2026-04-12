import logging

from bs4 import BeautifulSoup
import pandas as pd


def run_transform(
    soup: BeautifulSoup,
    LOG: logging.Logger,
) -> pd.DataFrame:

    LOG.info("========================")
    LOG.info("STAGE 03: TRANSFORM starting...")
    LOG.info("========================")

    # ============================================================
    # Extract title
    # ============================================================

    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "unknown"

    LOG.info(f"Extracted title: {title}")

    # ============================================================
    # Extract paragraphs (MAIN DATASET)
    # ============================================================

    paragraph_tags = soup.find_all("p")

    records = []

    for i, p in enumerate(paragraph_tags):
        text = p.get_text(strip=True)

        # Skip empty or tiny lines
        if len(text) < 20:
            continue

        records.append(
            {
                "paragraph_id": i,
                "text": text,
                "word_count": len(text.split()),
                "char_count": len(text),
                "title": title,
            }
        )

    LOG.info(f"Extracted {len(records)} usable paragraphs")

    # ============================================================
    # Convert to DataFrame
    # ============================================================

    df = pd.DataFrame(records)

    LOG.info(f"Created DataFrame with {len(df)} rows")
    LOG.info(f"Columns: {list(df.columns)}")

    LOG.info("Sample:")
    LOG.info(f"\n{df.head()}")

    return df
