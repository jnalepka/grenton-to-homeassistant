
![logo@2x](https://github.com/user-attachments/assets/08571ca3-a9b2-404b-820f-dccc688f62e8)

# Grenton to Home Assistant


![image](https://github.com/user-attachments/assets/4cab82f8-548c-4b96-ae29-daaea8c5c11e)


A Home Assistant custom integration for presenting and controlling Grenton objects.

This integration creates objects in Home Assistant based on selected objects from Grenton. The HTTP Gate module is required, as well as the creation of a virtual HttpListener object and a script, according to the instructions. After providing the identifiers of Grenton objects, they will appear in Home Assistant. It is possible to display statuses and control Grenton devices.

If you like what I do, buy me a `coffee`!

<a href="https://tipply.pl/@jnalepka">
    <img src="https://img.shields.io/static/v1?label=Donate&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86" alt="Donate" width="130" height="30">
</a>


# Installation

If you're using [HACS](https://hacs.xyz/), is to the easiest way is to install Grenton Objects through it.

To install manually, copy the grenton_objects folder along with all its contents into the custom_components folder of your Home Assistant setup. This folder is typically found within the /config directory.


# Requirement on the Grenton side

1. Create a `HTTPListener` virtual object on GateHTTP named `HA_Listener_Integration` and configure it as follows:
   * Path - `/HAlistener` (You can edit it if you want)
   * ResponseType - `JSON`

  ![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/1d69d9fc-95f3-4f89-90e3-588b8637ffad)

2. Create a script named `HA_Integration_Script` and attach it to the OnRequest event of the virtual object.

```lua
-- ╔═══════════════════════════════════════════════════════════════════════╗
-- ║                        Author: Jan Nalepka                            ║
-- ║                                                                       ║
-- ║ Script: HA_Integration_Script                                         ║
-- ║ Description: Display and control Grenton objects in Home Assistant.   ║
-- ║                                                                       ║
-- ║ License: MIT License                                                  ║
-- ║ Github: https://github.com/jnalepka/grenton-to-homeassistant          ║
-- ║                                                                       ║
-- ║ Version: 1.0.0                                                        ║
-- ║                                                                       ║
-- ║ Requirements:                                                         ║
-- ║    Gate Http:                                                         ║
-- ║          1.  Gate Http NAME: "GATE_HTTP" <or change it in this script>║
-- ║                                                                       ║
-- ║    HttpListener virtual object:                                       ║
-- ║          Name: HA_Listener_Integration                                ║
-- ║          Path: /HAlistener                                            ║
-- ║          ResponseType: JSON                                           ║
-- ║                                                                       ║
-- ╚═══════════════════════════════════════════════════════════════════════╝

local reqJson = GATE_HTTP->HA_Listener_Integration->RequestBody
local code = 400
local resp = { g_status = "Grenton script ERROR" }

if reqJson.command or reqJson.status then
    local results = {}

    for key, value in pairs(reqJson) do
        logDebug("HA integration command >> " .. value)
        results[key] = load(value)()
    end

    resp = { g_status = "OK" }
    for key, result in pairs(results) do
        resp[key] = result
    end

    code = 200
end

GATE_HTTP->HA_Listener_Integration->SetStatusCode(code)
GATE_HTTP->HA_Listener_Integration->SetResponseBody(resp)
GATE_HTTP->HA_Listener_Integration->SendResponse()
```

> NOTE! Pay attention to the name of the GATE and the Object.

![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/25a94dee-a43a-4b32-a3f2-83c455652688)


# Adding Grenton objects to Home Assistant

1. Open `Settings` -> `Devices & services` -> `+Add integration`.
2. Type and select "Grenton Objects".
3. Add your Grenton object.

# Supported objects

### Switch (On_Off)
* IO MODULE 8/8 DIN
* IO MODULE 2/2 FM
* RELAY X2 DIN
* RELAY X4 DIN
* RELAY Z-WAVE
* RELAY WI-FI

### Light (On_Off)
* IO MODULE 8/8 DIN
* IO MODULE 2/2 FM
* RELAY X2 DIN
* RELAY X4 DIN
* RELAY Z-WAVE
* RELAY WI-FI

### Light (Dimmer)
* DIMMER DIN
* DIMMER FM
* LED RGBW Z-WAVE (SINGLE ZWAVE_LED OBJECT)

### Light (RGB)
* LED RGBW DIN
* LED RGBW FM
* LED RGBW Z-WAVE

### Cover (Roller_Shutter)
* ROLLER SHUTTER DIN
* ROLLER SHUTTER X3 DIN
* ROLLER SHUTTER FM
* ROLLER SHUTTER Z-WAVE

### Climate (Thermostat)
* THERMOSTAT - Virtual Object

### Binary Sensor (Digital Value)
* Any Digital Value (e.g. DIN, ZWAVE_DIN)

### Sensor (Analog Value, e.g. OneWire / Temperature)
* ONE_WIRE
* TEMPERATURE_SENSOR (MULTISENSOR)
* PANELSENSTEMP (SMART PANEL / TOUCH PANEL)
* ANALOG IN/OUT DIN
* CLU User Feature
* MODBUS, MODBUS_VALUE, MODBUS_RTU, MODBUS_CLIENT, MODBUS_SERVER, MODBUS_SLAVE_RTU

#### Supported sensor device class:

- `device_class`, `unit_of_measurement`, `state_class` - More information https://developers.home-assistant.io/docs/core/entity/sensor

| device_class                            | unit_of_measurement         |
|----------------------------------------|--------------------------|
| `apparent_power`                       | VA                       |
| `atmospheric_pressure`                 | cbar, bar, hPa, mmHg, inHg, kPa, mbar, Pa, psi |
| `battery`                              | %                        |
| `carbon_dioxide`                       | ppm                      |
| `carbon_monoxide`                      | ppm                      |
| `current`                              | A, mA                    |
| `distance`                             | km, m, cm, mm, mi, yd, in |
| `duration`                             | d, h, min, s, ms         |
| `energy`                               | Wh, kWh, MWh, MJ, GJ     |
| `energy_storage`                       | Wh, kWh, MWh, MJ, GJ     |
| `frequency`                            | Hz, kHz, MHz, GHz        |
| `gas`                                  | m³, ft³, CCF             |
| `humidity`                             | %                        |
| `illuminance`                          | lx                       |
| `irradiance`                           | W/m², BTU/(h⋅ft²)        |
| `moisture`                             | %                        |
| `nitrogen_dioxide`                     | µg/m³                    |
| `nitrogen_monoxide`                    | µg/m³                    |
| `nitrous_oxide`                        | µg/m³                    |
| `ozone`                                | µg/m³                    |
| `ph`                                   | None                     |
| `pm1`                                  | µg/m³                    |
| `pm10`                                 | µg/m³                    |
| `pm25`                                 | µg/m³                    |
| `power`                                | W, kW                    |
| `power_factor`                         | %, None                  |
| `precipitation`                        | cm, in, mm               |
| `precipitation_intensity`              | in/d, in/h, mm/d, mm/h   |
| `pressure`                             | cbar, bar, hPa, mmHg, inHg, kPa, mbar, Pa, psi |
| `reactive_power`                       | var                      |
| `signal_strength`                      | dB, dBm                  |
| `sound_pressure`                       | dB, dBA                  |
| `speed`                                | ft/s, in/d, in/h, km/h, kn, m/s, mph, mm/d |
| `sulphur_dioxide`                      | µg/m³                    |
| `temperature`                          | °C, °F, K                |
| `timestamp`                            | None                     |
| `volatile_organic_compounds`           | µg/m³                    |
| `volatile_organic_compounds_parts`     | ppm, ppb                 |
| `voltage`                              | V, mV                    |
| `volume`                               | L, mL, gal, fl. oz., m³, ft³, CCF |
| `volume_flow_rate`                     | m³/h, ft³/min, L/min, gal/min |
| `volume_storage`                       | L, mL, gal, fl. oz., m³, ft³, CCF |
| `water`                                | L, gal, m³, ft³, CCF     |
| `weight`                               | kg, g, mg, µg, oz, lb, st |
| `wind_speed`                           | ft/s, km/h, kn, m/s, mph |



# Forced faster state update

By default, Home Assistant automatically refreshes entities every 30 seconds. If you want to accelerate the object update, go to the `Settings->Automations & Scenes` and set up the automation:

1. `Trigger` -> `Time and location` -> `Time pattern` -> e.g. `/10` (every 10 seconds)

![Przechwytywanie1](https://github.com/jnalepka/GrentonObjects_HomeAssistant/assets/70645322/305b7f35-63a8-4341-83e6-ac3a85006dfd)

2. `Action` -> `Other action` -> `Call service` -> `Home Assistant Core Integration: Update entity`
3. Select objects (`+Choose entity`) to be updated at specified intervals.

![Przechwytywanie2](https://github.com/jnalepka/GrentonObjects_HomeAssistant/assets/70645322/47d19f37-decb-4c7d-a5ed-c06bc66058a6)

4. Save and restart Home Assistant.


