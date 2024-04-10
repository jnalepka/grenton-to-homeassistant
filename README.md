# GrentonHomeAssistantIntegration

```yaml
  - platform: grenton_objects
    name: "Integracja Janek Lampa"
    api_endpoint: http://192.168.0.4
    grenton_id: CLU221001090->ZWA8272
```

grenton

```lua
local reqJson = GATE_HTTP->HA_Listener_Integration->RequestBody
local code, resp

logDebug("HA integration script start")

if reqJson.command then
	local s = reqJson.command
	logDebug("HA integration s>> " .. s)
	local p1, p2 = string.match(s, "(.-)->(.+)")
	local g_command = p1 .. ':execute(0, "' .. p2 .. '")'   
	logDebug("HA integration command cmd>> " .. g_command)
	load(g_command)()
	
	resp = { g_status = "ok" }
	code = 200

elseif reqJson.status then
	local s = reqJson.status
	logDebug("HA integration s>> " .. s)
	local p1, p2 = string.match(s, "(.-)->(.+)") 
	local g_command = 'return ' .. p1 .. ':execute(0, "' .. p2 .. '")'
	logDebug("HA integration status cmd>> " .. g_command)
	local g_object_value = load(g_command)()
	logDebug("HA integration status g_object_value>> " .. g_object_value)
	resp = { object_value = g_object_value }
	code = 201
else
	resp = { g_status = "Grenton script error" }
	code = 400
end


GATE_HTTP->HA_Listener_Integration->SetStatusCode(code)
GATE_HTTP->HA_Listener_Integration->SetResponseBody(resp)
GATE_HTTP->HA_Listener_Integration->SendResponse()
```

temp

```yaml
# Loads default set of integrations. Do not remove.
default_config:

# Load frontend themes from the themes folder
frontend:
  themes: !include_dir_merge_named themes

automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml

http:
  ssl_certificate: /ssl/fullchain.pem
  ssl_key: /ssl/privkey.pem

google_assistant:
  project_id: home-assistant-97980
  service_account: !include watchful-goods-419415-50b348f76563.json
  report_state: false
  exposed_domains:
    - light
  entity_config:
    light.attic_jan_lamp:
      name: Lampa Janek
      expose: true
    light.stairs_lamp:
      name: Lampa Schody
      expose: true
    light.livingroom_lamp:
      name: Lampa Salon
      expose: true
    light.marysia_lamp:
      name: Lampa Marysia
      expose: true
    light.kitchen_lamp:
      name: Lampa Kuchnia
      expose: true
    light.bathroom_lamp:
      name: Lampa Łazienka
      expose: true
    light.corridor_lamp:
      name: Lampa Korytarz
      expose: true
    light.entrance_room_lamp:
      name: Lampa Wiatrołap
      expose: true

light:
  - platform: template
    lights:
      attic_jan_lamp:
        friendly_name: "Lampa Janek"
        unique_id: attic_jan_lamp
        turn_on:
          service: rest_command.attic_jan_lamp_on
        turn_off:
          service: rest_command.attic_jan_lamp_off
      stairs_lamp:
        friendly_name: "Lampa Schody"
        unique_id: stairs_lamp
        turn_on:
          service: rest_command.stairs_lamp_on
        turn_off:
          service: rest_command.stairs_lamp_off
      livingroom_lamp:
        friendly_name: "Lampa Salon"
        unique_id: livingroom_lamp
        turn_on:
          service: rest_command.livingroom_lamp_on
        turn_off:
          service: rest_command.livingroom_lamp_off
      marysia_lamp:
        friendly_name: "Lampa Marysia"
        unique_id: marysia_lamp
        turn_on:
          service: rest_command.marysia_lamp_on
        turn_off:
          service: rest_command.marysia_lamp_off
      kitchen_lamp:
        friendly_name: "Lampa Kuchnia"
        unique_id: kitchen_lamp
        turn_on:
          service: rest_command.kitchen_lamp_on
        turn_off:
          service: rest_command.kitchen_lamp_off
      bathroom_lamp:
        friendly_name: "Lampa Łazienka"
        unique_id: bathroom_lamp
        turn_on:
          service: rest_command.bathroom_lamp_on
        turn_off:
          service: rest_command.bathroom_lamp_off
      corridor_lamp:
        friendly_name: "Lampa Korytarz"
        unique_id: corridor_lamp
        turn_on:
          service: rest_command.corridor_lamp_on
        turn_off:
          service: rest_command.corridor_lamp_off
      entrance_room_lamp:
        friendly_name: "Lampa Wiatrołap"
        unique_id: entrance_room_lamp
        turn_on:
          service: rest_command.entrance_room_lamp_on
        turn_off:
          service: rest_command.entrance_room_lamp_off
  - platform: grenton_objects
    name: "Integracja Janek Lampa"
    api_endpoint: http://192.168.0.4
    grenton_id: CLU221001090->ZWA8272

rest_command:
  attic_jan_lamp_on:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"jan_lamp", "state":"on"}'
  attic_jan_lamp_off:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"jan_lamp", "state":"off"}'
  stairs_lamp_on:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"stairs_lamp", "state":"on"}'
  stairs_lamp_off:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"stairs_lamp", "state":"off"}'
  livingroom_lamp_on:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"livingroom_lamp", "state":"on"}'
  livingroom_lamp_off:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"livingroom_lamp", "state":"off"}'
  marysia_lamp_on:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"marysia_lamp", "state":"on"}'
  marysia_lamp_off:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"marysia_lamp", "state":"off"}'
  kitchen_lamp_on:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"kitchen_lamp", "state":"on"}'
  kitchen_lamp_off:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"kitchen_lamp", "state":"off"}'
  bathroom_lamp_on:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"bathroom_lamp", "state":"on"}'
  bathroom_lamp_off:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"bathroom_lamp", "state":"off"}'
  corridor_lamp_on:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"corridor_lamp", "state":"on"}'
  corridor_lamp_off:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"corridor_lamp", "state":"off"}'
  entrance_room_lamp_on:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"entrance_room_lamp", "state":"on"}'
  entrance_room_lamp_off:
    url: http://192.168.0.4/HAlistener
    method: post
    content_type: "application/json"
    payload: '{"object":"entrance_room_lamp", "state":"off"}'
```
