"""Helper functions for history page tests with mocked API responses"""
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import allure
from playwright.sync_api import Route

from config.auth_config import BASE_URL

HISTORY_API_ENDPOINT = "/api-v1/history"
MOCK_DATA_PATH = Path(__file__).parent / "history_mock_data.json"


@allure.step("Load mock history data from JSON file")
def load_mock_data():
    with open(MOCK_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@allure.step("Generate mock history API response")
def generate_history_response(count: int, offset: int, limit: int, total_count: int, all_results: list):
    next_url = None
    if offset + limit < total_count:
        next_offset = offset + limit
        next_url = f"{BASE_URL.rstrip('/')}{HISTORY_API_ENDPOINT}?limit={limit}&offset={next_offset}"

    previous_url = None
    if offset > 0:
        prev_offset = max(0, offset - limit)
        if prev_offset == 0:
            previous_url = f"{BASE_URL.rstrip('/')}{HISTORY_API_ENDPOINT}?limit={limit}"
        else:
            previous_url = f"{BASE_URL.rstrip('/')}{HISTORY_API_ENDPOINT}?limit={limit}&offset={prev_offset}"

    results = all_results[offset:offset + count]

    return {
        "count": total_count,
        "next": next_url,
        "previous": previous_url,
        "results": results
    }


@allure.step("Handle history API route with pagination")
def handle_history_route(route: Route, mock_data: dict, limit: int = 30):
    url = route.request.url

    if HISTORY_API_ENDPOINT not in url:
        route.fallback()
        return

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    offset = 0
    request_limit = limit

    if "offset" in query_params:
        try:
            offset = int(query_params["offset"][0])
        except (ValueError, IndexError):
            offset = 0

    if "limit" in query_params:
        try:
            request_limit = int(query_params["limit"][0])
        except (ValueError, IndexError):
            request_limit = limit

    total_count = mock_data["count"]
    all_results = mock_data["results"]

    items_on_page = min(request_limit, total_count - offset)
    if items_on_page <= 0:
        items_on_page = 0

    response_data = generate_history_response(
        count=items_on_page,
        offset=offset,
        limit=request_limit,
        total_count=total_count,
        all_results=all_results
    )

    route.fulfill(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response_data)
    )
