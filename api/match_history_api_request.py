from api.api_request import ApiRequest


class MatchHistoryApiRequest(ApiRequest):
    def __init__(self, endpoint):
        super().__init__(endpoint)

    def with_hero_id(self, hero_id: int):
        self.query_parameters["hero_id"] = hero_id
        return self

    def with_game_mode(self, game_mode: int):
        self.query_parameters["game_mode"] = game_mode
        return self

    def with_skill(self, skill: int):
        self.query_parameters["skill"] = skill
        return self

    def with_min_players(self, min_players: int):
        self.query_parameters["min_players"] = str(min_players)
        return self

    def with_account_id(self, account_id: int):
        self.query_parameters["account_id"] = str(account_id)
        return self

    def with_league_id(self, league_id: int):
        self.query_parameters["league_id"] = str(league_id)
        return self

    def with_start_at_match_id(self, start_at_match_id: int):
        if start_at_match_id != -1:
            self.query_parameters["start_at_match_id"] = str(start_at_match_id)

        return self

    def with_matches_requested(self, matches_requested: int):
        self.query_parameters["matches_requested"] = str(matches_requested)
        return self

    def with_tournament_games_only(self, tournament_games_only: bool):
        if tournament_games_only is True:
            flag = "1"
        else:
            flag = "0"

        self.query_parameters["tournament_games_only"] = flag
        return self
