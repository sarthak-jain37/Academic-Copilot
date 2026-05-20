import re
import pymupdf



def clean_text(text):
    text = re.sub(r"\.{5,}", " ", text)
    text = re.sub(r"Page\s+\d+\s+of\s+\d+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def parse_document(document):
    source = document.split("/")[-1].replace(".pdf", "")
    full_text = None

    print(f"\nProcessing {source}...")

    try:
        with pymupdf.open(document) as doc:
            all_pages = []

            for page_num, page in enumerate(doc, start=1):
                try:
                    all_pages.append(page.get_text())
                except Exception as e:
                    raise Exception(f"Reading failed at page {page_num}: {e}")

        full_text = "\n".join(all_pages)
        full_text = clean_text(full_text)

        print(f"{source} successfully read")

    except Exception as e:
        print(f"{source}: {e}")

    return source, full_text