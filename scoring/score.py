CORNER_POINTS = 6
TOKEN_CORNER_POINTS = 4
TOKEN_END_POINTS = 2


class InvalidScoresheetException(Exception):
    pass


class Scorer(object):
    def __init__(self, teams_data, arena_data):
        self._teams_data = teams_data
        self._arena_data = arena_data

    def calculate_scores(self):
        scores = {
            tla: self.calculate_game_points(info['events'], info.get('holding-super'))
            for tla, info in self._teams_data.items()
        }

        tla_holding_super = None
        for tla, info in self._teams_data.items():
            if info.get('holding-super'):
                if tla_holding_super is not None:
                    raise InvalidScoresheetException(
                        "Only one team can be holding the super token at the end",
                    )
                tla_holding_super = tla

        def opponent_holds_super(tla):
            return tla_holding_super is not None and tla_holding_super != tla

        scores = {
            tla: score if not opponent_holds_super(tla) else score * 0.5
            for tla, score in scores.items()
        }

        return scores

    @staticmethod
    def calculate_game_points(events, holding_super):
        def can_up(backs, tokens, score):
            return backs, tokens + 1, score

        def can_down(backs, tokens, score):
            if tokens == 0:
                raise InvalidScoresheetException(
                    "Cannot put down token -- not currently holding any tokens",
                )
            return backs, tokens - 1, score

        event_handlers = {
            'b': lambda backs, tokens, score: (backs + 1, tokens, score),
            'c': lambda backs, tokens, score:
                (0, tokens, score + CORNER_POINTS + (tokens * TOKEN_CORNER_POINTS))
                if backs == 0
                else (backs - 1, tokens, score),
            'u': can_up,
            'd': can_down,
            'END': lambda backs, tokens, score:
                (backs, tokens, score + (tokens * TOKEN_END_POINTS)),
        }

        events = list(events.lower()) + ['END']

        backs, tokens, score = 0, 0, 0
        for event in events:
            if event.isspace():
                continue

            backs, tokens, score = event_handlers[event](backs, tokens, score)

        if holding_super and tokens == 0:
            raise InvalidScoresheetException(
                "Cannot be holding the super token -- not holding any tokens at the end",
            )

        return score


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
