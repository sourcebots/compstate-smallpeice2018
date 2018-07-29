CORNER_POINTS = 6
CAN_CORNER_POINTS = 4
CAN_END_POINTS = 2
CANS_IN_ARENA = 7


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
                        "Only one team can be holding the super can at the end",
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
        def can_up(backs, cans, score):
            if cans == CANS_IN_ARENA:
                raise InvalidScoresheetException(
                    "Cannot pick up can -- already holding all the cans",
                )
            return backs, cans + 1, score

        def can_down(backs, cans, score):
            if cans == 0:
                raise InvalidScoresheetException(
                    "Cannot put down can -- not currently holding any cans",
                )
            return backs, cans - 1, score

        event_handlers = {
            'b': lambda backs, cans, score: (backs + 1, cans, score),
            'c': lambda backs, cans, score:
                (0, cans, score + CORNER_POINTS + (cans * CAN_CORNER_POINTS))
                if backs == 0
                else (backs - 1, cans, score),
            'u': can_up,
            'd': can_down,
            'END': lambda backs, cans, score:
                (backs, cans, score + (cans * CAN_END_POINTS)),
        }

        events = list(events.lower()) + ['END']

        backs, cans, score = 0, 0, 0
        for event in events:
            if event.isspace():
                continue

            backs, cans, score = event_handlers[event](backs, cans, score)

        if holding_super and cans == 0:
            raise InvalidScoresheetException(
                "Cannot be holding the super can -- not holding any cans at the end",
            )

        return score


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
