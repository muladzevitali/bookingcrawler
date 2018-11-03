from configuration import *


def get_bbox(response):
    hotel_bbox_string = response.xpath('//*[@data-bbox]/@data-bbox').extract()
    for bbox in hotel_bbox_string:
        if bbox:
            return bbox
    return None


def get_number_of_hotels(response):
    _header_string = response.xpath('//*[@class="sr_header--title"]//*[@class="sorth1"]/text()').extract_first()
    _numbers_string = int(list(filter(lambda x: ',' in x, _header_string.split(' ')))[0].replace(',', ''))
    return _numbers_string


def get_clean_result(response, _xpath):
    value = response.xpath(_xpath).extract_first()
    if value:
        return value.strip()
    return None


def get_languages(response):
    languages_list = None

    for div in response.xpath('//*[@id="hp_facilities_box"]/div[4]/div'):
        text = div.xpath('.//h5/text()').extract()
        for each in text:
            if each.strip() == 'Languages spoken':
                languages_list = div.xpath('.//ul//text()').extract()

    if not languages_list:
        return None

    languages = [each.strip() for each in languages_list if each.strip()]
    return ', '.join(languages)


def get_district(response):
    text = response.xpath('.//a[@data-coords]//text()').extract_first()
    if not text:
        return None
    return text.replace('– Show on map', '').strip()


def get_property_type(response):
    text = response.body.decode("utf-8")
    _atnm_index = text.find('atnm')
    _comma_index = text[_atnm_index:].find(',')
    property_type = text[_atnm_index: _atnm_index + _comma_index].split("'")[-2]
    return property_type


def load_cities():
    with open(cities_file, 'r') as _input_file:
        cities = _input_file.readlines()

    cities = [city.strip() for city in cities]

    return cities


def rotate_coordinates(_coordinates):
    if not _coordinates:
        return None
    y, x = _coordinates.strip().split(',')
    return float(x), float(y)


def rotate_bbox(bbox):
    if not bbox:
        return None
    y0, x0, y1, x1 = bbox.strip().split(',')
    return [(x0, y0), (x1, y1)]
