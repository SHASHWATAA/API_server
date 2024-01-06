import time
from credentials import home_assistantant_token as token
from requests import post, get

living_room_tv_entity_id = "media_player.samsung_7_series_50"
# Define the headers
ha_authorization_headers = {
    "Authorization": f"Bearer {token}",
    "content-type": "application/json",
}


def turn_on_tv(entity_id, headers):
    # Define the entity ID

    # Check if the TV is on
    url_state = f"https://ha.shash.win/api/states/{entity_id}"
    response_state = get(url_state, headers=headers)
    state = response_state.json()["state"]

    # If the TV is off, try to turn it on up to 3 times
    for i in range(3):
        if state == "off":
            url_turn_on = "https://ha.shash.win/api/services/media_player/turn_on"
            data_turn_on = {"entity_id": entity_id}
            response_turn_on = post(url_turn_on, headers=headers, json=data_turn_on)

            # Poll the API until the TV turns on or 8 seconds have passed
            start_time = time.time()
            while state == "off" and time.time() - start_time < 8:
                response_state = get(url_state, headers=headers)
                state = response_state.json()["state"]
                time.sleep(1)  # wait for 1 second before polling again

        # If the TV is on, break the loop
        if state == "on":
            break

    return state


def turn_off_tv(entity_id, headers):
    # Define the entity ID

    # Check if the TV is on
    url_state = f"https://ha.shash.win/api/states/{entity_id}"
    response_state = get(url_state, headers=headers)
    state = response_state.json()["state"]

    # If the TV is off, try to turn it on up to 3 times
    for i in range(3):
        if state == "on":
            url_turn_off = "https://ha.shash.win/api/services/media_player/turn_off"
            data_turn_off = {"entity_id": entity_id}
            response_turn_off = post(url_turn_off, headers=headers, json=data_turn_off)

            # Poll the API until the TV turns on or 8 seconds have passed
            start_time = time.time()
            while state == "on" and time.time() - start_time < 8:
                response_state = get(url_state, headers=headers)
                state = response_state.json()["state"]
                time.sleep(1)  # wait for 1 second before polling again

        # If the TV is on, break the loop
        if state == "off":
            break

    return state


def switch_tv_to_plex(entity_id):
    url_select_source = "https://ha.shash.win/api/services/media_player/select_source"
    data_select_source = {
        "entity_id": entity_id,
        "source": "Plex"
    }
    response_select_source = post(url_select_source, headers=ha_authorization_headers, json=data_select_source)
    return response_select_source.status_code


def movie_time(entity_id, headers):
    state = turn_on_tv(entity_id, headers)
    # If the TV is on, change the source to Plex
    if state == "on":
        switch_tv_to_plex(entity_id)
        return True
    else:
        print("The TV did not turn on within the specified time.")
        return False


if __name__ == '__main__':
    movie_time(living_room_tv_entity_id,ha_authorization_headers)
