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
        event_handlers = {
            'b': lambda backs, tokens, score: (backs + 1, tokens, score),
            'c': lambda backs, tokens, score:
                (0, tokens, score + 1 + tokens)
                if backs == 0
                else (backs - 1, tokens, score),
            'u': lambda backs, tokens, score: (backs, tokens + 1, score),
            'd': lambda backs, tokens, score: (backs, tokens - 1, score),
            'END': lambda backs, tokens, score: (backs, tokens, score + tokens),
        }

        events = list(events.lower()) + ['END']

        backs, tokens, score = 0, 0, 0
        for event in events:
            backs, tokens, score = event_handlers[event](backs, tokens, score)

        return score


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
