import unittest
import datetime
import heapq
import re
from typing import Any


def merge(*iterables, key=None):
    if key is None:
        def key(x: Any) -> Any:
            return x

    iters = [iter(it) for it in iterables]
    heap: list[tuple] = []

    for source_index, iterable in enumerate(iters):
        try:
            item = next(iterable)
            heapq.heappush(heap, (key(item), source_index, item, iterable))
        except StopIteration:
            continue

    while heap:
        _, source_index, item, iterable = heapq.heappop(heap)
        yield item
        try:
            nxt = next(iterable)
            heapq.heappush(heap, (key(nxt), source_index, nxt, iterable))
        except StopIteration:
            pass


apache_ts_re = re.compile(r'\[(\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})]')


def log_key(line: str) -> datetime.datetime:
    m = apache_ts_re.search(line)
    if m:
        date = datetime.datetime.strptime(m.group(1), '%d/%b/%Y:%H:%M:%S %z').astimezone(
            datetime.timezone.utc).replace(tzinfo=None)
        return date

    head = line.lstrip().split(None, 2)
    if len(head) >= 2:
        ts = " ".join(head[:2])
    else:
        ts = head[0]

    for pattern in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%d.%m.%Y %H:%M:%S",
            "%Y/%m/%d %H:%M:%S"
    ):
        try:
            return datetime.datetime.strptime(ts, pattern)
        except ValueError:
            continue

    try:
        return datetime.datetime.fromisoformat(ts)
    except ValueError:
        raise ValueError(f"{ts} is not unknown in {line!r}")


class TestTest(unittest.TestCase):
    def test_numeric_merge(self):
        a, b, c = [1, 4, 7], [0, 2, 5, 8], [3, 6, 9]
        self.assertEqual(list(merge(a, b, c)), list(range(10)))

    def test_key_function(self):
        a, b, = ["apple", "banana"], ["Apricot", "blueberry"]
        result = list(merge(a, b, key=str.lower))
        self.assertEqual(result, ["apple", "Apricot", "banana", "blueberry"])

    def test_stable_on_equal_keys(self):
        a, b = [1, 3, 5], [1, 3, 4]
        self.assertEqual(list(merge(a, b)), [1, 1, 3, 3, 4, 5])

    def test_logs_merge(self):
        first = ['2025-05-11 10:00:00 A', '2025-05-11 10:05:00 B']
        second = ['2025-05-11 09:59:59 X', '2025-05-11 10:04:00 Y', '2025-05-11 10:06:00 Z']
        expected = sorted(first + second, key=log_key)
        self.assertEqual(list(merge(first, second, key=log_key)), expected)


if __name__ == '__main__':
    unittest.main()
