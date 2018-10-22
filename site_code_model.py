def SITENAME(): # EDIT - SITENAME
    data = []
    urls__ = []
    pages = 100 # EDIT -  Set max of pages
    count_url = 0
    for page_number in range(1, pages+1):
        print('')
        print(page_number, '/', pages, '  [', count_url, '/', MAX_URLS_SITE, ']', end='')

        url_ = # EDIT - URL with a list of articles

        try:
            soup_ = get_soup(url_)
            if type(soup_) == str:
                print('timeout', end='')
                continue
        except:
            print("Error urlopen.", url_)
            continue
        soup_.prettify('utf-8')
        links = # EDIT - Get article URL bey soup_
        for anchor in links:
            url = # EDIT - get url . usually anchor['href'] 
            if url in urls__:
                continue
            urls__.append(url)
            soup = get_soup(url, timeout=5)
            if type(soup) == type(''):
                print('timeout', end='')
                continue
            count_url += 1
            if count_url > MAX_URLS_SITE:
                return data
            print('.', end='')
            soup.prettify("utf-8")
            data_ = []
            dic_ = {'claim': 0, 'credibility': 0, 'body': 0, 'date': 0, 'title': 0}
            SITENAME_walk_html(soup, data_, 'SITENAME', url, 0, dic_=dic_) # EDIT - SITENAME
            if dic_['claim'] and dic_['credibility'] and dic_['body']:
                data += data_
            else:
                count_url -= 1
    if count_url < MAX_URLS_SITE:
        print('Warning:', count_url, 'URLS was include')
    return data

def SITENAME_walk_html(element, data, site, url, level, parent=None, brothers=[], dic_=None):
    features = {}
    if element is None:
        return
    features['site'] = site
    features['url'] = url
    features['tag'] = element.name
    features['attrs'] = validate_text_dict(element.attrs)
    features['level'] = level
    features['text'] = validate_text(element.text, level)

    if brothers:
        features['brother_tag'] = brothers[-1]['tag']
        features['brother_attrs'] = brothers[-1]['attrs']
        features['brother_text'] = brothers[-1]['text']
    else:
        features['brother_tag'] = ''
        features['brother_attrs'] = {}
        features['brother_text'] = 'NONE'

    # Title
    if (features['tag'] == 'title' or ()): # EDIT - Title
        features['label'] = 'Title'
        dic_['title'] += 1

    # Date
    elif (): # EDIT - Date
        features['label'] = 'Date'
        dic_['date'] += 1

    # Body
    elif (): # EDIT - Body
        features['label'] = 'Body'
        dic_['body'] += 1

    # Claim
    elif (): # EDIT - Claim
        features['label'] = 'Claim'
        dic_['claim'] += 1

    # Credibility
    elif (): # EDIT - Credibility
        features['label'] = 'Credibility'
        dic_['credibility'] += 1

    # None
    else:
        features['label'] = 'None'

    data.append(features)
    brothers_ = []
    for e_child in element:
        if (type(e_child) == bs4.element.NavigableString or
            type(e_child) == bs4.element.Comment or
            type(e_child) == bs4.element.Doctype or
            type(e_child) == str or e_child.name in ignore_html_tags):
                continue
        brothers_.append(SITENAME_walk_html(e_child, data, site, url, level+1, parent=features, brothers=brothers_, dic_=dic_)) # EDIT - SITENAME
    return features
