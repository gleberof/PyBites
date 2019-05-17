scores = [10, 50, 100, 175, 250, 400, 600, 800, 1000]
ranks = 'white yellow orange green blue brown black paneled red'.split()
BELTS = dict(zip(scores, ranks))

CONGRATS_MSG = ('Congrats, you earned {score} points '
                'obtaining the PyBites Ninja {rank} Belt')
NEW_SCORE_MSG = 'Set new score to {score}'

class NinjaBelt:

    def __init__(self, score=0):
        self._score = score
        self._last_earned_belt = None

    def _get_belt(self, new_score):
        """Might be a useful helper"""
        return max([(s, b) for s, b in BELTS.items() if s <= new_score])[1]

    def _get_score(self):
        return self._score

    def _set_score(self, new_score):
        if not isinstance(new_score, int):
            raise ValueError
        if new_score > self._score:
            self._score = new_score
            if self._get_belt(new_score) != self._last_earned_belt:
                self._last_earned_belt = self._get_belt(new_score)
                print(str(CONGRATS_MSG.format(score=new_score, rank=self._last_earned_belt.title())))
            else:
                print(str(NEW_SCORE_MSG.format(score=new_score)))
        return

    score = property(_get_score, _set_score)
