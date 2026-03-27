from typing import List, Tuple, Set
import re
import difflib
# import json
from sklearn.metrics import f1_score
import numpy as np


def normalize_text(lines: list[str]) -> list[str]:

    res = []

    for s in lines:
        s = re.sub(r"\(.*?\)|\[.*?\]", " ", s)
        s = s.lower()
        s = re.sub(r"[^а-яa-z0-9\s\-']", " ", s)
        s = re.sub(r"\s+", " ", s)
        s = s.strip()
        if s:
            res.append(s)
            
    return res


_similarity_cache: dict[Tuple[str, str], int] = {}

def similarity(target: str, cur: str) -> int:

    key = (target, cur)
    if key in _similarity_cache:
        return _similarity_cache[key]

    dist = difflib.SequenceMatcher(None, target, cur).ratio()

    if dist >= 0.9999:
        res = 1
    elif dist > 0.9:
        res = -1
    else:
        res = 0

    _similarity_cache[key] = res
    return res
    

def merge_sections(pairs: List[List[int]], lyrics: List[List[str]]) -> List[List[int]]:

    if not pairs:
        return []

    pairs.sort(key=lambda x: x[0])
    merged_list = [pairs[0].copy()]

    for pair in pairs[1:]:
        last_section = merged_list[-1]
        seg1 = lyrics[last_section[0]: last_section[1] + 1]
        seg2 = lyrics[pair[0]: pair[1] + 1]
        if_chorus_identical = [similarity(cur, targ) for cur, targ in zip(seg1, seg2)]

        if pair[0] <= last_section[1] + 1 and all(x != 0 for x in if_chorus_identical) and not all(x == 1 for x in if_chorus_identical):
            last_section[1] = max(last_section[1], pair[1])
        else:
            merged_list.append(pair.copy())
    
    return merged_list


def find_best_chorus(lyrics: List[List[str]]) -> List[List[int]]:

    # best_chorus = []
    best_chorus_length = 0
    best_chorus_repetitions: List[List[int]] = []

    n = len(lyrics)
    max_len = 16

    for start in range(n):

        for length in range(2, max_len + 1):
            chorus = lyrics[start:start + length]
            repetitions = [[start, start + length - 1]]
            current_pos = start + length

            while current_pos < n:
                seg = lyrics[current_pos:current_pos + length]

                if len(seg) < length:
                    break

                if_chorus_res = [similarity(cur, targ) for cur, targ in zip(seg, chorus)]

                if all(x != 0 for x in if_chorus_res):
                    repetitions.append([current_pos, current_pos + length - 1])
                    current_pos += length
                else:
                    current_pos += 1
                    # print('#')

            repetitions = merge_sections(repetitions, lyrics)
            # print(repetitions)

            if len(repetitions) >= 2 and (
                    (length > best_chorus_length and len(repetitions) >= len(best_chorus_repetitions)) or
                    (length == best_chorus_length and len(repetitions) > len(best_chorus_repetitions))
            ):
                # best_chorus = chorus
                best_chorus_length = length
                best_chorus_repetitions = repetitions

    return best_chorus_repetitions


class Solution:

    def detect(self, tracks: List[Tuple[List[str], str]]) -> List[Set[Tuple[int, int]]]:
        results = []

        for lyrics, name in tracks:
            if not lyrics:
                results.append([])
                continue

            normalized = [normalize_text([line])[0] if normalize_text([line]) else "" for line in lyrics]

            repetitions = find_best_chorus(normalized)

            if repetitions:
                results.append([(int(s), int(e)) for s, e in repetitions])
            else:
                results.append([])

        return results


"""def ranges_to_mask(ranges: List[List[int]], n_lines: int) -> List[int]:
    mask = [0] * n_lines
    for start, end in ranges:
        for i in range(start, end + 1):
            if i < n_lines:
                mask[i] = 1
    return mask


def evaluate_model(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    model = Solution()
    all_f1 = []

    for track in data:
        lines = track["lines"]
        true_chorus = track["chorus"]

        true_mask = ranges_to_mask(true_chorus, len(lines))

        pred_groups = model.detect([(lines, track["title"])])[0]
        pred_mask = ranges_to_mask(pred_groups, len(lines))

        min_len = min(len(true_mask), len(pred_mask))
        true_mask = true_mask[:min_len]
        pred_mask = pred_mask[:min_len]

        f1 = f1_score(true_mask, pred_mask, zero_division=0)
        all_f1.append(f1)

        print(f"{track['title']}: F1 = {f1:.3f}")

    mean_f1 = np.mean(all_f1)
    print(f"\nСредний F1-score по всем трекам: {mean_f1:.3f}")
    return mean_f1


mean_f1 = evaluate_model("tracks.json")



example_tracks = [
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