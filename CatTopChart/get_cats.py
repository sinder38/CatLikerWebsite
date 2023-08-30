import requests


class ImageProvider:
    def __init__(self, access_key: str, query="cat"):
        """Initial parameters to work with API

        :param query: search terms
        :param access_key: key to access unsplash.com API
        """
        self.query = query  # what if you require only fat cats

        # different API use varying formats. This format is for unsplash.com
        self.api_url = "https://api.unsplash.com/search/photos"
        self.headers = {"Authorization": access_key}

    def __get_params(self, count):
        # This format is for unsplash.com
        return {
            "query": self.query,
            "page": 1,
            "per_page": count,
            "order_by": "latest",
            "content_filter": "low"
        }

    @staticmethod
    def __get_img_data(response: requests.Response):
        # This format is for unsplash.com
        for img_data in response.json()["results"]:
            img_link = img_data["links"]["download"]
            img_id = img_data["id"]
            yield img_id, img_link

    def get_images(self, count: int) -> tuple:
        """returns images links with their id's

        :param count: quantity on images
        :return: tuple of tuples where each inner tuple is (img_id, img_link)
        """
        params = self.__get_params(count)
        response = requests.get(self.api_url, headers=self.headers, params=params)
        response.raise_for_status()  # raise errors if data is absent
        return tuple(self.__get_img_data(response))


if __name__ == "__main__":
    sample_access_key = ""
    if sample_access_key:
        img_provider = ImageProvider(sample_access_key)
        data = img_provider.get_images(2)
        print("sample data:", data)
