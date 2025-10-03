
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

- Light – DOUT / DIMMER / LED / ZWAVE
- Switch – DOUT / ZWAVE
- Cover – ROLLER_SHUTTER / ZWAVE
- Climate – THERMOSTAT
- Sensor – ONE_WIRE / TEMPERATURE / ANALOG IN / MODBUS / ZWAVE / User Feature
- Binary Sensor 0/1 – DIN / BINARY_SENSOR / ZWAVE
- User Scripts

# Grenton object services

| HA device_type                     |  service               | parameters                                        |
|------------------------------------|------------------------|---------------------------------------------------|
| Binary Sensor 0/1                  |  set_state             | state [0 (off), 1 (on)]                           |
| Switch                             |  set_state             | state [0 (off), 1 (on)]                           |
| Light                              |  set_state             | state [0 (off), 1 (on)]                           |
| Light                              |  set_brightness        | brightness [0.00 (0%, off), 1.00 or 255 (100%)]   |
| Light                              |  set_rgb               | hex [#RRGGBB]                                     |
| Sensor                             |  set_value             | value [-999999999.99 to 999999999.99]             |
| Cover                              |  set_cover             | state [1-4], position [0-100%], lamel (optional, 0-90°) |