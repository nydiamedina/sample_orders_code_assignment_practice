import pytest
from transformations.user_agent_parser import parse_user_agent

# List of tuples containing a user agent string and the expected results
test_data = [
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        {
            "device_type": "Computer",
            "browser_type": "Chrome",
            "browser_version": "115.0.0",
        },
    ),
    (
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        {
            "device_type": "Mobile",
            "browser_type": "Chrome Mobile",
            "browser_version": "115.0.0",
        },
    ),
    (
        "Mozilla/5.0 (Linux; Android 13; SM-S918U Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36",
        {
            "device_type": "Mobile",
            "browser_type": "Chrome Mobile Webview",
            "browser_version": "115.0.5790",
        },
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/115.0.5790.160 Mobile/15E148 Safari/604.1",
        {
            "device_type": "Mobile",
            "browser_type": "Chrome Mobile iOS",
            "browser_version": "115.0.5790",
        },
    ),
    (
        "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.5735.131 Mobile DuckDuckGo/5 Safari/537.36",
        {
            "device_type": "Mobile",
            "browser_type": "DuckDuckGo Mobile",
            "browser_version": "5",
        },
    ),
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        {
            "device_type": "Computer",
            "browser_type": "Edge",
            "browser_version": "115.0.1901",
        },
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20G75 [FBAN/FBIOS;FBDV/iPhone13,3;FBMD/iPhone;FBSN/iOS;FBSV/16.6;FBSS/3;FBID/phone;FBLC/en_US;FBOP/5]",
        {
            "device_type": "Mobile",
            "browser_type": "Facebook",
            "browser_version": "",
        },
    ),
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0",
        {
            "device_type": "Computer",
            "browser_type": "Firefox",
            "browser_version": "116.0",
        },
    ),
    (
        "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/116.0 Firefox/116.0",
        {
            "device_type": "Mobile",
            "browser_type": "Firefox Mobile",
            "browser_version": "116.0",
        },
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/35.0  Mobile/15E148 Safari/605.1.15",
        {
            "device_type": "Mobile",
            "browser_type": "Firefox iOS",
            "browser_version": "35.0",
        },
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/278.0.557984068 Mobile/15E148 Safari/604.1",
        {
            "device_type": "Mobile",
            "browser_type": "Google",
            "browser_version": "278.0.557984068",
        },
    ),
    (
        "Mozilla/5.0 (Linux; Android 12; moto g power (2022) Build/S3RQS32.20-42-10-9-6; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36 Instagram 297.0.0.33.109 Android (31/12; 332dpi; 720x1473; motorola; moto g power (2022); tonga; mt6765; en_US; 507536347)",
        {
            "device_type": "Mobile",
            "browser_type": "Instagram",
            "browser_version": "297.0.0",
        },
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
        {
            "device_type": "Mobile",
            "browser_type": "Mobile Safari",
            "browser_version": "16.1",
        },
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Shop App/2.121.0/iOS/16.6/WebView",
        {
            "device_type": "Mobile",
            "browser_type": "Mobile Safari UI/WKWebView",
            "browser_version": "",
        },
    ),
    (
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36 (Ecosia android@111.0.5563.116)",
        {
            "device_type": "Mobile",
            "browser_type": "Phantom",
            "browser_version": "111.0.5563",
        },
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [Pinterest/iOS]",
        {
            "device_type": "Mobile",
            "browser_type": "Pinterest",
            "browser_version": "",
        },
    ),
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
        {
            "device_type": "Computer",
            "browser_type": "Safari",
            "browser_version": "16.3",
        },
    ),
    (
        "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G970U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/111.0.5563.116 Mobile Safari/537.36",
        {
            "device_type": "Mobile",
            "browser_type": "Samsung Internet",
            "browser_version": "22.0",
        },
    ),
    (
        "",
        {
            "device_type": "Unknown",
            "browser_type": "Unknown",
            "browser_version": "Unknown",
        },
    ),
]


@pytest.mark.parametrize("ua_string,expected", test_data)
def test_parse_user_agent(ua_string, expected):
    result = parse_user_agent(ua_string)
    assert result == expected
