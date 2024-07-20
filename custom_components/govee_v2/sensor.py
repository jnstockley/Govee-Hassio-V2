import logging

from homeassistant.const import CONF_DEVICE_ID, CONF_API_KEY, CONF_NAME, UnitOfTemperature, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType, ConfigType
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
    PLATFORM_SCHEMA
)

from custom_components.govee_v2.devices.H5179 import H5179, H5179_Device

log = logging.getLogger()

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICE_ID): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_NAME): cv.string,
})


async def async_setup_platform(hass: HomeAssistant, config: ConfigType, async_add_entities: AddEntitiesCallback,
                   discovery_info: DiscoveryInfoType | None = None) -> None:
    device_id = config[CONF_DEVICE_ID]
    sku = config[CONF_NAME]
    api_key = config[CONF_API_KEY]

    device = await H5179(api_key=api_key, sku=sku, device=device_id).update()

    async_add_entities([GoveeTemperature(device_id, sku, api_key, device), GoveeHumidity(device_id, sku, api_key, device)])


class GoveeTemperature(SensorEntity):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
    _attr_native_value = -999
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 2
    _attr_unique_id = f"{CONF_DEVICE_ID}-temp"
    _attr_name = "Temperature"

    def __init__(self, device_id: str, sku: str, api_key: str, device: H5179_Device) -> None:
        log.info(f"Setting up temperature: {device_id} - {sku} - {api_key}")
        self.device_id = device_id
        self.sku = sku
        self.api_key = api_key
        self._attr_native_value = device.temperature

    async def async_update(self) -> None:
        log.info(f"Updating temperature for device {self.device_id} - {self.sku}")
        device = await H5179(api_key=self.api_key, sku=self.sku, device=self.device_id).update()
        log.info(f"Device: {device}")
        self._attr_native_value = device.temperature


class GoveeHumidity(SensorEntity):
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_native_value = -1
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 1
    _attr_unique_id = f"{CONF_DEVICE_ID}-humidity"
    _attr_name = "Humidity"

    def __init__(self, device_id: str, sku: str, api_key: str, device: H5179_Device) -> None:
        log.info(f"Setting up humidity: {device_id} - {sku} - {api_key}")
        self.device_id = device_id
        self.sku = sku
        self.api_key = api_key
        self._attr_native_value = device.temperature

    async def async_update(self) -> None:
        log.info(f"Updating humidity for device {self.device_id} - {self.sku}")
        device = await H5179(api_key=self.api_key, sku=self.sku, device=self.device_id).update()
        log.info(f"Device: {device}")
        self._attr_native_value = device.humidity
