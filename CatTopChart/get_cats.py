import datetime
import json
import os
import string

import requests
import random

SAVE_FOLDER = "api_responses"


# looks bad coz this used to have class structure,
# but it was removed due to inconvenience :(
def __get_headers():
    # This format is for unsplash.com
    return {
        "Accept-Version": "v1"}


def __get_params(query, per_page, page, access_key):
    # This format is for unsplash.com
    return {
        "client_id": access_key,
        "query": query,
        "page": page,
        "per_page": per_page,
        "order_by": "latest",
        "content_filter": "low"
    }


def __get_img_data(response: json):
    # This format is for unsplash.com
    for img_data in response["results"]:
        img_link = img_data["links"]["download"]
        img_id = img_data["id"]
        yield img_id, img_link


def get_images(query, api_url, access_key, per_page, page=1, save=False) -> tuple:
    """returns images links with their id's

    :param page: Page number to retrieve
    :param per_page: number of items per page.
    :param save: if true save api responses in json
    :param access_key: key for API
    :param query: prompt to search image for
    :param api_url: link to API
    :return: tuple of tuples where each inner tuple is (img_id, img_link)
    """
    params = __get_params(query, per_page, page, access_key)

    response = requests.get(f"{api_url}", headers=__get_headers(), params=params)
    response.raise_for_status()  # raise errors if data is absent
    ser_response = response.json()  # also raises JSONDecodeError

    if save:
        target_path = os.path.join(os.getcwd(), SAVE_FOLDER)
        while not os.path.exists(target_path):
            os.mkdir(target_path)
        with open(os.path.join(SAVE_FOLDER, f"api_response {datetime.datetime.now()}.json"), "w") as out_file:
            json.dump(ser_response, out_file)

    return tuple(__get_img_data(ser_response))


# replicates get_images without using API coz requests limit

def get_test_data(count: int) -> tuple:
    """returns fake images links with their id's

    :param count: quantity on images
    :return: tuple of tuples where each inner tuple is (img_id, img_link)
    """

    def img_data():
        letters = string.ascii_lowercase
        for _ in range(count):
            img_id = ''.join(random.choice(letters) for _ in range(7))
            img_link = f"https://unsplash.com/photos/{img_id}/download'"
            yield img_id, img_link

    # yes that is function in function. I was lazy
    return tuple(img_data())
