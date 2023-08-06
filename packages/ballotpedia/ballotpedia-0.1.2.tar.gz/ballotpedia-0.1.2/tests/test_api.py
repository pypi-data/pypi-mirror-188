"""Test suite for ballotpedia.api"""
from datetime import date, datetime

import data


def test_districts(fixture_ballotpedia, requests_mock):
    """tests ballotpedia.api.districts"""
    requests_mock.get(
        "https://api4.ballotpedia.org/data/districts/point?lat=40.5550746&long=-74.27596989999999",
        text=data.DISTRICTS_RESP,
    )
    ret = fixture_ballotpedia.districts(lat=40.5550746, lng=-74.27596989999999)
    assert ret["success"]


def test_officeholders(fixture_ballotpedia, requests_mock):
    """tests ballotpedia.api.officeholders"""
    requests_mock.get(
        "https://api4.ballotpedia.org/data/officeholders?long=-89.3818172&lat=43.079896&collections=contact",
        text=data.OFFICEHOLDERS,
    )
    ret = fixture_ballotpedia.officeholders(
        lat=43.079896, lng=-89.3818172, collections="contact"
    )
    assert ret["success"]


def test_election_dates_by_point(fixture_ballotpedia, requests_mock):
    """tests ballotpedia.api.election_dates_by_point"""
    requests_mock.get(
        "https://api4.ballotpedia.org/data/election_dates/point?lat=40.5550746&long=-74.27596989999999",
        text=data.ELECTION_DATES,
    )
    ret = fixture_ballotpedia.election_dates_by_point(
        lat=40.5550746, lng=-74.27596989999999
    )
    assert ret["success"]


def test_election_dates_list(fixture_ballotpedia, requests_mock):
    """tests ballotpedia.api.election_dates_list"""
    # without parameters
    requests_mock.get(
        "https://api4.ballotpedia.org/data/election_dates/list?page=1",
        text=data.ELECTION_DATES_NO_PARAM_PAGE1,
    )

    requests_mock.get(
        "https://api4.ballotpedia.org/data/election_dates/list?page=2",
        text=data.ELECTION_DATES_NO_PARAM_PAGE2,
    )

    iters = 0
    for i in fixture_ballotpedia.election_dates_list():
        d = datetime.strptime(i["date"], "%Y-%m-%d").date()
        assert date(2018, 1, 1) <= d <= date(2018, 1, 31)
        iters += 1
    assert iters == 25

    # with parameters
    requests_mock.get(
        "https://api4.ballotpedia.org/data/election_dates/list?state=WI&type=Special&year=2020&page=1",
        text=data.ELECTION_DATES_PARAMS,
    )
    iters = 0
    for i in fixture_ballotpedia.election_dates_list(
        state="WI", election_type="Special", year=2020
    ):
        assert i["date"] == "2020-05-12"
        iters += 1
    assert iters == 1


def test_elections_by_point(fixture_ballotpedia, requests_mock):
    """tests ballotpedia.api.elections_by_point"""
    requests_mock.get(
        "https://api4.ballotpedia.org/data/elections_by_point?"
        "long=-88.72466949999999&lat=43.194246&election_date=2020-11-03",
        text=data.ELECTIONS_BY_POINT,
    )
    ret = fixture_ballotpedia.elections_by_point(
        lat=43.194246, lng=-88.72466949999999, election_date=date(2020, 11, 3)
    )
    assert ret["success"]


def test_elections_by_state(fixture_ballotpedia, requests_mock):
    """tests ballotpedia.api.elections_by_state"""
    requests_mock.get(
        "https://api4.ballotpedia.org/data/elections_by_state?"
        "state=WI&election_date=2020-11-03&office_level=Federal&page=1",
        text=data.ELECTIONS_BY_STATE,
    )
    requests_mock.get(
        "https://api4.ballotpedia.org/data/elections_by_state?"
        "state=WI&election_date=2020-11-03&office_level=Federal&page=2",
        text=data.ELECTIONS_BY_STATE_PAGE2,
    )
    for i in fixture_ballotpedia.elections_by_state(
        state="WI", election_date=date(2020, 11, 3), office_level="Federal"
    ):
        assert i["name"].startswith("Wisconsin District")
        assert i["type"] == "Congress"

    # When a race is a partisan primary, multiple objects will exist in the races array for the respective political
    # party primary. This is defined as stage_party. This applies to both the By Point and By State endpoints.
    requests_mock.get(
        "https://api4.ballotpedia.org/data/elections_by_state?state=WI&election_date=2020-08-11&page=1",
        text=data.ELECTIONS_BY_STATE_PARTISAN,
    )
    requests_mock.get(
        "https://api4.ballotpedia.org/data/elections_by_state?state=WI&election_date=2020-08-11&page=2",
        text=data.ELECTIONS_BY_STATE_PAGE2,
    )
    for i in fixture_ballotpedia.elections_by_state(
        state="WI", election_date=date(2020, 8, 11)
    ):
        assert i["name"].startswith("Wisconsin District")
        assert i["type"] == "Congress"
        assert not i["ballot_measures"]

    # When a race utilizes Ranked Choice Voting, is_ranked_choice will be true. The ranked_choice_voting_rounds array
    # will be populated with the candidate's round results. The cand_status data point reflects their result at the end
    # of the RCV voting. The votes_for_cand reflects the total number of votes throughout the rounds. This applies to
    # both the By Point and By State endpoints in which the race uitilizes RCV.
    requests_mock.get(
        "https://api4.ballotpedia.org/data/elections_by_state?"
        "state=CA&election_date=2020-08-11&district_type=County+subdivision&page=1",
        text=data.ELECTIONS_BY_STATE_RCV,
    )
    requests_mock.get(
        "https://api4.ballotpedia.org/data/elections_by_state?"
        "state=CA&election_date=2020-08-11&district_type=County+subdivision&page=2",
        text=data.ELECTIONS_BY_STATE_PAGE2,
    )
    for i in fixture_ballotpedia.elections_by_state(
        state="CA", election_date=date(2020, 8, 11), district_type="County subdivision"
    ):
        assert datetime.strptime(i["date"], "%Y-%m-%d") == "2020-08-11"
        assert i["descripton"] == "County subdivision"
        assert i["state"] == "CA"

    requests_mock.get(
        "https://api4.ballotpedia.org/data/elections_by_state?state=MD&election_date=2024-11-05",
        text=data.ELECTIONS_BY_STATE_ERROR,
    )
    assert (
        len(
            list(
                fixture_ballotpedia.elections_by_state(
                    state="MD", election_date=date(2024, 11, 5)
                )
            )
        )
        == 0
    )
