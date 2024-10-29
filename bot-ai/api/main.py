#if __name__ == '__main__':
    #pass
    # if not init_api(True):
    #     print('Failed to init api')
    #     quit()

    # success, teams = get_players_by_game_id(game_id)
    # if not success:
    #     print('Failed to get teams for server ' + servername)
    #     quit()

    # for key in teams.keys():
    #     print(key)

    # playername = input("Enter player name to kick ")

    # reason = input("Reason: ")

    # success, details = get_full_server_details_by_game_id(game_id)
    # if not success:
    #     print_error_message('Failed to get server details for id ' + game_id, details)
    #     quit()

    # print(details)

    # details['result']['rspInfo']

    # success, persona_id = get_player_persona_by_name(playername)
    # if not success:
    #     print_error_message('Failed to get player ' + playername, persona_id)
    #     quit()

    # success, content = kick_player(game_id, persona_id, reason)

    # if not success:
    #     print_error_message('Failed to kick player with id ' + str(persona_id), content)
    #     quit()

    # print(content)

    # input('Press any key to exit')
