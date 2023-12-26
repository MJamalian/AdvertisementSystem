from BaseAdvertising import BaseAdvertising


class Advertiser(BaseAdvertising):
    __total_clicks = 0

    def __init__(self, advertiser_id, name):
        super().__init__()
        self.__id = advertiser_id
        self.__name = name

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def inc_clicks(self):
        super().inc_clicks()
        Advertiser.__total_clicks += 1

    @staticmethod
    def help():
        return ("This class has four field: \n" +
                "id: Unique identifier of the advertiser. \n" +
                "name: Name of the advertiser. \n" +
                "clicks: Number of clicks on ads that are owned by this advertiser. \n" +
                "views: Number of views of ads that are owned by this advertiser.\n")

    def describe_me(self):
        return "This class holds information related to an advertiser."

    @staticmethod
    def get_total_clicks():
        return Advertiser.__total_clicks
