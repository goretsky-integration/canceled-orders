import json
import pathlib
import tomllib
from dataclasses import dataclass
from zoneinfo import ZoneInfo

from enums import CountryCode

__all__ = ('get_config', 'Config')

CONFIG_FILE_PATH = pathlib.Path(__file__).parent.parent / 'config.toml'
GOOGLE_SHEETS_CREDENTIALS_FILE_PATH = CONFIG_FILE_PATH.parent / 'google_sheets_credentials.json'


def load_google_sheets_credentials() -> dict[str, str]:
    return json.loads(
        GOOGLE_SHEETS_CREDENTIALS_FILE_PATH.read_text(encoding='utf-8')
    )


@dataclass(frozen=True, slots=True)
class StorageConfig:
    base_url: str
    http_client_timeout: int


@dataclass(frozen=True, slots=True)
class DodoIsConfig:
    country_code: CountryCode
    http_client_timeout: int


@dataclass(frozen=True, slots=True)
class SentryConfig:
    is_enabled: bool
    dsn: str
    traces_sample_rate: float
    profiles_sample_rate: float


@dataclass(frozen=True, slots=True)
class Config:
    app_name: str
    timezone: ZoneInfo
    message_queue_url: str
    sentry: SentryConfig
    auth_credentials_storage: StorageConfig
    units_storage: StorageConfig
    dodo_is: DodoIsConfig
    spreadsheet_id: str


def get_config() -> Config:
    config_text = CONFIG_FILE_PATH.read_text(encoding='utf-8')
    config = tomllib.loads(config_text)

    app_name = config['app']['name']
    timezone = ZoneInfo(config['app']['timezone'])
    message_queue_url = config['message_queue']['url']

    auth_credentials_storage = config['auth_credentials_storage']

    units_storage = config['units_storage']

    sentry_config = config['sentry']
    sentry = SentryConfig(
        is_enabled=sentry_config['is_enabled'],
        dsn=sentry_config['dsn'],
        traces_sample_rate=sentry_config['traces_sample_rate'],
        profiles_sample_rate=sentry_config['profiles_sample_rate'],
    )

    return Config(
        app_name=app_name,
        timezone=timezone,
        message_queue_url=message_queue_url,
        sentry=sentry,
        auth_credentials_storage=StorageConfig(
            base_url=auth_credentials_storage['base_url'],
            http_client_timeout=auth_credentials_storage[
                'http_client_timeout'],
        ),
        units_storage=StorageConfig(
            base_url=units_storage['base_url'],
            http_client_timeout=units_storage['http_client_timeout'],
        ),
        dodo_is=DodoIsConfig(
            country_code=CountryCode(config['dodo_is']['country_code']),
            http_client_timeout=config['dodo_is']['http_client_timeout'],
        ),
        spreadsheet_id=config['google_sheets']['spreadsheet_id']
    )
