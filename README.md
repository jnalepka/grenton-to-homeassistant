# GrentonObjects_HomeAssistant

This is an unofficial integration of the Grenton system with the Home Assistant.

If you like what I do, buy me a `coffee`!

[![](https://img.shields.io/static/v1?label=Donate&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://tipply.pl/@jnalepka)


# Installation

1. Copy the folder `grenton_objects` to the `custom_components` folder in your Home Assistant. Create the folder if you don't have it. You can use the Visual Studio Code add-on to create the folder and copy the files.

![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/110e00e8-a3ff-4be1-8b1e-c33639b87ea2)

2. Create a `HTTPListener` virtual object on GateHTTP named `HA_Listener_Integration` and configure it as follows:

* Path - `/HAlistener` (You can edit it if you want)
* ResponseType - `JSON`

  ![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/1d69d9fc-95f3-4f89-90e3-588b8637ffad)

3. Create a script named `HA_Integration_Script` and attach it to the OnRequest event of the virtual object.

```lua
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

4. Add your Grenton objects to the Home Assistant. Example:

```yaml
light:
  - platform: grenton_objects
    name: "Bedroom Lamp"
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->ZWA8272
  - platform: grenton_objects
    name: "Kitchen Lamp"
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->ZWA8272
```

where:
* `api_endpoint` - is your GateHTTP IP and HTTPListener patch
* `grenton_id` is copied from the Id section in the Grenton object properties window

  ![image](https://github.com/jnalepka/GrentonHomeAssistantIntegration/assets/70645322/0e4ede98-20fb-4a80-a759-b550633ae418)


5. Send configuration to the Grenton Gate HTTP, restart HomeAssistant, and test your new objects in your Dashboard!

> The data update in Home Assistant occurs automatically every 30 seconds.

# Configure Grenton objects

Add your objects to the `configuration.yaml` file.

## Switch (On_Off)

#### For:
* IO MODULE 8/8 DIN
* IO MODULE 2/2 FM
* RELAY X2 DIN
* RELAY X4 DIN
* RELAY Z-WAVE
* RELAY WI-FI

```yaml
switch:
  - platform: grenton_objects
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->DOU8272
    name: "Kitchen Radio Switch"
```

## Light (On_Off)

#### For:
* IO MODULE 8/8 DIN
* IO MODULE 2/2 FM
* RELAY X2 DIN
* RELAY X4 DIN
* RELAY Z-WAVE
* RELAY WI-FI

```yaml
light:
  - platform: grenton_objects
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->DOU8272
    name: "Bedroom Lamp"
```

## Light (Dimmer)

#### For:
* DIMMER DIN
* DIMMER FM
  
```yaml
light:
  - platform: grenton_objects
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->DIM8272
    name: "Bedroom Dimmer"
```

#### For:
* LED RGBW Z-WAVE (SINGLE ZWAVE_LED OBJECT)
  
```yaml
light:
  - platform: grenton_objects
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->ZWA8272
    grenton_type: DIMMER
    name: "Bedroom Dimmer"
```

## Light (RGB)

#### For:
* LED RGBW DIN
* LED RGBW FM

```yaml
light:
  - platform: grenton_objects
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->LED8272
    name: "Bedroom Led"
```

#### For:
* LED RGBW Z-WAVE

```yaml
light:
  - platform: grenton_objects
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->ZWA8272
    grenton_type: RGB
    name: "Bedroom Led"
```

## Cover (Roller_Shutter)

#### For:
* ROLLER SHUTTER DIN
* ROLLER SHUTTER X3 DIN
* ROLLER SHUTTER FM
* ROLLER SHUTTER Z-WAVE

```yaml
cover:
  - platform: grenton_objects
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->ROL5664
    name: "Kichen Blinds"
```

If `ReversePosition` is set to `Yes`:

```yaml
cover:
  - platform: grenton_objects
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->ROL5664
    reversed: True
    name: "Kichen Blinds"
```

## Climate (Thermostat)

#### For:
* THERMOSTAT - Virtual Object

```yaml
climate:
  - platform: grenton_objects
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->THE9334
    name: "Bedroom Thermostat"
```

## Sensor (OneWire / Temperature)

#### For:
* ONE_WIRE
* TEMPERATURE_SENSOR (MULTISENSOR)
* PANELSENSTEMP (SMART PANEL / TOUCH PANEL)

```yaml
sensor:
  - platform: grenton_objects
    api_endpoint: http://192.168.0.4/HAlistener
    grenton_id: CLU221001090->TEM5469
    name: "Bedroom Thermostat"
```

# Forced faster state update

By default, Home Assistant automatically refreshes entities every 30 seconds. If you want to accelerate the object update, go to the `Settings->Automations & Scenes` and set up the automation:

1. `Trigger` -> `Time and location` -> `Time pattern` -> e.g. `/10` (every 10 seconds)

![Przechwytywanie1](https://github.com/jnalepka/GrentonObjects_HomeAssistant/assets/70645322/305b7f35-63a8-4341-83e6-ac3a85006dfd)

2. `Action` -> `Other action` -> `Call service` -> `Home Assistant Core Integration: Update entity`
3. Select objects (`+Choose entity`) to be updated at specified intervals.

![Przechwytywanie2](https://github.com/jnalepka/GrentonObjects_HomeAssistant/assets/70645322/47d19f37-decb-4c7d-a5ed-c06bc66058a6)

4. Save and restart Home Assistant.


