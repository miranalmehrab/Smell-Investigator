(lambda main: main(0, 'https://opensource.org/licenses/MIT', ''.join(filter(str.isalpha, __import__('random').choice(open('/usr/share/dict/words').readlines()).upper())), set(), '|======\n|   |\n| {3} {0} {5}\n|  {2}{1}{4}\n|  {6} {7}\n|  {8} {9}\n|', list('OT-\\-//\\||'), 10, main))(lambda _, license, chosen_word, guesses, scaffold, man, guesses_left, main_: main_(map(guesses.add, filter(str.isalpha, raw_input('%s(%s guesses left)\n%s\n%s:' % (','.join(sorted(guesses)), guesses_left, scaffold.format(*(man[:10-guesses_left] + [' '] * guesses_left)), ' '.join(letter if letter in guesses else '_' for letter in chosen_word))).upper())), license, chosen_word, guesses, scaffold, man, max((10 - len(guesses - set(chosen_word))), 0), main_) if not all(letter in guesses for letter in chosen_word) and guesses_left else __import__('sys').stdout.write('You ' + ['lose!\n' + scaffold.format(*man), 'win!'][bool(guesses_left)] + '\nWord was ' + chosen_word + '\n'))