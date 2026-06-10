from errors import CSSTagSelectorError

PLATINUM_POINTS_TEST_ID = "platinumPoints"


def find_items(soup):
    """Find MyNintendo reward product cards on the page."""
    items = []
    seen_labels = set()

    for anchor in soup.find_all("a", attrs={"aria-label": True}):
        label = anchor.get("aria-label", "").strip()
        if not label or label in seen_labels:
            continue
        if anchor.find(attrs={"data-testid": PLATINUM_POINTS_TEST_ID}):
            items.append(anchor)
            seen_labels.add(label)

    if not items:
        raise CSSTagSelectorError("Reward product items not found on page.")

    return items
