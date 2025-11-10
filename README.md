
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

<img src="https://user-images.githubusercontent.com/47686437/168548113-b3cd4206-3281-445b-b7c6-bc0a3251293d.png" height="20"> Youtube tutorial: [HACS and Grenton Objects Installation](https://youtu.be/LEcBMFAkLcY)

## Manual installation (not recommended)

To install manually, copy the grenton_objects folder along with all its contents into the custom_components folder of your Home Assistant setup. This folder is typically found within the /config directory.

# Requirements on the Grenton side

<img src="https://user-images.githubusercontent.com/47686437/168548113-b3cd4206-3281-445b-b7c6-bc0a3251293d.png" height="20"> Youtube tutorial: [Configure Grenton side and add first object](https://youtu.be/QOVhQc0x1ro)

1. Create a `HTTPListener` virtual object on the `GATE_HTTP` named `HA_Integration_Listener` and configure it as follows:
   * Path - `/HAlistener` (You can edit it if you want)
   * ResponseType - `JSON`

  <img width="836" height="643" alt="image" src="https://github.com/user-attachments/assets/32aef72d-bd06-4ec9-8861-20c48c50b06f" />


2. Create a script on the `GATE_HTTP` named `HA_Integration_Script`.

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
-- ║          Name: HA_Integration_Listener                                ║
-- ║          Path: /HAlistener                                            ║
-- ║          ResponseType: JSON                                           ║
-- ║                                                                       ║
-- ╚═══════════════════════════════════════════════════════════════════════╝

local reqJson = GATE_HTTP->HA_Integration_Listener->RequestBody
local code = 400
local resp = { g_status = "Grenton script ERROR" }

if reqJson.command or reqJson.status then
    local results = {}

    for key, value in pairs(reqJson) do
        results[key] = load(value)()
    end

    resp = { g_status = "OK" }
    for key, result in pairs(results) do
        resp[key] = result
    end

    code = 200
end

GATE_HTTP->HA_Integration_Listener->SetStatusCode(code)
GATE_HTTP->HA_Integration_Listener->SetResponseBody(resp)
GATE_HTTP->HA_Integration_Listener->SendResponse()
```

> NOTE! Pay attention to the name of the GATE and the virtual object.

3. Attach `HA_Integration_Script` script to the `OnRequest` event of the `HA_Integration_Listener` virtual object.

![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/25a94dee-a43a-4b32-a3f2-83c455652688)

# How to add an object

<img src="https://user-images.githubusercontent.com/47686437/168548113-b3cd4206-3281-445b-b7c6-bc0a3251293d.png" height="20"> Youtube tutorial: [Configure Grenton side and add first object](https://youtu.be/QOVhQc0x1ro)

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

<img src="https://user-images.githubusercontent.com/47686437/168548113-b3cd4206-3281-445b-b7c6-bc0a3251293d.png" height="20"> Youtube tutorial: [Dynamic update - Lamp (DOUT)](https://youtu.be/3-AoxTPbSp0)

To configure dynamic updates, go to `Settings -> Devices & Services -> Grenton Objects`, and for each object you want to enable dynamic updates for, disable automatic updates.

## Create long-lived access tokens

To use the Home Assistant REST API, you need to create an access token. To do this, go to `Profile → Security → Long-Lived Access Tokens`, create a token, and then copy it.

<img width="603" height="295" alt="image" src="https://github.com/user-attachments/assets/36c3a1c8-783d-4bc6-b8cb-6ffcf7e15014" />


## Grenton-side requirement for calling Grenton services

1. Create a two `user features` on the `GATE_HTTP`:
   * `queueHA`, type `OTHER`, init value `0`
   * `queueHArunning`, type `BOOLEAN`, init value `false`
  
<img width="864" height="643" alt="image" src="https://github.com/user-attachments/assets/ce621b2d-55ec-46b7-9fee-b05939b2bd30" />
  
2. Create a `HTTPRequest` virtual object on the `GATE_HTTP` named `HA_Request_Grenton_Set` and configure it as follows:
   * Host - `http://192.168.0.95:8123` (Enter the IP address of your Home Assistant.)
   * Path - `\z`
   * Method = `POST`
   * RequestType = `JSON`
   * ResponseType = `JSON`
   * RequestHeaders = `Authorization: Bearer <your token>` (paste your long-lived access token)

2. Create a script on the `GATE_HTTP` named `HA_Integration_Queue_Prepare`.

```lua
-- ╔═══════════════════════════════════════════════════════════════════════╗
-- ║                        Author: Jan Nalepka                            ║
-- ║                                                                       ║
-- ║ Script: HA_Integration_Queue_Prepare                                  ║
-- ║ Description: Prepare queue for the grenton service request to the HA. ║
-- ║                                                                       ║
-- ║ License: Free for non-commercial use                                  ║
-- ║ Github: https://github.com/jnalepka/grenton-to-homeassistant          ║
-- ║                                                                       ║
-- ║ Version: 1.0.0                                                        ║
-- ║                                                                       ║
-- ║ Requirements:                                                         ║
-- ║    Gate Http:                                                         ║
-- ║          1.  Gate Http NAME: "GATE_HTTP" <or change it in this script>║
-- ║          2.  HA_Integration_Queue_Prepare     script added            ║
-- ║                                                                       ║
-- ║    Script parameters:                                                 ║
-- ║          1.  ha_entity, default: "-", string                          ║
-- ║          2.  grenton_service, default: "-", string                    ║
-- ║          3.  value_1, default: "-1", number                           ║
-- ║          4.  value_2, default: "-1", number                           ║
-- ║          5.  value_3, default: "-1", number                           ║
-- ║          6.  string_value, default: "-", string                       ║
-- ║                                                                       ║
-- ╚═══════════════════════════════════════════════════════════════════════╝

if type(queueHA) ~= "table" then queueHA = {} end
local req = { e = ha_entity, s = grenton_service }
local builders = {
    set_state = function(r) r.v1 = value_1 end,
    set_brightness = function(r) r.v1 = value_1 end,
    set_rgb = function(r) r.v4 = string_value end,
    set_value = function(r) r.v1 = value_1 end,
    set_cover = function(r)
        r.v1 = value_1
        r.v2 = value_2
        if value_3 ~= "-1" then r.v3 = value_3 end
    end
}
local builder = builders[grenton_service]
if builder then builder(req) end
table.insert(queueHA, req)
if not GATE_HTTP->queueHArunning then
    GATE_HTTP->HA_Integration_Process_Queue()
end
```

> NOTE! Pay attention to the name of the `GATE_HTTP` and the virtual object.

3. Create a `parameters` for the script `HA_Integration_Queue_Prepare`:
   * ha_entity, default: "-", string
   * grenton_service, default: "-", string
   * value_1, default: "-1", number
   * value_2, default: "-1", number
   * value_3, default: "-1", number
   * string_value, default: "-", string
  
<img width="556" height="485" alt="image" src="https://github.com/user-attachments/assets/2861dd8a-c1d1-4048-8d9d-ac645b19cd66" />

4. Create a script on the `GATE_HTTP` named `HA_Integration_Process_Queue`.

```lua
-- ╔═══════════════════════════════════════════════════════════════════════╗
-- ║                        Author: Jan Nalepka                            ║
-- ║                                                                       ║
-- ║ Script: HA_Integration_Process_Queue                                  ║
-- ║ Description: Send grenton service request to the HA.                  ║
-- ║                                                                       ║
-- ║ License: Free for non-commercial use                                  ║
-- ║ Github: https://github.com/jnalepka/grenton-to-homeassistant          ║
-- ║                                                                       ║
-- ║ Version: 1.0.0                                                        ║
-- ║                                                                       ║
-- ║ Requirements:                                                         ║
-- ║    Gate Http:                                                         ║
-- ║          1.  Gate Http NAME: "GATE_HTTP" <or change it in this script>║
-- ║          2.  HA_Integration_Process_Queue_Timer: CountDown, 50ms      ║
-- ║                 |- OnTimer: this script                               ║
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

GATE_HTTP->queueHArunning = true
if GATE_HTTP->HA_Request_Grenton_Set->IsActive == 1 then
	GATE_HTTP->HA_Integration_Process_Queue_Timer->Start()
    return
end
local nextReq = table.remove(queueHA, 1)
if not nextReq then
	GATE_HTTP->queueHArunning = false
    return
end
local path = "/api/services/grenton_objects/"..nextReq.s
local reqJson = { entity_id = nextReq.e }
local handlers = {
    set_state = function(r, n) r.state = n.v1 end,
    set_brightness = function(r, n) r.brightness = n.v1 end,
    set_rgb = function(r, n) r.hex = n.v4 end,
    set_value = function(r, n) r.value = n.v1 end,
    set_cover = function(r, n)
        r.state = n.v1
        r.position = n.v2
        if n.v3 ~= "-1" then r.lamel = n.v3 end
    end
}
local handler = handlers[nextReq.s]
if handler then handler(reqJson, nextReq) end
GATE_HTTP->HA_Request_Grenton_Set->SetPath(path)
GATE_HTTP->HA_Request_Grenton_Set->SetRequestBody(reqJson)
GATE_HTTP->HA_Request_Grenton_Set->SendRequest()
GATE_HTTP->HA_Integration_Process_Queue_Timer->Start()
```

> NOTE! Pay attention to the name of the `GATE_HTTP` and the virtual object.

5. Create a `Timer` virtual object on the `GATE_HTTP` named `HA_Integration_Process_Queue_Timer` and configure it as follows:
   * Time - `50`
   * Mode - `CountDown`
   * OnTImer - `GATE_HTTP->HA_Integration_Process_Queue()`


## How to perform a dynamic update

| Grenton object type               |   object event  | ha_entity example   |  grenton service    | value_1             | value_2  | value_3  | string_value |
|-----------------------------------|-----------------|---------------------|---------------------|---------------------|----------|----------|--------------|
| DOUT - Light / Switch / Binary Sensor  | OnValueChange   | light.lamp1         |   set_state         | CLU->dout->Value  |    (default)     |      (default)    |       (default)     |
| DIMMER - Light                    | OnValueChange   | light.lamp2         |   set_brightness         | CLU->dimmer->Value  |    (default)     |     (default)    |       (default)    |
| LED - Light                      | OnValueChange   | light.lamp3         |   set_brightness         | CLU->led->Value  |    (default)    |     (default)    |       (default)     |
| -                             | OnValueChange   | light.lamp3         |   set_rgb         | (default)  |    (default)     |      (default)    |       CLU->led->RGB     |
| ONE_WIRE / TEMPERATURE / ANALOG IN / Other - Sensor  | OnValueChange   | sensor.tempsens1         |   set_value         | CLU->sensor->Value  |    (default)    |     (default)    |       (default)     |
| ROLLER_SHUTTER - Cover  | OnStateChange   | cover.blinds1         |   set_cover         | CLU->roller->State  |    CLU->roller->Position   |     CLU->roller->LamelPosition    |       (default)     |
<!-- | THERMOSTAT - Climate  | OnStart   | climate.therm1         |   set_therm_state         | CLU->thermostat->State  |    (default)     |      (default)    |       (default)     |
| -                     | OnStop   | climate.therm1         |   set_therm_state         | CLU->thermostat->State  |    (default)     |      (default)    |       (default)     |
| -                     | OnChange   | climate.therm1         |   set_therm_target_temp         | CLU->thermostat->PointValue  |    (default)     |      (default)    |       (default)     |
| *THERMOSTAT temp sensor  | OnValueChange   | climate.therm1         |   set_therm_current_temp         | CLU->sensor->Value  |    (default)     |      (default)    |       (default)     | -->

## Usage example

### DOUT - Light / Switch / Binary Sensor

<img width="864" height="643" alt="image" src="https://github.com/user-attachments/assets/bd2fdec5-912d-432f-8859-488c2ed02dba" />


<img width="836" height="543" alt="image" src="https://github.com/user-attachments/assets/b5789a7d-3116-41ab-828b-335cc11b54a6" />



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
<!-- | Climate                            |  set_therm_state       | state [0 (off), 1 (on)], direction (optional) [0 (normal/heat), 1 (reverse/cool)] |
| Climate                            |  set_therm_target_temp | temp (target temp)                                |
| Climate                            |  set_therm_current_temp | temp (current temp)                              | -->
