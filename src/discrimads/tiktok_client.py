"""
Tiktok client.
"""

from datetime import date
import json
import pandas as pd
from pydantic import BaseModel, Field, ValidationError
import requests
from typing import Dict, List

from discrimads.util import flatten_ad_dict


TIKTOK_ADS_AVAILABLE_FIELDS = [
    "ad.id",
    "ad.first_shown_date",
    "ad.last_shown_date",
    "ad.status",
    "ad.status_statement",
    "ad.videos",
    "ad.image_urls",
    "ad.reach",
    "advertiser.business_id",
    "advertiser.business_name",
    "advertiser.paid_for_by",
]


TIKTOK_DETAILS_AVAILABLE_FIELDS = TIKTOK_ADS_AVAILABLE_FIELDS + [
    "advertiser.follower_count",
    "advertiser.avatar_url",
    "advertiser.profile_url",
    "ad_group.targeting_info",
]


class TiktokBaseParams(BaseModel):
    region_code: str = Field(
        default="FR", description="Pays de diffusion de la publicité."
    )
    min_date: date = Field(
        ..., description="Date de première impression de la publicité."
    )
    max_date: date = Field(
        ..., description="Date de dernière impression de la publicité."
    )
    with_details: bool = Field(
        default=False, description="True if details are desired for the researched ads."
    )


class TiktokAdvertiserAdsParams(TiktokBaseParams):
    pass


class TiktokSearchAdsParams(TiktokBaseParams):
    pass


class TiktokAdsTransparencyClient():
    """
    Tiktok Ads Transparency client.
    """

    DEFAULT_URL = "https://open.tiktokapis.com/v2/research/adlib/ad/query/?fields={}"
    AD_DETAILS_URL = (
        "https://open.tiktokapis.com/v2/research/adlib/ad/detail/?fields={}"
    )
    AUTH_URL = "https://open.tiktokapis.com/v2/oauth/token/"
    ADVERTISER_URL = (
        "https://open.tiktokapis.com/v2/research/adlib/advertiser/query/?fields={}"
    )
    AUTH_HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
    }
    DETAILS_METHOD_THRESHOLD = 101

    def __init__(self, **kwargs) -> None:
        self._initialize_credentials(**kwargs)

    def _initialize_credentials(self, **kwargs) -> None:
        """
        Initialize Tiktok client with a valid access token.
        """
        client_key = kwargs.get("client_key")
        client_secret = kwargs.get("client_secret")
        if (not client_key) or (not client_secret):
            raise KeyError(
                "Arguments `client_key` and `client_secret` containing a "
                "valid Tiktok credentials are required."
            )
        # Make POST request for token
        data = {
            "client_key": client_key,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }
        auth_reponse = requests.post(
            self.AUTH_URL, headers=self.AUTH_HEADERS, data=data
        )
        # TODO: catch authentication error
        self.access_token = auth_reponse.json()["access_token"]

    def get_advertiser_ids(self, advertiser_name: str, n: int | None = None) -> dict:
        headers = {
            "authorization": f"bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        data = {"search_term": advertiser_name, "max_count": n}

        url = self.ADVERTISER_URL.format(",".join(["business_name", "business_id"]))
        # Query API
        response = requests.post(url, headers=headers, data=json.dumps(data))
        # Get response
        response = response.json()

        # Error message if not successful
        if response["error"]["code"] != "ok":
            # TODO: detail error message
            raise ValueError(
                f"Error response from Tiktok: {response['error']['message']}"
            )

        return response["data"]["advertisers"]

    def get_advertiser_ads(
        self, advertiser_ids: str | List[str], n: int | None = None, **kwargs
    ):
        """
        Get ads from a single or multiple advertisers.
        """
        try:
            params = TiktokAdvertiserAdsParams(**kwargs)
        except ValidationError as e:
            raise ValueError(e)
        # Return ads
        return self._get_ads(
            advertiser_ids=advertiser_ids,
            region_code=params.region_code,
            min_date=params.min_date,
            max_date=params.max_date,
            with_details=params.with_details,
            n=n,
        )

    def search_ads(self, search_terms: str, n: int | None = None, **kwargs):
        """
        Get ads from search terms.
        """
        try:
            params = TiktokSearchAdsParams(**kwargs)
        except ValidationError as e:
            raise ValueError(e)
        # Return ads
        return self._get_ads(
            search_terms=search_terms,
            region_code=params.region_code,
            min_date=params.min_date,
            max_date=params.max_date,
            with_details=params.with_details,
            n=n,
        )

    @staticmethod
    def _get_ads_from_url(
        url: str,
        headers: Dict,
        request_data: Dict,
        n: int | None = None,
    ):
        """
        Get Tiktok ads from a URL along with headers and request data, up to n ads.
        """
        # TODO: remove hard limit
        remaining_ads = n if n is not None else 999999
        while True:
            # Make the POST request
            response = requests.post(
                url, headers=headers, data=json.dumps(request_data)
            )
            # Get response
            response = response.json()

            # Error message if not successful
            if response["error"]["code"] != "ok":
                # TODO: detail error message
                raise ValueError(
                    f"Error response from Tiktok: {response['error']['message']}"
                )

            # Number of ads
            n_ads = len(response["data"]["ads"])
            if n_ads >= remaining_ads:
                yield [
                    flatten_ad_dict(ad)
                    for ad in response["data"]["ads"][:remaining_ads]
                ]
                break
            else:
                yield [flatten_ad_dict(ad) for ad in response["data"]["ads"]]

            # Break if no more results
            if not response["data"]["has_more"]:
                break
            # Update request data and remaining ads
            remaining_ads -= n_ads
            request_data["search_id"] = response["data"]["search_id"]

    @staticmethod
    def _get_ad_details_from_url(
        details_url: str,
        headers: Dict,
        request_data: Dict,
    ):
        """
        Get Tiktok ad details from a URL along with headers and specific request data.
        """
        # Make the POST request
        response = requests.post(
            details_url, headers=headers, data=json.dumps(request_data)
        )
        # Get response
        response = response.json()

        # Error message if not successful
        if response["error"]["code"] != "ok":
            # TODO: detail error message
            raise ValueError(
                f"Error response from Tiktok: {response['error']['message']}"
            )

        return flatten_ad_dict(response["data"])

    def _get_ads(
        self,
        search_terms: str | None = None,
        advertiser_ids: str | List[str] | None = None,
        region_code: str | None = None,
        min_date: date | None = None,
        max_date: date | None = None,
        with_details: bool = False,
        n: int | None = None,
    ):
        """
        Get n Tiktok ads from request parameters.
        """
        headers = {
            "authorization": f"bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        data = self._create_data_dict(
            search_terms=search_terms,
            region_code=region_code,
            advertiser_ids=advertiser_ids,
            min_date=min_date,
            max_date=max_date,
        )

        url = self.DEFAULT_URL.format(",".join(TIKTOK_ADS_AVAILABLE_FIELDS))
        ads = self._get_ads_from_url(url, headers, data, n)
        data = []
        for ads_batch in ads:
            data += list(ads_batch)
        data = pd.DataFrame(data)

        # Without details, return data
        if not with_details:
            return data
        else:
            if n > self.DETAILS_METHOD_THRESHOLD:
                raise ValueError("Number of ads should be smaller to get full details.")

            # Get ad ids
            ad_ids = pd.DataFrame(data)["id"].to_list()
            # Ad details API
            details_url = self.AD_DETAILS_URL.format(
                ",".join(TIKTOK_DETAILS_AVAILABLE_FIELDS)
            )
            details = []
            for ad_id in ad_ids:
                data = {"ad_id": ad_id}
                details.append(
                    self._get_ad_details_from_url(
                        details_url=details_url,
                        headers=headers,
                        request_data=data,
                    )
                )
            return pd.DataFrame(details)

    @staticmethod
    def _create_data_dict(
        search_terms: str | None = None,
        advertiser_ids: str | List[str] | None = None,
        region_code: str | None = None,
        min_date: date | None = None,
        max_date: date | None = None,
    ):
        """
        Create data dictionary for a Titktok request from
        search parameters.
        """
        # Error message if search terms and business ids
        if (search_terms is not None) and (advertiser_ids is not None):
            raise ValueError("Both search terms and advertiser ids are provided.")
        elif (search_terms is None) and (advertiser_ids is None):
            raise ValueError("Either seach terms or advertiser ids must be provided.")
        data = {
            "filters": {
                "country": region_code,
                "ad_published_date_range": {
                    "min": min_date.strftime("%Y%m%d"),
                    "max": max_date.strftime("%Y%m%d"),
                },
            },
            "max_count": 5,  # TODO: tune default value ?
        }

        # Add either search terms or advertiser id
        if advertiser_ids is not None:
            if isinstance(advertiser_ids, str):
                data["filters"]["advertiser_business_ids"] = [int(advertiser_ids)]
            elif isinstance(advertiser_ids, list):
                data["filters"]["advertiser_business_ids"] = [
                    int(advertiser_id) for advertiser_id in advertiser_ids
                ]
            else:
                raise TypeError(
                    "`advertiser_ids` must either be a string or a list of strings."
                )
        else:
            data["search_type"] = (
                "exact_phrase"  # TODO: allow for different search types
            )
            data["search_term"] = search_terms
        return data
