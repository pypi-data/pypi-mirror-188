from pydantic import BaseModel


class UserProxyConfig(BaseModel):
    proxy_soft: str
    proxy_type: str | None = None
    proxy_host: str | None = None
    proxy_port: str | None = None
    proxy_user: str | None = None
    proxy_password: str | None = None
    proxy_url: str | None = None


class FingepringConfig(BaseModel):
    automatic_timezone: int = 1
    timezone: str | None = None
    webrtc: str | None = None
    location: str | None = None
    location_switch: int = 1
    longitude: str | None = None
    latitude: str | None = None
    accuracy: int = 1000
    language: list[str] = ["en-US", "en"]
    language_switch: str | None = None
    ua: str | None = None
    screen_resolution: str = 'none'
    fonts: str | None = None
    canvas: int = 1
    webgl_image: int | None = 1
    webgl: int = 3
    webgl_config: dict = {"unmasked_vendor": "", "unmasked_renderer": ""}
    audio: int = 1
    do_not_track: str = 'default'
    hardware_concurrency: int = 4
    device_memory: int = 8
    flash: str = 'block'
    scan_port_type: int = 1
    allow_scan_ports: list | None = None
    media_devices: int = 1
    client_rects: int = 1
    device_name_switch: int = 1
    device_name: str | None = None
    random_ua: dict | None = None
    speech_switch: int = 1
    mac_address_config: dict = {"model": "1", "address": ""}
    browser_kernel_config: dict = {"version": "latest", "type": "chrome"}
    gpu: int = 0
