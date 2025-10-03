
<img src="https://github.com/user-attachments/assets/08571ca3-a9b2-404b-820f-dccc688f62e8" width="600"/>

# Grenton to Home Assistant


![image](https://github.com/user-attachments/assets/4cab82f8-548c-4b96-ae29-daaea8c5c11e)


A Home Assistant custom integration for presenting and controlling Grenton objects.

This integration creates objects in Home Assistant based on selected objects from Grenton. The HTTP Gate module is required, as well as the creation of a virtual HttpListener object and a script, according to the instructions. After providing the identifiers of Grenton objects, they will appear in Home Assistant. It is possible to display statuses and control Grenton devices.

If you like what I do, buy me a `coffee`!

<a href="https://tipply.pl/@jnalepka">
    <img src="https://img.shields.io/static/v1?label=Donate&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86" alt="Donate" width="130" height="30">
</a>


<br>Watch the video how to use this integration: https://www.youtube.com/watch?v=uhjFG1vz1Ro

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
-- ║ Script version: 1.0.0                                                 ║
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
        -- print("HA integration command >> " .. value)
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

# Supported Grenton objects

| Grenton Object                         | grenton_id (example)           | HA device_type           |    Other settings        |  HA functions         |
|----------------------------------------|--------------------------|--------------------------|-----------------------|-----------------------|
| DOUT / ZWAVE_DOUT (simple switch)      | CLU221000001->DOU1234    | Switch                   |                          | ON/OFF                |
| DOUT / ZWAVE_DOUT (light)              | CLU221000001->DOU1234    | Light                    |  grenton_type = DOUT     | ON/OFF    |
| DIMMER                                 | CLU221000001->DIM1234    | Light                    |  grenton_type = DIMMER   | ON/OFF, BRIGHTNESS    |
| DIMMER SINGLE ZWAVE_LED                | CLU221000001->ZWA1234    | Light                    |  grenton_type = DIMMER   | ON/OFF, BRIGHTNESS    |
| DIMMER RGBW_Red, RGBW_Green, RGBW_Blue, RGBW_White | CLU221000001->LED1234    | Light                    |  grenton_type = LED_R/G/B/W   | ON/OFF, BRIGHTNESS    |
| RGBW                                   | CLU221000001->LED1234    | Light                    |  grenton_type = RGB      | ON/OFF, BRIGHTNESS, RGB   |
| ROLLER_SHUTTER / ZWAVE_ROLLER_SHUTTER  | CLU221000001->ROL1234    | Cover                    |  if ReversePosition=Yes, check reversed     | UP/DOWN, POSITION, TILT POSITION     |
| THERMOSTAT                             | CLU221000001->THE1234    | Climate                  |                          | TEMPERATURE CONTROL   |
| DIN / ZWAVE_DIN / ZWAVE_BINARY_SENSOR  | CLU221000001->DIN1234    | Binary Sensor            |                          | BINARY SENSOR         |
| ONE_WIRE / TEMPERATURE_SENSOR /  PANELSENSTEMP   |  CLU221000001->ONE1234     | Sensor       |  grenton_type = DEFAULT_SENSOR, device_class=temperature  | SENSOR        |
| ANALOG IN                              | CLU221000001->ANA1234    | Sensor                   |  grenton_type = DEFAULT_SENSOR, device_class=?  | SENSOR        |
| GATE HTTP User feature (where the script is)    | My_feature   (Without GATE-> !!)      | Sensor |  grenton_type = DEFAULT_SENSOR, device_class=?  | SENSOR        |
| CLU User feature                       | CLU221000001->My_feature  | Sensor                  |  grenton_type = DEFAULT_SENSOR, device_class=?  | SENSOR        |
| MODBUS (Virtual object TYPE!)          | CLU501000001->MOD1234     | Sensor                  |   grenton_type = MODBUS, device_class=?  | SENSOR        |
| MODBUS_VALUE (Virtual object TYPE!)    | CLU501000001->MOD1234     | Sensor                  |  grenton_type = MODBUS_VALUE, device_class=?  | SENSOR        |
| MODBUS_RTU                             | CLU501000001->MOD1234     | Sensor                  |  grenton_type = MODBUS_RTU, device_class=?  | SENSOR        |
| MODBUS_CLIENT                          | CLU501000001->MOD1234     | Sensor                  |  grenton_type = MODBUS_CLIENT , device_class=?  | SENSOR        |
| MODBUS_SERVER                          | CLU501000001->MOD1234     | Sensor                  |  grenton_type = MODBUS_SERVER, device_class=?  | SENSOR        |
| MODBUS_SLAVE_RTU                       | CLU501000001->MOD1234     | Sensor                  |  grenton_type = MODBUS_SLAVE_RTU, device_class=?  | SENSOR        |
| GATE HTTP Script (integration clu)    | Script_name   (Without GATE-> !!)      | Script               |               | BUTTON        |
| OTHER CLU Script                      | CLU221000001->Script_name              | Script               |               | BUTTON        |

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

# Grenton object services

| HA device_type                     |  service               | parameters                                        |
|------------------------------------|------------------------|---------------------------------------------------|
| Binary Sensor 0/1                  |  set_state             | state [0 (off), 1 (on)]                           |
| Switch                             |  set_state             | state [0 (off), 1 (on)]                           |
| Light                              |  set_state             | state [0 (off), 1 (on)]                           |
| Light                              |  set_brightness        | brightness [0.00 (0%, off), 1.00 lub 255 (100%)]  |
| Light                              |  set_rgb               | hex [#RRGGBB]                                     |