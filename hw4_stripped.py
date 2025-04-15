#!/usr/bin/env python3
import datetime
import unittest
import re


log_pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<dt>[^\]]+)\] "(?P<method>GET|PUT|POST|HEAD|OPTIONS|DELETE) '
    r'(?P<page>\S+) (?P<protocol>[^"]+)" (?P<code>\d{3}) (?P<size>\d+|-) "(?P<referrer>[^"]+)" '
    r'"(?P<agent>[^"]+)"(?: (?P<proc_time>\d+))?'
)


class LogStat:
    def __init__(self):
        self.slowest_page = (None, -1)
        self.fastest_page = (None, float('inf'))
        self.page_times = {}

        self.page_requests = {}
        self.client_requests = {}
        self.browser_requests = {}
        self.client_by_date = {}

    def add_line(self, line):
        words = log_pattern.match(line)
        if not words:
            return

        data = words.groupdict()
        page = data['page']
        ip = data['ip']
        agent = data['agent']

        self.page_requests[page] = self.page_requests.get(page, 0) + 1
        self.client_requests[ip] = self.client_requests.get(ip, 0) + 1
        self.browser_requests[agent] = self.browser_requests.get(agent, 0) + 1

        proc_time = data.get('proc_time')
        if proc_time is None:
            return

        proc_time = int(proc_time)
        if proc_time >= self.slowest_page[1]:
            self.slowest_page = (page, proc_time)
        if proc_time <= self.fastest_page[1]:
            self.fastest_page = (page, proc_time)

        total, count = self.page_times.get(page, (0, 0))
        total += proc_time
        count += 1
        self.page_times[page] = (total, count)

        try:
            dt = datetime.datetime.strptime(data['dt'].split()[0], '%d/%b/%Y:%H:%M:%S')
            day = dt.date()
        except Exception:
            return

        if day not in self.client_by_date:
            self.client_by_date[day] = {}
        self.client_by_date[day][ip] = self.client_by_date[day].get(ip, 0) + 1

    def results(self):
        results = {}
        slowest_average_page = None
        max_average = -1

        for page, (total, count) in self.page_times.items():
            average = total / count
            if average > max_average:
                max_average = average
                slowest_average_page = page

        results["SlowestPage"] = self.slowest_page[0] if self.slowest_page[0] is not None else ''
        results["FastestPage"] = self.fastest_page[0] if self.fastest_page[0] is not None else ''
        results["SlowestAveragePage"] = slowest_average_page if slowest_average_page is not None else ''

        results["MostPopularPage"] = self._choose_by_count(self.page_requests)
        results["MostActiveClient"] = self._choose_by_count(self.client_requests)
        results["MostPopularBrowser"] = self._choose_by_count(self.browser_requests)

        most_active_by_day = {}
        for day, counts in self.client_by_date.items():
            most_active_by_day[day] = self._choose_by_count(counts)
        results["MostActiveClientByDay"] = most_active_by_day

        return results

    @staticmethod
    def _choose_by_count(counts_dictionary):
        if not counts_dictionary:
            return ''

        max_count = max(counts_dictionary.values())
        candidates = [key for key, count in counts_dictionary.items() if count == max_count]

        return min(candidates)


def make_stat():
    return LogStat()


class LogStatTests(unittest.TestCase):
    def test_basic_stats(self):
        log_lines = [
            '192.168.12.155 - - [08/Jul/2012:06:27:46 +0600] "GET /page1 HTTP/1.1" 200 123 "-" "BrowserA" 1000',
            '192.168.12.155 - - [08/Jul/2012:06:27:47 +0600] "GET /page1 HTTP/1.1" 200 123 "-" "BrowserA" 2000',
            '192.168.12.155 - - [08/Jul/2012:06:27:48 +0600] "GET /page2 HTTP/1.1" 200 123 "-" "BrowserB" 500',
            '192.168.12.155 - - [08/Jul/2012:06:27:48 +0600] "GET /page3 HTTP/1.1" 200 123 "-" "BrowserB"'
        ]

        stat = make_stat()
        for line in log_lines:
            stat.add_line(line)
        res = stat.results()

        self.assertEqual(res['SlowestPage'], '/page1')
        self.assertEqual(res['FastestPage'], '/page2')
        self.assertEqual(res['SlowestAveragePage'], '/page1')

        self.assertEqual(res['MostPopularPage'], '/page1')
        self.assertEqual(res['MostActiveClient'], '192.168.12.155')
        self.assertEqual(res['MostPopularBrowser'], 'BrowserA')
        self.assertIn(datetime.date(2012, 7, 8), res['MostActiveClientByDay'])
        self.assertEqual(res['MostActiveClientByDay'][datetime.date(2012, 7, 8)], '192.168.12.155')


if __name__ == '__main__':
    unittest.main()
