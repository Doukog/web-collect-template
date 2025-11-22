from dataclasses import dataclass


@dataclass
class Patchright:
    chrome_path: str
    cdp_url: str
    headless: bool
    port: int
    page_timeout: int
    node_timeout: int
