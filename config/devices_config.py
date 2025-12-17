from typing import Any, Dict

from playwright.sync_api import Playwright

DEVICE_NAMES = {
    "desktop": "Desktop Chrome",
    "mobile": "iPhone 15 Pro Max",
    "tablet": "iPad Pro 11",
}

DEVICE_ALIASES = {
    "desktop": ["desktop", "pc", "laptop"],
    "mobile": ["mobile", "iphone", "phone", "smartphone"],
    "tablet": ["tablet", "ipad", "pad"],
}


def get_device_config(playwright: Playwright, device_name: str) -> Dict[str, Any]:
    device_name_lower = device_name.lower()

    for device_type, aliases in DEVICE_ALIASES.items():
        if device_name_lower in aliases:
            device_name = DEVICE_NAMES[device_type]
            break

    if device_name not in playwright.devices:
        available_devices = ", ".join(sorted(playwright.devices.keys()))

        raise ValueError(f"Device '{device_name}' not found. Available devices: {available_devices}")

    return playwright.devices[device_name]


def list_available_devices(playwright: Playwright) -> Dict[str, list]:
    devices = {
        "desktop": [],
        "mobile": [],
        "tablet": [],
        "other": [],
    }

    for device_name in playwright.devices.keys():
        device_lower = device_name.lower()

        if "desktop" in device_lower:
            devices["desktop"].append(device_name)

        elif "iphone" in device_lower or "pixel" in device_lower or "galaxy" in device_lower:
            devices["mobile"].append(device_name)

        elif "ipad" in device_lower:
            devices["tablet"].append(device_name)

        else:
            devices["other"].append(device_name)

    return devices
