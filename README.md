# GrentonObjects_HomeAssistant

This is an unofficial integration of the Grenton system with the Home Assistant.

## Installation

1. Copy the folder `grenton_objects` to the `custom_components` folder in your Home Assistant. Create the folder if you don't have it. You can use the Visual Studio Code add-on to create the folder and copy the files.

![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/110e00e8-a3ff-4be1-8b1e-c33639b87ea2)

2. Create a `HTTPListener` virtual object on GateHTTP named `HA_Listener_Integration` and configure it as follows:

* Path - `/HAlistener` (You can edit it if you want)
* ResponseType - `JSON`

  ![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/1d69d9fc-95f3-4f89-90e3-588b8637ffad)

3. Create a script and attach it to the OnRequest event of the virtual object.

```lua
local reqJson = GATE_HTTP->HA_Listener_Integration->RequestBody
local code, resp

if reqJson.command then
	local s = reqJson.command
	local p1, p2 = string.match(s, "(.-)->(.+)")
	local g_command = p1 .. ':execute(0, "' .. p2 .. '")'   
	logDebug("HA integration command >> " .. g_command)
	load(g_command)()
	resp = { g_status = "ok" }
	code = 200
elseif reqJson.status then
	local s = reqJson.status
	local p1, p2 = string.match(s, "(.-)->(.+)") 
	local g_command = 'return ' .. p1 .. ':execute(0, "' .. p2 .. '")'
	logDebug("HA integration status command>> " .. g_command)
	local g_object_value = load(g_command)()
	resp = { object_value = g_object_value }
	code = 200
else
	resp = { g_status = "Grenton script error" }
	code = 400
end

GATE_HTTP->HA_Listener_Integration->SetStatusCode(code)
GATE_HTTP->HA_Listener_Integration->SetResponseBody(resp)
GATE_HTTP->HA_Listener_Integration->SendResponse()
```

> NOTE! Pay attention to the name of the GATE and the Object.

![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/25a94dee-a43a-4b32-a3f2-83c455652688)

4. Add your Grenton objects to the Home Assistant. Example:

```yaml
light:
  - platform: grenton_objects
    name: "Bedroom Lamp"
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->ZWA8272
  - platform: grenton_objects
    name: "Kitchen Lamp"
    api_endpoint: [http://192.168.0.4](http://192.168.0.4/HAlistener)
    grenton_id: CLU221001090->ZWA8272
```

where:
* `api_endpoint` - is your GateHTTP IP and HTTPListener patch
* `grenton_id` is copied from the Id section in the Grenton object properties window

  ![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/0e4ede98-20fb-4a80-a759-b550633ae418)


5. Send configuration to the Grenton Gate HTTP, restart HomeAssistant, and test your new objects in your Dashboard!

> The data update in Home Assistant occurs automatically every 30 seconds.

## Grenton objects

### Light (On_Off)

```yaml
light:
  - platform: grenton_objects
    name: "Bedroom Lamp"
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->ZWA8272
```

#### Work with:
* IO MODULE 8/8
* IO MODULE 2/2 FM
* RELAY X2
* RELAY X4
* RELAY Z-WAVE
* RELAY WI-FI
