"""Sample ads from tiktok ads repository."""
import os
from discrimads.tiktok_client import TiktokAdsTransparencyClient


def sample_from_tiktok(advertiser_name: str):
    client_key = os.environ["KEY"]
    client_secret = os.environ["SECRET"]
    client = TiktokAdsTransparencyClient(client_key=client_key, client_secret=client_secret)
    advertiser_ids = client.get_advertiser_ids(advertiser_name=advertiser_name)
    advertiser_ids = [str(d["business_id"]) for d in advertiser_ids]

    min_date = "2024-10-01"
    max_date = "2025-02-01"
    ads = client.get_advertiser_ads(
        advertiser_ids=advertiser_ids,
        n=100,
        region_code="FR",
        min_date=min_date,
        max_date=max_date,
        with_details=True,
    )
    ads.to_parquet("data/tiktok_sample.parquet")
    print(f"Extraction of {len(ads)} terminated.")


if __name__ == "__main__":
    sample_from_tiktok("INDEED UK OPERATIONS LIMITED")
