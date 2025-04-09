import sys
import re
import collections
import urllib.parse


try:
    import httpx
except ModuleNotFoundError:
    print("Module httpx not found. Download it: pip install httpx", file=sys.stderr)
    sys.exit(1)

base_url = "https://ru.wikipedia.org/wiki/"
target = "Философия"
headers = {'User-Agent': 'MyWikipediaPhilosophyBot/1.0 (Testing; myemail@example.com)'}
request_timeout = 10
link_regex = re.compile(
    r'<a\s+href\s*=\s*(["\'])/wiki/([^:#"\']+)\1',
    re.IGNORECASE
)

end_content_ids = [
    'id="См._также"', 'id="Примечания"', 'id="Литература"', 'id="Ссылки"',
    'id="catlinks"', 'id="See_also"', 'id="Notes"', 'id="References"',
    'id="External_links"'
]


def get_content(name):
    url_name = urllib.parse.quote(name.replace(' ', '_'))
    url = base_url + url_name
    try:
        with httpx.Client(follow_redirects=True, timeout=request_timeout, headers=headers) as client:
            response = client.get(url)
            if not response.url.path.startswith('/wiki/'):
                return None
            response.raise_for_status()
            return response.text
    except httpx.RequestError:
        return None
    except httpx.HTTPStatusError:
        return None
    except Exception:
        return None


def extract_content(page):
    content_start_marker = '<div id="mw-content-text"'
    start_div_pos = page.find(content_start_marker)

    if start_div_pos == -1:
        content_start_marker = '<div id="bodyContent"'
        start_div_pos = page.find(content_start_marker)
        if start_div_pos == -1:
            return 0, 0

    start_tag_end_pos = page.find('>', start_div_pos)
    if start_tag_end_pos == -1:
        return 0, 0

    begin_content = start_tag_end_pos + 1
    earliest_end_marker_pos = len(page)

    for marker_id_str in end_content_ids:
        for quote in ['"', "'"]:
            try:
                id_value = marker_id_str.split('=', 1)[1].strip(quote)
                if not id_value:
                    continue
            except IndexError:
                continue

            full_marker = f'id={quote}{id_value}{quote}'
            marker_pos = page.find(full_marker, begin_content)

            if marker_pos != -1:
                possible_h_tag_starts = [page.rfind(f'<h{i}', begin_content, marker_pos) for i in range(1, 7)]
                tag_start_h = max((pos for pos in possible_h_tag_starts if pos != -1), default=-1)
                tag_start_div = -1

                if 'catlinks' in id_value:
                    tag_start_div = page.rfind('<div', begin_content, marker_pos)

                tag_start = -1
                if tag_start_h != -1 and tag_start_div != -1:
                    tag_start = max(tag_start_h, tag_start_div)
                elif tag_start_h != -1:
                    tag_start = tag_start_h
                elif tag_start_div != -1:
                    tag_start = tag_start_div
                if tag_start != -1:
                    earliest_end_marker_pos = min(earliest_end_marker_pos, tag_start)

    end_content = earliest_end_marker_pos
    printfooter_pos = page.find('<div class="printfooter">', begin_content)

    if printfooter_pos != -1:
        end_content = min(end_content, printfooter_pos)

    if begin_content >= end_content:
        end_content = len(page)
        if begin_content >= end_content:
            return 0, 0

    return begin_content, end_content


def extract_links(page, begin, end):
    if begin >= end or begin >= len(page):
        return []

    safe_end = min(end, len(page))
    content_slice = page[begin:safe_end]
    links = set()

    for match in link_regex.finditer(content_slice):
        try:
            encoded_title = match.group(2)
            article_title = urllib.parse.unquote(encoded_title)

            if '<' not in article_title and '>' not in article_title:
                links.add(article_title)
        except Exception:
            continue

    return list(links)


def find_chain(start, finish):
    if start == finish:
        return [start]

    queue = collections.deque([[start]])
    visited = {start}
    while queue:
        current_path = queue.popleft()
        current_article = current_path[-1]

        page_content = get_content(current_article)
        if page_content is None:
            continue

        begin, end = extract_content(page_content)
        if begin == 0 and end == 0 and len(page_content) > 0:
            continue

        links = extract_links(page_content, begin, end)
        for link_article in links:
            link_article = link_article.strip()
            if not link_article:
                continue

            if link_article == finish:
                return current_path + [finish]

            if link_article not in visited:
                visited.add(link_article)
                new_path = current_path + [link_article]
                queue.append(new_path)

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py \"name of the article\"", file=sys.stderr)
        sys.exit(1)

    start_article = sys.argv[1]
    path = find_chain(start_article, target)

    if path:
        for article in path:
            print(article)


if __name__ == '__main__':
    main()
