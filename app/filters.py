import re
import bleach


def mention(content):
    username_ids = mention_username(content)
    if (len(username_ids) > 0):
        for username_id in username_ids:
            if (username_id[0].endswith('.') != True):
                content = content.replace('@' + username_id,
                                          '@<a href="/user/{_}">{_}</a>'.format(_=username_id))
    return content


def mention_username(content):
    usernames = re.findall('(@[a-zA-Z0-9\u4e00-\u9fa5\_]+\.?)\s?', content)
    username_ids = []
    if (len(usernames) > 0):
        username_ids = [re.findall('@([a-zA-Z0-9\u4e00-\u9fa5\_]+\.?)', username)[0] for username in usernames]
    return username_ids


def bleach_html(content):
    allowed_tags = ['a', 'b', 'blockquote', 'code', 'em', 'li', 'ol', 'pre',
                 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'p', 'img']
    allowed_attrs = {'a': ['href', 'rel'],
                     'img': ['src', 'alt']}
    return bleach.linkify(bleach.clean(
        content, tags=allowed_tags, strip=True, attributes=allowed_attrs))
