from base_advertising import BaseAdvertising
from advertiser import Advertiser
from ad import Ad


if __name__ == '__main__':
    # Error : BaseAdverting is an abstract class and can't initialze.
    # base_advertising = new BaseAdvertising()
    try:
        advertiser1 = Advertiser(1, "name1")
    except AttributeError:
        print("This id is taken.")

    try:
        advertiser2 = Advertiser(2, "name1")
    except AttributeError:
        print("This id is taken.")
    
    # raise an error because this id is already taken by another advertiser.
    try:
        advertiser3 = Advertiser(2, "name3")
    except AttributeError:
        print("This id is taken.")

    ad1 = Ad(1, "title1", "img-url1", "link1", advertiser1)
    ad2 = Ad(2, "title2", "img-url2", "link2", advertiser2)

    print(ad2.describe_me())
    print(advertiser1.describe_me())
    ad1.inc_views()
    ad1.inc_views()
    ad1.inc_views()
    ad1.inc_views()
    ad2.inc_views()
    ad1.inc_clicks()
    ad1.inc_clicks()
    ad2.inc_clicks()
    print(advertiser2.get_name())
    advertiser2.set_name("new name")
    print(advertiser2.get_name())
    print(ad1.get_clicks())
    print(advertiser2.get_clicks())
    print(Advertiser.get_total_clicks())
    print(Advertiser.help())


