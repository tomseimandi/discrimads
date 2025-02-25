"""Sample ads from tiktok ads repository."""
from getpass import getpass
from discrimads.tiktok_client import TiktokAdsTransparencyClient


def sample_from_tiktok(advertiser_name: str):
    client_key = input()
    client_secret = getpass()
    client = TiktokAdsTransparencyClient(client_key=client_key, client_secret=client_secret)
    advertiser_id = client.get_advertiser_ids(advertiser_name=advertiser_name)
    print(advertiser_id)


if __name__ == "__main__":
    sample_from_tiktok("indeed")
