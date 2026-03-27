from typing import List, Tuple, Set
import re
import difflib


def normalize_text(s: str) -> str:
    s = re.sub(r"\(.*?\)|\[.*?\]", " ", s)
    s = s.lower()
    s = re.sub(r"[^а-яa-z0-9\s\-']", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()
    
    
"""def find_groups_easiest(labels):
    groups = []
    n = len(labels)
    start = None

    for i in range(n):
        # print('*')
        if labels[i] is not None:
            if start is None:
                start = i
        else:
            if start is not None:
                expected_length_chorus = i - start
                if expected_length_chorus >= 2:
                    groups.append((start, i - 1))
                i_next = i + 1
                start = None
                break
    count = 0
    for j in range(i_next, n):
        # print('#')
        if labels[j] is not None:
            if start is None:
                start = j
                count += 1
            else:
                if count == expected_length_chorus:
                    groups.append((start, j - 1))
                    start = j
                    count = 1
                elif count < expected_length_chorus & start is not None:
                    count += 1

        else:
            if start is not None:
                if count == expected_length_chorus:
                    groups.append((start, j - 1))
                    count = 0
                    start = None

    if start is not None and n - start >= 2:
        groups.append((start, n - 1))

    return groups"""


def find_groups(labels):
    groups = []
    n = len(labels)
    start = None
    expected_length = None

    for i in range(n):
        if labels[i] is not None:
            if start is None:
                start = i
        else:
            if start is not None:
                length = i - start
                if length >= 2:
                    expected_length = length
                    groups.append((start, i - 1))
                    break
                start = None

    if expected_length is None:
        return []

    start = None
    count = 0
    for i in range(groups[0][1] + 1, n):
        if labels[i] is not None:
            if start is None:
                start = i
                count = 1
            else:
                count += 1

            if count == expected_length:
                groups.append((start, i))
                start = None
                count = 0
        else:
            start = None
            count = 0

    seen = {}
    for s, e in groups:
        block = tuple(labels[s:e + 1])
        seen[block] = seen.get(block, 0) + 1

    final_groups = [(s, e) for (s, e) in groups if seen[tuple(labels[s:e + 1])] > 1]

    return final_groups


class Solution:

    def detect(self, tracks: List[Tuple[List[str], str]]) -> List[Set[Tuple[int, int]]]:
        results = []

        for lyrics, name in tracks:
            if not lyrics:
                results.append([])
                continue

            normalized = [normalize_text(line) for line in lyrics]
            n = len(normalized)

            labels = [None] * n
            current_label = 1

            for i in range(n):
                if labels[i] is not None:
                    continue

                labels[i] = current_label

                for j in range(i + 1, n):
                    ratio = difflib.SequenceMatcher(None, normalized[i], normalized[j]).ratio()
                    if ratio > 0.65:
                        labels[j] = current_label

                current_label += 1

            #print(labels)
            only_choruses = [None] * n
            for i in range(n):
                for j in range(i+1, n):
                    if labels[i]==labels[j]:
                        only_choruses[i]=only_choruses[j]=labels[i]
                
            #print(only_choruses)
            #choruses = sorted(set(choruses))
            #print("---------------------------------------------------------------")
            #print(choruses)

            filtered = find_groups(only_choruses)
            #print(filtered)

            results.append(filtered)

        return results


"""example_tracks = [
    (
        [
            "Тёмный, мрачный коридор",
            "Я на цыпочках, как вор",
            "Пробираюсь, чуть дыша",
            "Чтобы не вспугнуть",
            "Тех, кто спит уже давно",
            "Тех, кому не всё равно",
            "В чью я комнату тайком",
            "Желаю заглянуть",
            "Чтобы увидеть",
            "Как бессонница в час ночной",
            "Меняет, нелюдимая, облик твой",
            "Чьих невольница ты идей?",
            "Зачем тебе охотиться на людей?",
            "Крестик на моей груди",
            "На него ты погляди",
            "Что в тебе способен он",
            "Резко изменить?",
            "Много книжек я читал",
            "Много фокусов видал",
            "Свою тайну от меня",
            "Не пытайся скрыть!",
            "Я это видел!",
            "Как бессонница в час ночной",
            "Меняет, нелюдимая, облик твой",
            "Чьих невольница ты идей?",
            "Зачем тебе охотиться на людей?",
            "Очень жаль, что ты тогда",
            "Мне поверить не смогла",
            "В то, что новый твой приятель",
            "Не такой, как все!"
        ],
        "Пример 1"
    ),
    (
        [
            "Я падаю вниз, я срываюсь со всех краёв",
            "Хотел выше птиц, но не попадаю в дверной проём",
            "Я опустился... Куда бы с тобою не смог",
            "Я распустился, как ядовитый цветок",
            "Я так хотел, чтоб ты",
            "Была счастлива со мной",
            "Но я — отрицательный герой",
            "Ведь я так хотел, чтоб ты",
            "Была счастлива со мной",
            "Но я — отрицательный герой",
            "Я не хочу, чтоб ты сомневалась в себе",
            "Я заплачу за все твои слёзы, поверь",
            "Я хуже тебя, мои обещания дешевле твоих, а-а",
            "Ты меня не прощай, я шум... И я стих",
            "Я так хотел, чтоб ты",
            "Была счастлива со мной",
            "Но я — отрицательный герой",
            "Ведь я так хотел, чтоб ты",
            "Была счастлива со мной",
            "Но я — отрицательный герой",
            "Я так хотел, чтоб ты",
            "Была счастлива со мной",
            "Но я — отрицательный герой",
            "Ведь я так хотел, чтоб ты",
            "Была счастлива со мной",
            "Но я — отрицательный герой"
        ],
        "Пример 3"
    ),
    (
        [
            "Кто, не знаю, распускает слухи зря",
            "Что живу я без печали и забот",
            "Что на свете всех удачливее я",
            "И всегда, и во всём мне везёт",
            "Так же, как все, как все, как все",
            "Я по земле хожу, хожу",
            "И у судьбы, как все, как все",
            "Счастья себе прошу",
            "Вы не верьте, что живу я, как в раю",
            "И обходит стороной меня беда",
            "Точно так же я под вечер устаю",
            "И грущу, и реву иногда",
            "Так же, как все, как все, как все",
            "Я по земле хожу, хожу",
            "И у судьбы, как все, как все",
            "Счастья себе прошу",
            "Жизнь меня порой колотит и трясёт",
            "Но от бед известно средство мне одно",
            "В горький час, когда смертельно не везёт",
            "Говорю, что везёт всё равно",
            "Так же, как все, как все, как все",
            "Я по земле хожу, хожу",
            "И у судьбы, как все, как все",
            "Счастья себе прошу",
            "И у судьбы, как все, как все",
            "Счастья себе прошу",
            "Счастья себе прошу..."
        ],
        "Пример 4"
    ),
    (
        [
            "Сколько сказано слов о любви, сколько спето",#1
            "Эта тема задета каждым поэтом",#2
            "Но я, не желая им уподобляться",#3
            "Предпочитал стихам совокупляться",#4
            "Но какое-то чувство в момент нашей встречи",#5
            "Озарило глаза мои нежно-зелёным",#6
            "Пошлость потеряла дар речи",#7
            "Наполнив мне лёгкие чем-то влюблённым",#8

            "Сердце в груди как только начало биться",#9
            "Стремиться быть с тобой рядом",#10
            "Ощущая тепло любимого взгляда",#11
            "Лучшее, что могло со мною случиться",#12

            "Я устал от сучек, лжи, запаха псины",
            "Ты - счастливейший случай быть самым красивым",
            "Так устав от зимы, я нашёл в тебе лето",
            "Я вышел из тьмы – значит, я иду к свету",
            "В этом мире жестоком, где нежность как слабость",
            "Где, чтобы выжить, ты вынужден биться",
            "Я набрался неслыханной наглости",
            "Я позволил себе влюбиться",

            "Сердце в груди продолжает беситься",
            "Стремиться быть с тобой рядом",
            "Ощущая тепло влюблённого взгляда",
            "Лучшее, что могло со мною случиться",

            "Сквозь покрытые дымом конопляные степи",
            "Я прошёл, переплыл океаны спиртного",
            "Искушён всеми бесами, но обошёл их",
            "А любовь оказалась сильней их намного",
            "И словно голодный, капризный мальчишка",
            "Узнавший, как просто унять этот голод",
            "Нашёл в тебе повод быть самым счастливым",
            "Если для этого вообще нужен повод",
            "Сердце в груди стучит словно молот",
            "И голым засыпать с тобой рядом",
            "Ощущая тепло влюблённого взгляда",
            "Лучшее мне и не надо иного",

            "Сердце в груди стучит словно птица",
            "Стремиться быть с тобой рядом",
            "Ощущая тепло любимого взгляда",
            "Лучшее, что могло со мною случиться",
            "Лучшее, что могло со мною случиться"
        ],
        "Пример 5"
    )
]

true_result = [
    # Пр 1
    {(9, 12), (22, 25)},
    # Пр 3
    {(4,9), (14,19), (20,25)},
    # Пр 4
    {(4, 7), (12, 15), (20, 23)},
    # Пр 5
    {(8,11), (20,23), (36,40)}
]

model = Solution()
predicted = model.detect(example_tracks)

print(predicted)
print("-------------------------------------------------------------")
print(true_result)

f1_scores = []

pred_sets = [set(p) for p in predicted]

for i, (pred, true) in enumerate(zip(pred_sets, true_result)):
    tp = len(pred & true)
    fp = len(pred - true)
    fn = len(true - pred)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    f1_scores.append(f1)
    print(f"\nПесня {i+1}:")
    print(f"F1={f1:.3f}")

print("\n-------------------------------------------------------------")
print(f"Средний F1: {sum(f1_scores) / len(f1_scores):.3f}")"""