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
        return {
            tla: self.calculate_game_points(info['events'])
            for tla, info in self._teams_data.items()
        }

    @staticmethod
    def calculate_game_points(events):
        def can_up(backs, tokens, score):
            return backs, tokens + 1, score

        def can_down(backs, tokens, score):
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

        return score


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
