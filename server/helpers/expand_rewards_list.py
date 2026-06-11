import logging
import re
import time

EXPAND_BUTTON_PATTERN = re.compile(r"see all|load more", re.I)
BUTTON_POLL_TIMEOUT_MS = 5000
EXPANSION_VERIFY_TIMEOUT_MS = 10000
MAX_CLICK_ATTEMPTS = 3

COUNT_PRODUCTS_JS = """() => {
    const anchors = document.querySelectorAll('a[aria-label]');
    const seen = new Set();
    let count = 0;
    for (const anchor of anchors) {
        const label = (anchor.getAttribute('aria-label') || '').trim();
        if (!label || seen.has(label)) continue;
        if (anchor.querySelector('[data-testid="platinumPoints"]')) {
            seen.add(label);
            count++;
        }
    }
    return count;
}"""


def count_products_on_page(page):
    """Count reward product cards using the same markers as find_items()."""
    return page.evaluate(COUNT_PRODUCTS_JS)


def find_expand_button(page):
    try:
        button = page.get_by_role("button", name=EXPAND_BUTTON_PATTERN).first
        if button.is_visible(timeout=0):
            return button
    except Exception:
        pass
    return None


def poll_for_expand_button(page, timeout_ms=BUTTON_POLL_TIMEOUT_MS):
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        button = find_expand_button(page)
        if button:
            return button
        time.sleep(0.25)
    return None


def wait_for_expansion(page, count_before, timeout_ms=EXPANSION_VERIFY_TIMEOUT_MS):
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        count_after = count_products_on_page(page)
        button = find_expand_button(page)
        if count_after > count_before:
            return count_after, True
        if button is None:
            return count_after, True
        time.sleep(0.25)
    return count_products_on_page(page), False


def expand_rewards_list(page, product_ready_selector):
    """Click See all / Load more and verify the product list expanded."""
    count_before = count_products_on_page(page)
    button = poll_for_expand_button(page)

    if button is None:
        logging.info(
            "No expansion button found. Product count: %s",
            count_before,
        )
        return {
            "expanded": True,
            "count_before": count_before,
            "count_after": count_before,
        }

    expanded = False
    count_after = count_before

    for attempt in range(MAX_CLICK_ATTEMPTS):
        button = find_expand_button(page)
        if button is None:
            count_after = count_products_on_page(page)
            expanded = True
            break

        button.scroll_into_view_if_needed()
        button.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_selector(product_ready_selector, timeout=10000)

        count_after, expanded = wait_for_expansion(page, count_before)
        if expanded:
            break
        logging.warning(
            "Expansion click attempt %s/%s did not increase product count",
            attempt + 1,
            MAX_CLICK_ATTEMPTS,
        )

    logging.info(
        "Expansion result: expanded=%s, count_before=%s, count_after=%s",
        expanded,
        count_before,
        count_after,
    )
    return {
        "expanded": expanded,
        "count_before": count_before,
        "count_after": count_after,
    }
