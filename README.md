# SauceDemo Checkout Automation

This project contains a Playwright + pytest end-to-end test for the standard SauceDemo purchase flow using the `standard_user` account.

## What the test covers

The automation verifies the happy path:

- open the SauceDemo login page
- sign in with the provided credentials
- add `Sauce Labs Backpack` to the cart
- open the cart and continue to checkout
- complete the checkout form with dummy data
- finish the purchase
- assert the confirmation message: `Thank you for your order!`

## Project files

- `test_saucedemo.py` — the runnable Playwright test
- `requirements.txt` — Python dependencies
- `README.md` — project setup and execution guide

## Requirements

- Python 3.10 or newer
- a working browser environment for Playwright

## Setup

From this project folder, run:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run the test

```bash
pytest -q test_saucedemo.py
```

To run it in headed mode so the browser window is visible:

```bash
pytest --headed -q test_saucedemo.py
```

## Optional environment overrides

The test uses the defaults below:

- `SAUCEDEMO_URL=https://saucedemo.com`
- `SAUCEDEMO_USERNAME=standard_user`
- `SAUCEDEMO_PASSWORD=secret_sauce`

You can override them if needed:

```bash
SAUCEDEMO_URL=https://saucedemo.com \
SAUCEDEMO_USERNAME=standard_user \
SAUCEDEMO_PASSWORD=secret_sauce \
pytest -q test_saucedemo.py
```
