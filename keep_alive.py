"""
keep_alive.py

Opens a headless browser, visits the Streamlit app, and waits long enough
for Streamlit to register the visit and stay awake.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

URL = "https://vfhinterpreter.streamlit.app"

# How long to wait for the app to finish loading (ms).
# Streamlit can take 30-60 s to wake from sleep.
LOAD_TIMEOUT = 90_000

# How long to linger on the page after it loads (ms), so the visit registers.
LINGER_MS = 10_000


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Visiting {URL} …")
        page.goto(URL, timeout=LOAD_TIMEOUT)

        # Wait for Streamlit's main container to appear — this confirms the app
        # has fully booted rather than just served the loading screen.
        try:
            page.wait_for_selector(
                "[data-testid='stAppViewContainer']",
                timeout=LOAD_TIMEOUT,
            )
            print("App loaded successfully.")
        except PlaywrightTimeout:
            print("Timed out waiting for app — it may still be waking up.")

        # Linger so the activity is counted.
        page.wait_for_timeout(LINGER_MS)

        browser.close()
        print("Done.")


if __name__ == "__main__":
    main()
