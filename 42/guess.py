import random

MAX_GUESSES = 5
START, END = 1, 20


def get_random_number():
    """Get a random number between START and END, returns int"""
    return random.randint(START, END)


class Game:
    """Number guess class, make it callable to initiate game"""

    def __init__(self):
        """Init _guesses, _answer, _win to set(), get_random_number(), False"""
        self._guesses = set()
        self._answer = get_random_number()
        self._win = False

    def guess(self):
        """Ask user for input, convert to int, raise ValueError outputting
           the following errors when applicable:
           'Please enter a number'
           'Should be a number'
           'Number not in range'
           'Already guessed'
           If all good, return the int"""
        g = input()

        if g == '':
            raise ValueError('Please enter a number')

        try:
            g = int(g)
        except ValueError:
            raise ValueError('Should be a number') from None
        except TypeError:
            raise ValueError('Please enter a number') from None

        if not (START <= g <= END):
            raise ValueError('Number not in range')

        if g in self._guesses:
            raise ValueError('Already guessed')

        self._guesses.add(g)
        return g


    def _validate_guess(self, guess):
        """Verify if guess is correct, print the following when applicable:
           {guess} is correct!
           {guess} is too low
           {guess} is too high
           Return a boolean"""
        if guess == self._answer:
            print(f'{guess} is correct!')
            return True
        elif guess < self._answer:
            print(f'{guess} is too low')
        else:
            print(f'{guess} is too high')
        return False

    def __call__(self):
        """Entry point / game loop, use a loop break/continue,
           see the tests for the exact win/lose messaging"""
        while len(self._guesses) < MAX_GUESSES:
            try:
                guess = self.guess()
                if self._validate_guess(guess):
                    self._win = True
                    print(f'It took you {len(self._guesses)} guesses')
                    return
            except ValueError as e:
                print(e)

        print(f'Guessed {MAX_GUESSES} times, answer was {self._answer}')
        return


if __name__ == '__main__':
    game = Game()
    game()