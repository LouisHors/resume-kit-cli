import re


def strip_frontmatter(text):
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text
    return parts[2].lstrip()


def extract_headings(text):
    lines = text.splitlines()
    headings = []
    current = None
    body = []
    for line in lines:
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            if current is not None:
                current["body"] = "\n".join(body).strip()
                headings.append(current)
            current = {
                "level": len(match.group(1)),
                "title": match.group(2).strip(),
                "body": "",
            }
            body = []
        else:
            body.append(line)
    if current is not None:
        current["body"] = "\n".join(body).strip()
        headings.append(current)
    return headings
