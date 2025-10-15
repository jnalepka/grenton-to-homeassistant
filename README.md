
<img src="https://github.com/user-attachments/assets/08571ca3-a9b2-404b-820f-dccc688f62e8" width="600"/>

# Grenton to Home Assistant (custom integration)

A Home Assistant custom integration for presenting and controlling Grenton objects.

This integration creates objects in Home Assistant based on selected objects from Grenton. The HTTP Gate module is required, as well as the creation of a virtual HttpListener object and a script, according to the instructions. After providing the identifiers of Grenton objects, they will appear in Home Assistant. It is possible to display statuses and control Grenton devices.

![image](https://github.com/user-attachments/assets/4cab82f8-548c-4b96-ae29-daaea8c5c11e)


<a href="https://tipply.pl/@jnalepka">
    <img src="https://img.shields.io/static/v1?label=Donate&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86" alt="Donate" width="130" height="30">
</a>

If you like what I do, buy me a `coffee`!

# License

This project is free for personal and non-commercial use.  
Commercial use requires the author's prior written permission.  
The full license text can be found in the [LICENSE](LICENSE) file.

**Note:** Starting from version 3.0.0, this license applies.  

# Installation

## Using HASC (recommended)

The best way to install is by using the Home Assistant Community Store (HACS). [Downloading HACS](https://www.hacs.xyz/docs/use/download/download/).
After installing HACS, search for and install Grenton Objects.

Youtube tutorial: [HACS and Grenton Objects Installation](https://www.youtube.com/watch?v=LEcBMFAkLcY&t=2s)

## Manual installation (not recommended)

To install manually, copy the grenton_objects folder along with all its contents into the custom_components folder of your Home Assistant setup. This folder is typically found within the /config directory.

# Requirements on the Grenton side

1. Create a `HTTPListener` virtual object on GateHTTP named `HA_Listener_Integration` and configure it as follows:
   * Path - `/HAlistener` (You can edit it if you want)
   * ResponseType - `JSON`

  ![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/1d69d9fc-95f3-4f89-90e3-588b8637ffad)

2. Create a script named `HA_Integration_Script`.

```lua
-- ╔═══════════════════════════════════════════════════════════════════════╗
-- ║                        Author: Jan Nalepka                            ║
-- ║                                                                       ║
-- ║ Script: HA_Integration_Script                                         ║
-- ║ Description: Display and control Grenton objects in Home Assistant.   ║
-- ║                                                                       ║
-- ║ License: Free for non-commercial use                                  ║
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

> NOTE! Pay attention to the name of the GATE and the virtual object.

3. Attach `HA_Integration_Script` script to the `OnRequest` event of the `HA_Listener_Integration` virtual object.

![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/25a94dee-a43a-4b32-a3f2-83c455652688)

# How to add an object

1. Open `Settings` -> `Devices & services` -> `+Add integration`.
2. Type and select "Grenton Objects".
3. Add your Grenton object.

### Supported Grenton objects

- Light – DOUT / DIMMER / LED / ZWAVE
- Switch – DOUT / ZWAVE
- Cover – ROLLER_SHUTTER / ZWAVE
- Climate – THERMOSTAT
- Sensor – ONE_WIRE / TEMPERATURE / ANALOG IN / MODBUS / ZWAVE / User Feature / Other
- Binary Sensor 0/1 – DIN / BINARY_SENSOR / ZWAVE
- User Scripts

# Auto updates

The add-on automatically retrieves the status of objects from Grenton. This works well for a small number of objects (around 15) and when immediate state updates are not required.
You can also go to `Settings -> Devices & Services -> Grenton Objects` and, by clicking the settings icon for a specific object, configure its data refresh interval.

> NOTE! After changing the object settings, a Home Assistant restart is required.

For a larger number of objects or when dynamic state updates are needed, dynamic updates should be configured.

# Dynamic updates

To configure dynamic updates, go to `Settings -> Devices & Services -> Grenton Objects`, and for each object you want to enable dynamic updates for, disable automatic updates.

> NOTE! After changing an object's settings, a Home Assistant restart is required.

## Create long-lived access tokens

To use the Home Assistant REST API, you need to create an access token. To do this, go to `Profile → Security → Long-Lived Access Tokens`, create a token, and then copy it.

<img width="603" height="295" alt="image" src="https://github.com/user-attachments/assets/36c3a1c8-783d-4bc6-b8cb-6ffcf7e15014" />


## Grenton-side requirement for calling Grenton services

1. Create a `HTTPRequest` virtual object on GateHTTP named `HA_Request_Grenton_Set` and configure it as follows:
   * Host - `http://192.168.0.95:8123` (Enter the IP address of your Home Assistant.)
   * Path - `\z`
   * Method = `POST`
   * RequestType = `JSON`
   * ResponseType = `JSON`
   * RequestHeaders = `Authorization: Bearer <your token>` (paste your long-lived access token)

2. Create a script named `HA_Integration_Grenton_Set` and attach it to the OnRequest event of the virtual object.

```lua
-- ╔═══════════════════════════════════════════════════════════════════════╗
-- ║                        Author: Jan Nalepka                            ║
-- ║                                                                       ║
-- ║ Script: HA_Integration_Grenton_Set                                    ║
-- ║ Description: Send a service command for an entity in Home Assistant.  ║
-- ║                                                                       ║
-- ║ License: Free for non-commercial use                                  ║
-- ║ Github: https://github.com/jnalepka/grenton-to-homeassistant          ║
-- ║                                                                       ║
-- ║ Version: 1.0.0                                                        ║
-- ║                                                                       ║
-- ║ Requirements:                                                         ║
-- ║    Gate Http:                                                         ║
-- ║          1.  Gate Http NAME: "GATE_HTTP" <or change it in this script>║
-- ║                                                                       ║
-- ║    Script parameters:                                                 ║
-- ║          1.  ha_entity, default: "-", string                          ║
-- ║          2.  grenton_service, default: "-", string                    ║
-- ║          3.  value_1, default: "-1", number                           ║
-- ║          4.  value_2, default: "-1", number                           ║
-- ║          5.  value_3, default: "-1", number                           ║
-- ║          6.  string_value, default: "-", string                       ║
-- ║                                                                       ║
-- ║    Http_Request virtual object:                                       ║
-- ║          Name: HA_Integration_Grenton_Set                             ║
-- ║          Host: http://192.168.0.114:8123  (example)                   ║
-- ║          Path: \z                                                     ║
-- ║          Method: "POST"                                               ║
-- ║          RequestType: JSON                                            ║
-- ║          ResponseType: JSON                                           ║
-- ║          RequestHeaders: Authorization: Bearer <your HA token>        ║
-- ║                                                                       ║
-- ╚═══════════════════════════════════════════════════════════════════════╝

local path = "/api/services/grenton_objects/"..grenton_service
local reqJson = { entity_id = ha_entity }
  
if grenton_service == "set_state" then
    reqJson.state = value_1
elseif grenton_service == "set_brightness" then
    reqJson.brightness = value_1
elseif grenton_service == "set_rgb" then
    reqJson.hex = string_value
elseif grenton_service == "set_value" then
    reqJson.value = value_1
elseif grenton_service == "set_cover" then
    reqJson.state = value_1
    reqJson.position = value_2
    if value_3 ~= "-1" then
        reqJson.lamel = value_3
    end
elseif grenton_service == "set_therm_state" then
    reqJson.state = value_1
    if value_2 ~= "-1" then
        reqJson.direction = value_2
    end
elseif grenton_service == "set_therm_target_temp" or grenton_service == "set_therm_current_temp" then
    reqJson.temp = value_1
end

GATE_HTTP->HA_Request_Grenton_Set->SetPath(path)
GATE_HTTP->HA_Request_Grenton_Set->SetRequestBody(reqJson)
GATE_HTTP->HA_Request_Grenton_Set->SendRequest()
```

> NOTE! Pay attention to the name of the GATE and the virtual object.

3. Create parameters for the script HA_Integration_Grenton_Set:
   * ha_entity, default: "-", string
   * grenton_service, default: "-", string
   * value_1, default: "-1", number
   * value_2, default: "-1", number
   * value_3, default: "-1", number
   * string_value, default: "-", string
  
<img width="602" height="508" alt="image" src="https://github.com/user-attachments/assets/edea5dd3-ff18-459c-be0e-74143d0b4d51" />


## All Grenton services

| HA device_type                     |  grenton service       | parameters                                        |
|------------------------------------|------------------------|---------------------------------------------------|
| Binary Sensor 0/1                  |  set_state             | state [0 (off), 1 (on)]                           |
| Switch                             |  set_state             | state [0 (off), 1 (on)]                           |
| Light                              |  set_state             | state [0 (off), 1 (on)]                           |
| Light                              |  set_brightness        | brightness [0.00 (0%, off), 1.00 or 255 (100%)]   |
| Light                              |  set_rgb               | hex [#RRGGBB]                                     |
| Sensor                             |  set_value             | value [-999999999.99 to 999999999.99]             |
| Cover                              |  set_cover             | state [0-4], position [0-100%], lamel (optional) [0-90°] |
| Climate                            |  set_therm_state       | state [0 (off), 1 (on)], direction (optional) [0 (normal/heat), 1 (reverse/cool)] |
| Climate                            |  set_therm_target_temp | temp (target temp)                                |
| Climate                            |  set_therm_current_temp | temp (current temp)                              |

## Example of a dynamic update

### DOUT - Light / Switch / Binary Sensor

<img width="836" height="643" alt="image" src="https://github.com/user-attachments/assets/fe39f7eb-879f-4b25-a8a2-3b27c3ac64a7" />

<img width="1099" height="557" alt="image" src="https://github.com/user-attachments/assets/fa76d811-c09a-4adc-9144-f29944605235" />

### DIMMER - Light

<img width="836" height="643" alt="image" src="https://github.com/user-attachments/assets/9bf141b2-36f1-48b2-ab67-077526f4a2ef" />

<img width="1099" height="557" alt="image" src="https://github.com/user-attachments/assets/ae260a69-7708-433d-bd3b-e028da617c40" />

### LED - Light

<img width="836" height="643" alt="image" src="https://github.com/user-attachments/assets/e7813732-cf0d-49ad-9f3b-6c3c5b2a230d" />

<img width="1099" height="559" alt="image" src="https://github.com/user-attachments/assets/b459e424-0a77-477f-bad1-05c6556fdef4" />

### ONE_WIRE / TEMPERATURE / ANALOG IN / Other - Sensor

<img width="836" height="643" alt="image" src="https://github.com/user-attachments/assets/1e7ea14f-7d9b-481f-b1e1-ede387fde552" />

<img width="1099" height="559" alt="image" src="https://github.com/user-attachments/assets/446f88af-9e21-4961-afb3-4122cd3597cd" />


<img width="1099" height="899" alt="image" src="https://github.com/user-attachments/assets/ba213fe7-ee07-4ee8-bf46-2de10025ffeb" />

### ROLLER_SHUTTER (without lamel) - Cover

<img width="836" height="697" alt="image" src="https://github.com/user-attachments/assets/53d11780-b770-461e-8e42-03ee41e8bcba" />

<img width="1099" height="557" alt="image" src="https://github.com/user-attachments/assets/8124101c-54b9-4728-8d63-349842134f89" />


### THERMOSTAT - Climate

<img width="836" height="643" alt="image" src="https://github.com/user-attachments/assets/87c94098-7eed-4ecc-879b-7c4d991f4bc8" />

<img width="836" height="664" alt="image" src="https://github.com/user-attachments/assets/489b1814-4d31-484e-92ea-71f944289fa9" />

<img width="836" height="643" alt="image" src="https://github.com/user-attachments/assets/dd1293f6-0405-4d31-986a-f1da153ffc3d" />

<img width="1059" height="563" alt="image" src="https://github.com/user-attachments/assets/e11022ea-9e23-4e40-899e-0fab24ed40b6" />

<img width="836" height="643" alt="image" src="https://github.com/user-attachments/assets/d9792c72-9bfe-427f-8ca2-92f45365a8af" />

<img width="1059" height="563" alt="image" src="https://github.com/user-attachments/assets/23ee434c-d681-405f-82b8-df73fd008368" />

