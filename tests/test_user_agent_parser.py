import pytest
from sample_orders_code_assignment.transformations.user_agent_parser import (
    parse_user_agent,
)

# List of tuples containing a user agent string and the expected results
test_data = [
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        ("Computer", "Chrome", "115.0.0"),
    ),
    (
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        ("Mobile", "Chrome Mobile", "115.0.0"),
    ),
    (
        "Mozilla/5.0 (Linux; Android 13; SM-S918U Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36",
        ("Mobile", "Chrome Mobile WebView", "115.0.5790"),
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/115.0.5790.160 Mobile/15E148 Safari/604.1",
        ("Mobile", "Chrome Mobile iOS", "115.0.5790"),
    ),
    (
        "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.5735.131 Mobile DuckDuckGo/5 Safari/537.36",
        ("Mobile", "DuckDuckGo Mobile", "5"),
    ),
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        ("Computer", "Edge", "115.0.1901"),
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20G75 [FBAN/FBIOS;FBDV/iPhone13,3;FBMD/iPhone;FBSN/iOS;FBSV/16.6;FBSS/3;FBID/phone;FBLC/en_US;FBOP/5]",
        ("Mobile", "Facebook", ""),
    ),
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0",
        ("Computer", "Firefox", "116.0"),
    ),
    (
        "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/116.0 Firefox/116.0",
        ("Mobile", "Firefox Mobile", "116.0"),
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/35.0 Mobile/15E148 Safari/605.1.15",
        ("Mobile", "Firefox iOS", "35.0"),
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/278.0.557984068 Mobile/15E148 Safari/604.1",
        ("Mobile", "Google", "278.0.557984068"),
    ),
    (
        "Mozilla/5.0 (Linux; Android 12; moto g power (2022) Build/S3RQS32.20-42-10-9-6; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36 Instagram 297.0.0.33.109 Android (31/12; 332dpi; 720x1473; motorola; moto g power (2022); tonga; mt6765; en_US; 507536347)",
        ("Mobile", "Instagram", "297.0.0"),
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
        ("Mobile", "Mobile Safari", "16.1"),
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Shop App/2.121.0/iOS/16.6/WebView",
        ("Mobile", "Mobile Safari UI/WKWebView", ""),
    ),
    (
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 (Ecosia android@111.0.5563.116)",
        ("Mobile", "Phantom", "111.0.5563"),
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [Pinterest/iOS]",
        ("Mobile", "Pinterest", ""),
    ),
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
        ("Computer", "Safari", "16.3"),
    ),
    (
        "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G970U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.36",
        ("Mobile", "Samsung Internet", "22.0"),
    ),
    (
        None,
        ("Unknown", "Unknown", "Unknown"),
    ),
    (
        "''",
        ("Unknown", "Unknown", "Unknown"),
    ),
    (
        "",
        ("Unknown", "Unknown", "Unknown"),
    ),
]


@pytest.mark.parametrize("ua_string,expected", test_data)
def test_parse_user_agent(ua_string, expected):
    result = parse_user_agent(ua_string)
    assert result == expected
