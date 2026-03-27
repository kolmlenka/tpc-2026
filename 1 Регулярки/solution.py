PASSWORD_REGEXP = r'^(?=.{8,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=(?:.*[\^$%@#&*!?]){2,})(?!.*(.)\1)[A-Za-z0-9^$%@#&*!?]+$'

COLOR_REGEXP = r'^(?:#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})|rgb\((?:100%|\d{1,2}%)(?:, ?(?:100%|\d{1,2}%)){2}\)|rgb\((?:\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])(?:, ?(?:\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])){2}\)|hsl\((?:\d{1,2}|1\d{2}|2\d{2}|3[0-5]\d|360)(?:, ?(?:100%|[1-9]?\d%)){2}\))$'

EXPRESSION_REGEXP = r''

DATES_REGEXP = r'^(?:(?:0?[1-9]|[12]\d|3[01])([.\-/])(0?[1-9]|1[0-2])\1\d{1,4}|\d{1,4}([.\-/])(0?[1-9]|1[0-2])\3(0?[1-9]|[12]\d|3[01])|(?:0?[1-9]|[12]\d|3[01]) (?:января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря) \d{1,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December) (?:0?[1-9]|[12]\d|3[01]), \d{1,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (?:0?[1-9]|[12]\d|3[01]), \d{1,4}|\d{1,4}, (?:January|February|March|April|May|June|July|August|September|October|November|December) (?:0?[1-9]|[12]\d|3[01])|\d{1,4}, (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (?:0?[1-9]|[12]\d|3[01]))$'


PARENTHESIS_REGEXP = r''
SENTENCES_REGEXP = r''
PERSONS_REGEXP = r'(?P<person>[А-ЯЁ][а-яё]+(?:-[А-ЯЁ]?[а-яё]+)?(?:\s[А-ЯЁ][а-яё]+){0,2})'
SERIES_REGEXP = r''

import re

text = """
Нургалиев уволил начальника УВД Томской области.
Начальник УВД Томской области Виктор Гречман освобожден от занимаемой должности.
Как сообщает "Интерфакс" со ссылкой на пресс-службу МВД, это решение принял глава ведомства Рашид Нургалиев по поручению президента РФ Дмитрия Медведева.
"""

pattern = re.compile(PERSONS_REGEXP)
matches = pattern.finditer(text)

for m in matches:
    print(m.group("person"))

