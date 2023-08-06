"""
Python interface to the Ballotpedia API (https://developer.ballotpedia.org/)

Please note that in order to hit the following endpoints from an application on the internet, you must contact the
Ballotpedia team to whitelist the domains from which those requests will originate. Requests from non-whitelisted origin
domains will receive a preflight CORS permissions error. You are free to run test requests locally or in a non-cors
context such as cURL, Postman, etc.
"""
from datetime import date
from typing import Dict, Iterator, Literal, Optional

import requests

from .api_types import (
    ElectionDates,
    ElectionLocation,
    ElectionStates,
    Location,
    OfficeHolders,
)

_COLLECTIONS_TYPES = Literal["social", "contact"]
_ELECTION_TYPES = Literal["General", "Primary", "Special", "Recall"]
_OFFICE_TYPES = Literal["Federal", "State", "Local"]
_OFFICE_BRANCH_TYPES = Literal["Legislative", "Executive", "Judicial"]
_DISTRICT_TYPES = Literal[
    "Country",
    "Congress",
    "State",
    "State Legislative (Upper)",
    "State Legislative (Lower)",
    "Judicial District",
    "County",
    "County subdivision",
    "City-town",
    "School District",
    "State subdivision",
    "Special district subdivision",
    "Judicial district subdivision",
    "Special District",
    "City-town subdivision",
    "School district subdivision",
]


class Ballotpedia:
    def __init__(self, api_key):
        self.headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    def districts(self, lat: float, lng: float) -> Dict:
        """
        Given a latitude and longitude point, a list of voting districts will be returned in which that point (address)
        lies.

        :param lat: latitude to search for current office holders
        :param lng: longitude to search for current office holders
        """
        payload: Location = {
            "lat": lat,
            "long": lng,
        }

        return requests.get(
            "https://api4.ballotpedia.org/data/districts/point",
            params=payload,  # type: ignore
            headers=self.headers,
        ).json()

    def officeholders(
        self, lat: float, lng: float, collections: Optional[_COLLECTIONS_TYPES] = None
    ) -> Dict:
        """
        Given a latitude and longitude point, a list of current officeholders representing the point (address) will be
        returned with accompanying information and data points on the district, office, officeholder and person.

        :param lat: latitude to search for current office holders
        :param lng: longitude to search for current office holders
        :param collections: type of collection to search (social,contact)
        """
        payload: OfficeHolders = {
            "lat": lat,
            "long": lng,
            "collections": collections if collections else None,
        }

        return requests.get(
            "https://api4.ballotpedia.org/data/officeholders",
            params=payload,  # type: ignore
            headers=self.headers,
        ).json()

    def election_dates_by_point(self, lat: float, lng: float) -> Dict:
        """
        Given a latitude and longitude point, a list of election dates will be returned for the particular point
        (address) that have occurred 1 year in the past and will occur 1 year in the future according to today's date.

        :param lat: latitude to search for current office holders
        :param lng: longitude to search for current office holders
        """
        payload: Location = {
            "lat": lat,
            "long": lng,
        }

        return requests.get(
            "https://api4.ballotpedia.org/data/election_dates/point",
            params=payload,  # type: ignore
            headers=self.headers,
        ).json()

    def election_dates_list(
        self,
        state: Optional[str] = None,
        election_type: Optional[_ELECTION_TYPES] = None,
        year: Optional[int] = None,
    ) -> Iterator[Dict]:
        """
        Election dates can be queried via several parameters which will return data from 2018+ and several years into
        the future. Data is returned in an ascending matter according to date, with limits of 25 results per page.

        :param state: abbreviated state to search
        :param election_type: election type to search (General,Primary,Special,Recall)
        :param year: election year to search
        """
        payload: ElectionDates = {
            "state": state if state else None,
            "type": election_type if election_type else None,
            "year": year if year else None,
            "page": None,
        }

        page_iter = 1

        while True:
            payload["page"] = page_iter
            ret = requests.get(
                "https://api4.ballotpedia.org/data/election_dates/list",
                params=payload,  # type: ignore
                headers=self.headers,
            ).json()

            if ret.get("data", {}).get("elections", None) is None:
                break

            for i in ret.get("data", {}).get("elections"):
                yield i
            page_iter += 1

    def elections_by_point(
        self,
        lat: float,
        lng: float,
        election_date: date,
        collections: Optional[_COLLECTIONS_TYPES] = None,
    ) -> Dict:
        """
        Given a latitude and longitude point and an election date, a list of candidates, ballot measures and races will
        be returned along with district, office, and person information for the particular point.

        Results of the election will be returned if included in your API package. Including which candidates won/lost,
        vote totals, and which ballot measures were approved or defeated.

        :param lat: latitude to search for current office holders
        :param lng: longitude to search for current office holders
        :param election_date: date of the election
        :param collections: type of collection to search (social,contact)
        """
        payload: ElectionLocation = {
            "lat": lat,
            "long": lng,
            "election_date": election_date.strftime("%Y-%m-%d"),
            "collections": collections if collections else None,
        }

        return requests.get(
            "https://api4.ballotpedia.org/data/elections_by_point",
            params=payload,  # type: ignore
            headers=self.headers,
        ).json()

    def elections_by_state(
        self,
        state: str,
        election_date: date,
        collections: Optional[_COLLECTIONS_TYPES] = None,
        office_level: Optional[_OFFICE_TYPES] = None,
        office_branch: Optional[_OFFICE_BRANCH_TYPES] = None,
        district_type: Optional[_DISTRICT_TYPES] = None,
    ):
        """
        Given a state and an election date, a list of candidates, ballot measures and races will be returned along with
        district, office, and person information for the entire state.

        Results of the election will be returned if included in your API package. Including which candidates won/lost,
        vote totals, and which ballot measures were approved or defeated.

        :param state: abbreviated state to search
        :param election_date: date of the election
        :param collections: type of collection to search (social,contact)
        :param office_level: the office level to search (federal, state, local)
        :param office_branch: the office branch to search (legislative, executive, judicial)
        :param district_type: district type to search (Country,Congress,State,State Legislative (Upper),
        State Legislative (Lower),Judicial District,County,County subdivision,City-town,School District,
        State subdivision,Special district subdivision,Judicial district subdivision,Special District,
        City-town subdivision,School district subdivision)
        """
        payload: ElectionStates = {
            "state": state,
            "election_date": election_date.strftime("%Y-%m-%d"),
            "collections": collections if collections else None,
            "office_level": office_level if office_level else None,
            "office_branch": office_branch if office_branch else None,
            "district_type": district_type if district_type else None,
            "page": None,
        }

        page_iter = 1
        while True:
            payload["page"] = page_iter

            ret = requests.get(
                "https://api4.ballotpedia.org/data/elections_by_state",
                params=payload,  # type: ignore
                headers=self.headers,
            ).json()
            if ret.get("data", "No results.") == "No results." or not ret.get(
                "data", {}
            ):
                break
            for i in ret.get("data", {}).get("districts"):
                yield i
            page_iter += 1
