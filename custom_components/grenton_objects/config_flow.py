import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

DEVICE_TYPES = {
    "light": "Light",
    "switch": "Switch",
    "cover": "Cover",
    "climate": "Climate",
    "sensor": "Sensor",
    "binary_sensor": "Binary sensor"
}

class GrentonConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Grenton integration."""

    VERSION = 1
    def __init__(self):
        self._devices = []

    async def async_step_user(self, user_input=None):
        """First step - choose device type."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("device_type"): vol.In(DEVICE_TYPES)
                })
            )

        self.device_type = user_input["device_type"]
        return await self.async_step_device_config()

    async def async_step_device_config(self, user_input=None):
        """Step to configure each device."""
        if user_input is None:
            return self.async_show_form(
                step_id="device_config",
                data_schema=self._get_device_schema()
            )

        self._devices.append({
            "device_type": self.device_type,
            "api_endpoint": user_input["api_endpoint"],
            "grenton_id": user_input["grenton_id"],
            "name": user_input["name"],
            "additional_params": user_input.get("additional_params", None)
        })

        return self.async_show_form(
            step_id="add_another",
            data_schema=vol.Schema({
                vol.Required("add_another", default=False): bool
            })
        )

    async def async_step_add_another(self, user_input=None):
        """Ask if the user wants to add another device."""
        if user_input["add_another"]:
            return await self.async_step_user()
        else:
            return self.async_create_entry(title="Grenton Objects", data={
                "devices": self._devices
            })

    def _get_device_schema(self):
        """Return a schema based on the selected device type."""
        if self.device_type == "light":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id"): str,
                vol.Required("grenton_type", default="UNKNOWN"): vol.In(["DOUT","DIMMER", "RGB"]),
            })
        elif self.device_type == "switch":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id"): str,
            })
        elif self.device_type == "cover":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id"): str,
                vol.Optional("reversed", default=False): bool,
            })
        elif self.device_type == "climate":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id"): str,
            })
        elif self.device_type == "sensor":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id"): str,
                vol.Optional("grenton_type", default="UNKNOWN"): vol.In(["MODBUS_RTU", "MODBUS_VALUE", "MODBUS", "MODBUS_CLIENT", "MODBUS_SLAVE_RTU"]),
                vol.Optional("device_class", default="temperature"): vol.In([
                    "app_usage",
                    "aqi",
                    "apparent_power",
                    "atmospheric_pressure",
                    "battery",
                    "carbon_dioxide",
                    "carbon_monoxide",
                    "current",
                    "data_rate",
                    "data_size",
                    "date",
                    "distance",
                    "duration",
                    "energy",
                    "energy_storage",
                    "enum",
                    "frequency",
                    "gas",
                    "humidity",
                    "illuminance",
                    "irradiance",
                    "moisture",
                    "monetary",
                    "nitrogen_dioxide",
                    "nitrogen_monoxide",
                    "nitrous_oxide",
                    "ozone",
                    "ph",
                    "pm1",
                    "pm10",
                    "pm25",
                    "power",
                    "power_factor",
                    "precipitation",
                    "precipitation_intensity",
                    "pressure",
                    "reactive_power",
                    "signal_strength",
                    "sound_pressure",
                    "speed",
                    "sulphur_dioxide",
                    "temperature",
                    "timestamp",
                    "volatile_organic_compounds",
                    "volatile_organic_compounds_parts",
                    "voltage",
                    "volume",
                    "volume_flow_rate",
                    "volume_storage",
                    "water",
                    "weight",
                    "wind_speed"
                ]),
                vol.Optional("unit_of_measurement"): vol.In([
                    "apps", "VA", "cbar", "bar", "hPa", "mmHg", "inHg", "kPa", "mbar", "Pa", "psi", "%",
                    "ppm", "A", "mA", "bit/s", "kbit/s", "Mbit/s", "Gbit/s", "B/s", "kB/s", "MB/s",
                    "GB/s", "KiB/s", "MiB/s", "GiB/s", "bit", "kbit", "Mbit", "Gbit", "B", "kB",
                    "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "KiB", "MiB", "GiB", "TiB", "km", "m",
                    "cm", "mm", "mi", "yd", "in", "d", "h", "min", "s", "ms", "Wh", "kWh", "MWh",
                    "MJ", "GJ", "Hz", "kHz", "MHz", "GHz", "m³", "ft³", "CCF", "lx", "W/m²",
                    "BTU/(h⋅ft²)", "µg/m³", "kW", "W", "cm", "in", "mm", "in/d", "in/h", "mm/d",
                    "mm/h", "var", "dB", "dBm", "dBA", "ft/s", "km/h", "kn", "m/s", "mph", "°C",
                    "°F", "K", "ppb", "ppb", "V", "mV", "L", "mL", "gal", "fl. oz.", "m³", "ft³",
                    "kg", "g", "mg", "µg", "oz", "lb", "st"
                ])
                vol.Optional("state_class"): vol.In(["total", "total_increasing", "measurement"]),
            })
        elif self.device_type == "binary_sensor":
            return vol.Schema({
                vol.Required("name"): str,
                vol.Required("api_endpoint", default="http://192.168.0.4/HAlistener"): str,
                vol.Required("grenton_id"): str
            })
