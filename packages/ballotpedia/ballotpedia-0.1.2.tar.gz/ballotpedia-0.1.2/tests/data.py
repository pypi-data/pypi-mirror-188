"""Mocking constants for testing"""
# flake8: noqa
DISTRICTS_RESP = """{
    "success": true,
    "data": [
        {
            "id": "249",
            "name": "New Jersey District 6",
            "type": "Congress",
            "url": "https://ballotpedia.org/New_Jersey%27s_6th_Congressional_District",
            "ocdid": "ocd-division/country:us/state:nj/cd:6",
            "nces_id": null,
            "geo_id": "5001600US3406",
            "state": "NJ",
            "end_date": null
        },
        {
            "id": "542",
            "name": "New Jersey",
            "type": "State",
            "url": "https://ballotpedia.org/New_Jersey",
            "ocdid": "ocd-division/country:us/state:nj",
            "nces_id": null,
            "geo_id": "0400000US34",
            "state": "NJ",
            "end_date": null
        },
        {
            "id": "1794",
            "name": "New Jersey State Senate District 19",
            "type": "State Legislative (Upper)",
            "url": "https://ballotpedia.org/New_Jersey_State_Senate_District_19",
            "ocdid": "ocd-division/country:us/state:nj/sldu:19",
            "nces_id": null,
            "geo_id": "610U600US34019",
            "state": "NJ",
            "end_date": null
        },
        {
            "id": "5625",
            "name": "New Jersey General Assembly District 19",
            "type": "State Legislative (Lower)",
            "url": "https://ballotpedia.org/New_Jersey_General_Assembly_District_19",
            "ocdid": "ocd-division/country:us/state:nj/sldl:19",
            "nces_id": null,
            "geo_id": "620L600US34019",
            "state": "NJ",
            "end_date": null
        },
        {
            "id": "93743",
            "name": "United States",
            "type": "Country",
            "url": "https://ballotpedia.org/Federal_Politics",
            "ocdid": "ocd-division/country:us",
            "nces_id": null,
            "geo_id": "0100000US",
            "state": "US",
            "end_date": null
        }
    ],
    "message": null
}"""

OFFICEHOLDERS = """{
    "success": true,
    "data": [
        {
            "elected_officials": {
                "districts": [
                    {
                        "name": "Wisconsin District 2",
                        "id": 430,
                        "type": "Congress",
                        "state": "WI",
                        "offices": [
                            {
                                "id": 10859,
                                "name": "U.S. House Wisconsin District 2",
                                "type": "Representative",
                                "level": "Federal",
                                "branch": "Legislative",
                                "officeholders": [
                                    {
                                        "id": 37193,
                                        "status": "Current",
                                        "name": "Mark Pocan",
                                        "last_name": "Pocan",
                                        "url": "https://ballotpedia.org/Mark_Pocan",
                                        "partisan_affiliation": 2,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "202-225-2906",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://pocan.house.gov/",
                                                "contact_type": "Website"
                                            }
                                        ],
                                        "person_contact_information": null
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Wisconsin",
                        "id": 562,
                        "type": "State",
                        "state": "WI",
                        "offices": [
                            {
                                "id": 401,
                                "name": "Governor of Wisconsin",
                                "type": "Governor",
                                "level": "State",
                                "branch": "Executive",
                                "officeholders": [
                                    {
                                        "id": 56270,
                                        "status": "Current",
                                        "name": "Tony Evers",
                                        "last_name": "Evers",
                                        "url": "https://ballotpedia.org/Tony_Evers",
                                        "partisan_affiliation": 2,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "https://evers.wi.gov/pages/home.aspx",
                                                "contact_type": "Website"
                                            },
                                            {
                                                "contact": "eversinfo@wisconsin.gov",
                                                "contact_type": "Email"
                                            },
                                            {
                                                "contact": "608-266-1212",
                                                "contact_type": "Phone"
                                            }
                                        ],
                                        "person_contact_information": null
                                    }
                                ]
                            },
                            {
                                "id": 9723,
                                "name": "Attorney General of Wisconsin",
                                "type": "Attorney General",
                                "level": "State",
                                "branch": "Executive",
                                "officeholders": [
                                    {
                                        "id": 294103,
                                        "status": "Current",
                                        "name": "Josh Kaul",
                                        "last_name": "Kaul",
                                        "url": "https://ballotpedia.org/Josh_Kaul",
                                        "partisan_affiliation": 2,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "https://www.doj.state.wi.us/exec-profile/josh-kaul",
                                                "contact_type": "Website"
                                            },
                                            {
                                                "contact": "Josh.Kaul@doj.state.wi.us",
                                                "contact_type": "Email"
                                            },
                                            {
                                                "contact": "608-266-1221",
                                                "contact_type": "Phone"
                                            }
                                        ],
                                        "person_contact_information": null
                                    }
                                ]
                            },
                            {
                                "id": 11813,
                                "name": "U.S. Senate Wisconsin",
                                "type": "Senator",
                                "level": "Federal",
                                "branch": "Legislative",
                                "officeholders": [
                                    {
                                        "id": 53821,
                                        "status": "Current",
                                        "name": "Tammy Baldwin",
                                        "last_name": "Baldwin",
                                        "url": "https://ballotpedia.org/Tammy_Baldwin",
                                        "partisan_affiliation": 2,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "202-224-5653",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://www.baldwin.senate.gov/",
                                                "contact_type": "Website"
                                            }
                                        ],
                                        "person_contact_information": null
                                    },
                                    {
                                        "id": 48568,
                                        "status": "Current",
                                        "name": "Ronald Harold Johnson",
                                        "last_name": "Johnson",
                                        "url": "https://ballotpedia.org/Ron_Johnson_(Wisconsin)",
                                        "partisan_affiliation": 1,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "ron_johnson@ronjohnson.senate.gov",
                                                "contact_type": "Email"
                                            },
                                            {
                                                "contact": "202-224-5323",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://www.ronjohnson.senate.gov/public/",
                                                "contact_type": "Website"
                                            }
                                        ],
                                        "person_contact_information": null
                                    }
                                ]
                            },
                            {
                                "id": 21638,
                                "name": "Wisconsin Secretary of State",
                                "type": "Secretary of State",
                                "level": "State",
                                "branch": "Executive",
                                "officeholders": [
                                    {
                                        "id": 15676,
                                        "status": "Current",
                                        "name": "Douglas J. La Follette",
                                        "last_name": "Follette",
                                        "url": "https://ballotpedia.org/Douglas_La_Follette",
                                        "partisan_affiliation": 2,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "statesec@wi.gov",
                                                "contact_type": "Email"
                                            },
                                            {
                                                "contact": "608-266-8888",
                                                "contact_type": "Phone"
                                            }
                                        ],
                                        "person_contact_information": null
                                    }
                                ]
                            },
                            {
                                "id": 14513,
                                "name": "Lieutenant Governor of Wisconsin",
                                "type": "Lieutenant Governor",
                                "level": "State",
                                "branch": "Executive",
                                "officeholders": [
                                    {
                                        "id": 36064,
                                        "status": "Current",
                                        "name": "Mandela Barnes",
                                        "last_name": "Barnes",
                                        "url": "https://ballotpedia.org/Mandela_Barnes",
                                        "partisan_affiliation": 2,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "https://evers.wi.gov/ltgov/Pages/About_LG.aspx",
                                                "contact_type": "Website"
                                            },
                                            {
                                                "contact": "ltgovernor@wisconsin.gov",
                                                "contact_type": "Email"
                                            },
                                            {
                                                "contact": "608-266-3516",
                                                "contact_type": "Phone"
                                            }
                                        ],
                                        "person_contact_information": null
                                    }
                                ]
                            },
                            {
                                "id": 20865,
                                "name": "Wisconsin Superintendent of Public Instruction",
                                "type": "Superintendent of Schools",
                                "level": "State",
                                "branch": "Executive",
                                "officeholders": [
                                    {
                                        "id": 335652,
                                        "status": "Current",
                                        "name": "Jill Underly",
                                        "last_name": "Underly",
                                        "url": "https://ballotpedia.org/Jill_Underly",
                                        "partisan_affiliation": 7,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "608-520-0547",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://dpi-transition.wi.gov/Pages/About.aspx",
                                                "contact_type": "Website"
                                            },
                                            {
                                                "contact": "dpiinfo@dpi-transition.wi.gov",
                                                "contact_type": "Email"
                                            }
                                        ],
                                        "person_contact_information": [
                                            {
                                                "contact": "underlyforwisconsin@gmail.com",
                                                "contact_type": "Email"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "id": 23727,
                                "name": "Greenfield City Council District 4",
                                "type": null,
                                "level": "Local",
                                "branch": "Legislative",
                                "officeholders": null
                            },
                            {
                                "id": 32705,
                                "name": "Milwaukee County Clerk of the Circuit Court",
                                "type": null,
                                "level": "Local",
                                "branch": "Executive",
                                "officeholders": null
                            },
                            {
                                "id": 10347,
                                "name": "Wisconsin Supreme Court",
                                "type": "Judge of court of last resort",
                                "level": "State",
                                "branch": "Judicial",
                                "officeholders": [
                                    {
                                        "id": 60167,
                                        "status": "Current",
                                        "name": "Ann Walsh Bradley",
                                        "last_name": "Bradley",
                                        "url": "https://ballotpedia.org/Ann_Walsh_Bradley",
                                        "partisan_affiliation": 7,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "608-266-1886",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://wicourts.gov/courts/supreme/justices/bradley.htm",
                                                "contact_type": "Website"
                                            }
                                        ],
                                        "person_contact_information": null
                                    },
                                    {
                                        "id": 85877,
                                        "status": "Current",
                                        "name": "Rebecca Bradley",
                                        "last_name": "Bradley",
                                        "url": "https://ballotpedia.org/Rebecca_Bradley",
                                        "partisan_affiliation": 7,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "608-266-1883",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://wicourts.gov/courts/supreme/justices/rbradley.htm",
                                                "contact_type": "Website"
                                            }
                                        ],
                                        "person_contact_information": null
                                    },
                                    {
                                        "id": 293943,
                                        "status": "Current",
                                        "name": "Rebecca Dallet",
                                        "last_name": "Dallet",
                                        "url": "https://ballotpedia.org/Rebecca_Dallet",
                                        "partisan_affiliation": 7,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "608-266-1884",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://wicourts.gov/courts/supreme/justices/dallet.htm",
                                                "contact_type": "Website"
                                            }
                                        ],
                                        "person_contact_information": null
                                    },
                                    {
                                        "id": 61839,
                                        "status": "Current",
                                        "name": "Brian Hagedorn",
                                        "last_name": "Hagedorn",
                                        "url": "https://ballotpedia.org/Brian_Hagedorn",
                                        "partisan_affiliation": 7,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "608-266-1885",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://wicourts.gov/courts/supreme/justices/hagedorn.htm",
                                                "contact_type": "Website"
                                            }
                                        ],
                                        "person_contact_information": null
                                    },
                                    {
                                        "id": 96029,
                                        "status": "Current",
                                        "name": "Jill Karofsky",
                                        "last_name": "Karofsky",
                                        "url": "https://ballotpedia.org/Jill_Karofsky",
                                        "partisan_affiliation": 7,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "608-266-1882",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://www.wicourts.gov/courts/supreme/justices/karofsky.htm",
                                                "contact_type": "Website"
                                            }
                                        ],
                                        "person_contact_information": null
                                    },
                                    {
                                        "id": 84124,
                                        "status": "Current",
                                        "name": "Patience Drake Roggensack",
                                        "last_name": "Roggensack",
                                        "url": "https://ballotpedia.org/Patience_Roggensack",
                                        "partisan_affiliation": 7,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "608-266-1888",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://wicourts.gov/courts/supreme/justices/roggensack.htm",
                                                "contact_type": "Website"
                                            }
                                        ],
                                        "person_contact_information": null
                                    },
                                    {
                                        "id": 60263,
                                        "status": "Current",
                                        "name": "Annette Ziegler",
                                        "last_name": "Ziegler",
                                        "url": "https://ballotpedia.org/Annette_Ziegler",
                                        "partisan_affiliation": 7,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "annette.ziegler@wicourts.gov",
                                                "contact_type": "Email"
                                            },
                                            {
                                                "contact": "608-266-1881",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://wicourts.gov/courts/supreme/justices/ziegler.htm",
                                                "contact_type": "Website"
                                            }
                                        ],
                                        "person_contact_information": null
                                    }
                                ]
                            },
                            {
                                "id": 7210,
                                "name": "Wisconsin Treasurer",
                                "type": "Treasurer",
                                "level": "State",
                                "branch": "Executive",
                                "officeholders": [
                                    {
                                        "id": 298061,
                                        "status": "Current",
                                        "name": "Sarah Godlewski",
                                        "last_name": "Godlewski",
                                        "url": "https://ballotpedia.org/Sarah_Godlewski",
                                        "partisan_affiliation": 2,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "https://statetreasurer.wi.gov/Pages/About-Sarah.aspx",
                                                "contact_type": "Website"
                                            },
                                            {
                                                "contact": "608-266-1714",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "Treasurer@wisconsin.gov",
                                                "contact_type": "Email"
                                            }
                                        ],
                                        "person_contact_information": null
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Wisconsin State Senate District 26",
                        "id": 2452,
                        "type": "State Legislative (Upper)",
                        "state": "WI",
                        "offices": [
                            {
                                "id": 28870,
                                "name": "Wisconsin State Senate District 26",
                                "type": "Senator",
                                "level": "State",
                                "branch": "Legislative",
                                "officeholders": [
                                    {
                                        "id": 31647,
                                        "status": "Current",
                                        "name": "Kelda Roys",
                                        "last_name": "Roys",
                                        "url": "https://ballotpedia.org/Kelda_Roys",
                                        "partisan_affiliation": 2,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "608-266-1627",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://docs.legis.wisconsin.gov/2021/legislators/senate/2252",
                                                "contact_type": "Website"
                                            },
                                            {
                                                "contact": "sen.roys@legis.wisconsin.gov",
                                                "contact_type": "Email"
                                            }
                                        ],
                                        "person_contact_information": null
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Wisconsin State Assembly District 76",
                        "id": 7302,
                        "type": "State Legislative (Lower)",
                        "state": "WI",
                        "offices": [
                            {
                                "id": 11319,
                                "name": "Wisconsin State Assembly District 76",
                                "type": "Representative",
                                "level": "State",
                                "branch": "Legislative",
                                "officeholders": [
                                    {
                                        "id": 330225,
                                        "status": "Current",
                                        "name": "Francesca Hong",
                                        "last_name": "Hong",
                                        "url": "https://ballotpedia.org/Francesca_Hong",
                                        "partisan_affiliation": 2,
                                        "officeholder_contact_information": [
                                            {
                                                "contact": "608-266-5342",
                                                "contact_type": "Phone"
                                            },
                                            {
                                                "contact": "https://docs.legis.wisconsin.gov/2021/legislators/assembly/2261",
                                                "contact_type": "Website"
                                            },
                                            {
                                                "contact": "rep.hong@legis.wisconsin.gov",
                                                "contact_type": "Email"
                                            }
                                        ],
                                        "person_contact_information": null
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "name": "Dane",
                        "id": 13889,
                        "type": "County",
                        "state": "WI",
                        "offices": null
                    },
                    {
                        "name": "Madison Metropolitan School District",
                        "id": 28168,
                        "type": "School District",
                        "state": "WI",
                        "offices": null
                    },
                    {
                        "name": "Wisconsin Court of Appeals District IV",
                        "id": 63613,
                        "type": "Judicial District",
                        "state": "WI",
                        "offices": null
                    },
                    {
                        "name": "Dane County Circuit Court, Wisconsin",
                        "id": 63626,
                        "type": "Judicial District",
                        "state": "WI",
                        "offices": null
                    },
                    {
                        "name": "Madison",
                        "id": 92584,
                        "type": "City-town",
                        "state": "WI",
                        "offices": null
                    },
                    {
                        "name": "Madison City Council District 2",
                        "id": 95104,
                        "type": "City-town subdivision",
                        "state": "WI",
                        "offices": null
                    },
                    {
                        "name": "Dane County Supervisor District 2",
                        "id": 95124,
                        "type": "County subdivision",
                        "state": "WI",
                        "offices": null
                    },
                    {
                        "name": "Sanders County Sewer District at Paradise",
                        "id": 99105,
                        "type": "Special district subdivision",
                        "state": null,
                        "offices": null
                    }
                ]
            }
        }
    ],
    "message": null
}"""

ELECTION_DATES = """        {
            "success": true,
            "data": {
                "elections": [
                    {
                        "type": "General",
                        "id": 18742,
                        "date": "2020-11-03",
                        "description": null
                    },
                    {
                        "type": "General",
                        "id": 18775,
                        "date": "2020-11-03",
                        "description": "U.S. Presidential election"
                    },
                    {
                        "type": "General",
                        "id": 22516,
                        "date": "2021-11-02",
                        "description": null
                    }
                ]
            },
            "message": null
        }
    """

ELECTION_DATES_NO_PARAM_PAGE1 = """    {
        "success": true,
        "data": {
            "elections": [
                {
                    "date": "2018-01-02",
                    "type": "General",
                    "description": "Special election",
                    "candidate_lists_complete": true,
                    "state": "SC"
                },
                {
                    "date": "2018-01-02",
                    "type": "Recall",
                    "description": "https://ballotpedia.org/Andrew_Hamilton_recall,_Lake_Forest,_Ca",
                    "candidate_lists_complete": true,
                    "state": "CA"
                },
                {
                    "date": "2018-01-09",
                    "type": "Recall",
                    "description": "https://ballotpedia.org/Larry_Thomas_recall,_Washburn_City_Comm",
                    "candidate_lists_complete": true,
                    "state": "ND"
                },
                {
                    "date": "2018-01-09",
                    "type": "Primary",
                    "description": "Special primary election",
                    "candidate_lists_complete": true,
                    "state": "NH"
                },
                {
                    "date": "2018-01-09",
                    "type": "General",
                    "description": "General election",
                    "candidate_lists_complete": true,
                    "state": "GA"
                },
                {
                    "date": "2018-01-09",
                    "type": "General",
                    "description": "General election",
                    "candidate_lists_complete": true,
                    "state": "GA"
                },
                {
                    "date": "2018-01-09",
                    "type": "General",
                    "description": "Special election",
                    "candidate_lists_complete": true,
                    "state": "CT"
                },
                {
                    "date": "2018-01-09",
                    "type": "Primary",
                    "description": "Special primary election",
                    "candidate_lists_complete": true,
                    "state": "OK"
                },
                {
                    "date": "2018-01-09",
                    "type": "General Runoff",
                    "description": "Special election runoff for State Senate District 49",
                    "candidate_lists_complete": true,
                    "state": "MS"
                },
                {
                    "date": "2018-01-16",
                    "type": "General",
                    "description": "Special election",
                    "candidate_lists_complete": true,
                    "state": "SC"
                },
                {
                    "date": "2018-01-16",
                    "type": "Recall",
                    "description": "https://ballotpedia.org/Mayor_and_town_board_recall,_Rockvale,_",
                    "candidate_lists_complete": true,
                    "state": "CO"
                },
                {
                    "date": "2018-01-16",
                    "type": "General",
                    "description": "Special election",
                    "candidate_lists_complete": true,
                    "state": "WI"
                },
                {
                    "date": "2018-01-16",
                    "type": "General",
                    "description": "Special election",
                    "candidate_lists_complete": true,
                    "state": "WI"
                },
                {
                    "date": "2018-01-16",
                    "type": "General",
                    "description": "Special election",
                    "candidate_lists_complete": true,
                    "state": "WI"
                },
                {
                    "date": "2018-01-16",
                    "type": "General",
                    "description": "Special election",
                    "candidate_lists_complete": true,
                    "state": "SC"
                },
                {
                    "date": "2018-01-16",
                    "type": "General",
                    "description": "Special election",
                    "candidate_lists_complete": true,
                    "state": "SC"
                },
                {
                    "date": "2018-01-16",
                    "type": "General",
                    "description": "Special election",
                    "candidate_lists_complete": true,
                    "state": "IA"
                },
                {
                    "date": "2018-01-23",
                    "type": "Special",
                    "description": null,
                    "candidate_lists_complete": true,
                    "state": "OR"
                },
                {
                    "date": "2018-01-23",
                    "type": "General",
                    "description": "Special election",
                    "candidate_lists_complete": true,
                    "state": "PA"
                },
                {
                    "date": "2018-01-23",
                    "type": "General",
                    "description": "Local ballot measures",
                    "candidate_lists_complete": true,
                    "state": "CA"
                },
                {
                    "date": "2018-01-23",
                    "type": "Recall",
                    "description": "https://ballotpedia.org/Francisco_Ramirez_recall,_Hanford_City_",
                    "candidate_lists_complete": true,
                    "state": "CA"
                },
                {
                    "date": "2018-01-25",
                    "type": "Primary",
                    "description": "Primary election",
                    "candidate_lists_complete": true,
                    "state": "TN"
                },
                {
                    "date": "2018-01-29",
                    "type": "Primary",
                    "description": "Special primary election",
                    "candidate_lists_complete": true,
                    "state": "MN"
                },
                {
                    "date": "2018-01-29",
                    "type": "Primary",
                    "description": "Special primary election",
                    "candidate_lists_complete": true,
                    "state": "MN"
                },
                {
                    "date": "2018-01-30",
                    "type": "Primary",
                    "description": "Special primary election",
                    "candidate_lists_complete": true,
                    "state": "FL"
                }
            ]
        },
        "message": null
    }"""

ELECTION_DATES_NO_PARAM_PAGE2 = (
    """{"success": true, "data": {"elections": null}, "message": null}"""
)

ELECTION_DATES_PARAMS = """    {
        "success": true,
        "data": {
            "elections": [
                {
                    "date": "2020-05-12",
                    "type": "Special",
                    "description": "Special election to fill unexpired term",
                    "candidate_lists_complete": false,
                    "state": "WI"
                }
            ]
        },
        "message": null
    }"""

ELECTIONS_BY_POINT = """    {
        "success": true,
        "data": {
            "longitude": -88.72466949999999,
            "latitude": 43.194246,
            "elections": [
                {
                    "date": "2020-11-03",
                    "candidate_lists_complete": true,
                    "districts": [
                        {
                            "id": 93743,
                            "name": "United States",
                            "type": "Country",
                            "ballot_measures": null,
                            "races": [
                                {
                                    "id": 31729,
                                    "office": {
                                        "id": 1,
                                        "name": "President of the United States",
                                        "level": "Federal",
                                        "branch": "Executive",
                                        "chamber": null,
                                        "is_partisan": "Partisan all",
                                        "type": null,
                                        "seat": null,
                                        "url": null,
                                        "office_district": 93743
                                    },
                                    "office_district": 93743,
                                    "url": "https://ballotpedia.org/Presidential_election,_2020",
                                    "number_of_seats": 1,
                                    "year": 2020,
                                    "type": "Regular",
                                    "is_marquee": false,
                                    "office_position": null,
                                    "is_ranked_choice": false,
                                    "results_certified": true,
                                    "stage_type": "General",
                                    "stage_party": null,
                                    "candidates": [
                                        {
                                            "id": 54804,
                                            "race": 31729,
                                            "running_mate": "Mike Pence",
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 1,
                                                    "name": "Republican Party",
                                                    "url": "https://ballotpedia.org/Republican_Party"
                                                }
                                            ],
                                            "is_incumbent": true,
                                            "is_write_in": false,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Lost",
                                            "votes_for_cand": 1610065,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 15180,
                                                "name": "Donald Trump",
                                                "first_name": "Donald",
                                                "last_name": "Trump",
                                                "url": "https://ballotpedia.org/Donald_Trump"
                                            }
                                        },
                                        {
                                            "id": 55042,
                                            "race": 31729,
                                            "running_mate": null,
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 5,
                                                    "name": "Independent",
                                                    "url": "https://ballotpedia.org/Independent"
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": true,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Lost",
                                            "votes_for_cand": null,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 312671,
                                                "name": "Kasey Wells",
                                                "first_name": "Kasey",
                                                "last_name": "Wells",
                                                "url": "https://ballotpedia.org/Kasey_Wells"
                                            }
                                        },
                                        {
                                            "id": 59216,
                                            "race": 31729,
                                            "running_mate": "Kamala D. Harris",
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 2,
                                                    "name": "Democratic Party",
                                                    "url": "https://ballotpedia.org/Democratic_Party"
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": false,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Won",
                                            "votes_for_cand": 1630673,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 26709,
                                                "name": "Joe Biden",
                                                "first_name": "Joe",
                                                "last_name": "Biden",
                                                "url": "https://ballotpedia.org/Joe_Biden"
                                            }
                                        },
                                        {
                                            "id": 59781,
                                            "race": 31729,
                                            "running_mate": "Angela Nicole Walker",
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 4,
                                                    "name": "Green Party",
                                                    "url": "https://ballotpedia.org/Green_Party"
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": true,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Lost",
                                            "votes_for_cand": null,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 21669,
                                                "name": "Howie Hawkins",
                                                "first_name": "Howie",
                                                "last_name": "Hawkins",
                                                "url": "https://ballotpedia.org/Howie_Hawkins"
                                            }
                                        },
                                        {
                                            "id": 65308,
                                            "race": 31729,
                                            "running_mate": "Spike Cohen",
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 3,
                                                    "name": "Libertarian Party",
                                                    "url": "https://ballotpedia.org/Libertarian_Party"
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": false,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Lost",
                                            "votes_for_cand": 38491,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 322425,
                                                "name": "Jo Jorgensen",
                                                "first_name": "Jo",
                                                "last_name": "Jorgensen",
                                                "url": "https://ballotpedia.org/Jo_Jorgensen"
                                            }
                                        },
                                        {
                                            "id": 65662,
                                            "race": 31729,
                                            "running_mate": "Amar Patel",
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 17,
                                                    "name": "American Solidarity Party",
                                                    "url": null
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": false,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Lost",
                                            "votes_for_cand": 5258,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 292603,
                                                "name": "Brian T. Carroll",
                                                "first_name": "Brian",
                                                "last_name": "Carroll",
                                                "url": "https://ballotpedia.org/Brian_T._Carroll"
                                            }
                                        },
                                        {
                                            "id": 66060,
                                            "race": 31729,
                                            "running_mate": "William Mohr",
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 6,
                                                    "name": "Constitution Party",
                                                    "url": "https://ballotpedia.org/Constitution_Party"
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": false,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Lost",
                                            "votes_for_cand": 5144,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 292195,
                                                "name": "Don Blankenship",
                                                "first_name": "Don",
                                                "last_name": "Blankenship",
                                                "url": "https://ballotpedia.org/Don_Blankenship_(West_Virginia)"
                                            }
                                        },
                                        {
                                            "id": 72757,
                                            "race": 31729,
                                            "running_mate": null,
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 5,
                                                    "name": "Independent",
                                                    "url": "https://ballotpedia.org/Independent"
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": true,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Lost",
                                            "votes_for_cand": null,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 312838,
                                                "name": "President Boddie",
                                                "first_name": "President",
                                                "last_name": "Boddie",
                                                "url": "https://ballotpedia.org/President_Boddie"
                                            }
                                        },
                                        {
                                            "id": 76526,
                                            "race": 31729,
                                            "running_mate": "Claudeliah Roze",
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 21467,
                                                    "name": "Becoming One Nation",
                                                    "url": null
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": true,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Lost",
                                            "votes_for_cand": null,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 324666,
                                                "name": "Jade Simmons",
                                                "first_name": "Jade",
                                                "last_name": "Simmons",
                                                "url": "https://ballotpedia.org/Jade_Simmons"
                                            }
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 433,
                            "name": "Wisconsin District 5",
                            "type": "Congress",
                            "ballot_measures": null,
                            "races": [
                                {
                                    "id": 31685,
                                    "office": {
                                        "id": 18366,
                                        "name": "U.S. House Wisconsin District 5",
                                        "level": "Federal",
                                        "branch": "Legislative",
                                        "chamber": "Lower",
                                        "is_partisan": "Partisan all",
                                        "type": "Representative",
                                        "seat": "Wisconsin's 5th Congressional District",
                                        "url": "https://ballotpedia.org/Wisconsin's_5th_Congressional_District",
                                        "office_district": 433
                                    },
                                    "office_district": 433,
                                    "url": "https://ballotpedia.org/Wisconsin%27s_5th_Congressional_District_election,_2020",
                                    "number_of_seats": 1,
                                    "year": 2020,
                                    "type": "Regular",
                                    "is_marquee": false,
                                    "office_position": null,
                                    "is_ranked_choice": false,
                                    "results_certified": true,
                                    "stage_type": "General",
                                    "stage_party": null,
                                    "candidates": [
                                        {
                                            "id": 65365,
                                            "race": 31685,
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 1,
                                                    "name": "Republican Party",
                                                    "url": "https://ballotpedia.org/Republican_Party"
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": false,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Won",
                                            "votes_for_cand": 265434,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 50408,
                                                "name": "Scott Fitzgerald",
                                                "first_name": "Scott",
                                                "last_name": "Fitzgerald",
                                                "url": "https://ballotpedia.org/Scott_Fitzgerald"
                                            }
                                        },
                                        {
                                            "id": 65431,
                                            "race": 31685,
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 2,
                                                    "name": "Democratic Party",
                                                    "url": "https://ballotpedia.org/Democratic_Party"
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": false,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Lost",
                                            "votes_for_cand": 175902,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 291468,
                                                "name": "Tom Palzewicz",
                                                "first_name": "Tom",
                                                "last_name": "Palzewicz",
                                                "url": "https://ballotpedia.org/Tom_Palzewicz"
                                            }
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": 7263,
                            "name": "Wisconsin State Assembly District 37",
                            "type": "State Legislative (Lower)",
                            "ballot_measures": null,
                            "races": [
                                {
                                    "id": 49591,
                                    "office": {
                                        "id": 6123,
                                        "name": "Wisconsin State Assembly District 37",
                                        "level": "State",
                                        "branch": "Legislative",
                                        "chamber": "Lower",
                                        "is_partisan": "Partisan all",
                                        "type": "Representative",
                                        "seat": "District 37",
                                        "url": "https://ballotpedia.org/Wisconsin_State_Assembly_District_37",
                                        "office_district": 7263
                                    },
                                    "office_district": 7263,
                                    "url": "https://ballotpedia.org/Wisconsin_State_Assembly_elections,_2020",
                                    "number_of_seats": 1,
                                    "year": 2020,
                                    "type": "Regular",
                                    "is_marquee": false,
                                    "office_position": null,
                                    "is_ranked_choice": false,
                                    "results_certified": true,
                                    "stage_type": "General",
                                    "stage_party": null,
                                    "candidates": [
                                        {
                                            "id": 87590,
                                            "race": 49591,
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 2,
                                                    "name": "Democratic Party",
                                                    "url": "https://ballotpedia.org/Democratic_Party"
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": false,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Lost",
                                            "votes_for_cand": 14142,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 330171,
                                                "name": "Abigail Lowery",
                                                "first_name": "Abigail",
                                                "last_name": "Lowery",
                                                "url": "https://ballotpedia.org/Abigail_Lowery"
                                            }
                                        },
                                        {
                                            "id": 87592,
                                            "race": 49591,
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 5,
                                                    "name": "Independent",
                                                    "url": "https://ballotpedia.org/Independent"
                                                }
                                            ],
                                            "is_incumbent": false,
                                            "is_write_in": false,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Lost",
                                            "votes_for_cand": 1041,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 330173,
                                                "name": "Stephen Ratzlaff Jr.",
                                                "first_name": "Stephen",
                                                "last_name": "Ratzlaff",
                                                "url": "https://ballotpedia.org/Stephen_Ratzlaff_Jr."
                                            }
                                        },
                                        {
                                            "id": 87593,
                                            "race": 49591,
                                            "stage_party": null,
                                            "party_affiliation": [
                                                {
                                                    "id": 1,
                                                    "name": "Republican Party",
                                                    "url": "https://ballotpedia.org/Republican_Party"
                                                }
                                            ],
                                            "is_incumbent": true,
                                            "is_write_in": false,
                                            "withdrew_still_on_ballot": false,
                                            "cand_status": "Won",
                                            "votes_for_cand": 19406,
                                            "ranked_choice_voting_rounds": [],
                                            "person": {
                                                "id": 27978,
                                                "name": "John Jagler",
                                                "first_name": "John",
                                                "last_name": "Jagler",
                                                "url": "https://ballotpedia.org/John_Jagler"
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "message": null
    }"""

ELECTIONS_BY_STATE = """    {
        "success": true,
        "data": {
            "election_date": "2020-11-03",
            "districts": [
                {
                    "id": 429,
                    "name": "Wisconsin District 1",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31681,
                            "office": {
                                "id": 2462,
                                "name": "U.S. House Wisconsin District 1",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 1st Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_1st_Congressional_District",
                                "office_district": 429
                            },
                            "office_district": 429,
                            "url": "https://ballotpedia.org/Wisconsin%27s_1st_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "General",
                            "stage_party": null,
                            "candidates": [
                                {
                                    "id": 86856,
                                    "race": 31681,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Won",
                                    "votes_for_cand": 238271,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 298470,
                                        "name": "Bryan Steil",
                                        "first_name": "Bryan",
                                        "last_name": "Steil",
                                        "url": "https://ballotpedia.org/Bryan_Steil"
                                    }
                                },
                                {
                                    "id": 71354,
                                    "race": 31681,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 163170,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 322063,
                                        "name": "Roger Polack",
                                        "first_name": "Roger",
                                        "last_name": "Polack",
                                        "url": "https://ballotpedia.org/Roger_Polack"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 430,
                    "name": "Wisconsin District 2",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31682,
                            "office": {
                                "id": 10859,
                                "name": "U.S. House Wisconsin District 2",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 2nd Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_2nd_Congressional_District",
                                "office_district": 430
                            },
                            "office_district": 430,
                            "url": "https://ballotpedia.org/Wisconsin%27s_2nd_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "General",
                            "stage_party": null,
                            "candidates": [
                                {
                                    "id": 64770,
                                    "race": 31682,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Won",
                                    "votes_for_cand": 318523,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 37193,
                                        "name": "Mark Pocan",
                                        "first_name": "Mark",
                                        "last_name": "Pocan",
                                        "url": "https://ballotpedia.org/Mark_Pocan"
                                    }
                                },
                                {
                                    "id": 86859,
                                    "race": 31682,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 138306,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 44392,
                                        "name": "Peter Theron",
                                        "first_name": "Peter",
                                        "last_name": "Theron",
                                        "url": "https://ballotpedia.org/Peter_Theron"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 431,
                    "name": "Wisconsin District 3",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31683,
                            "office": {
                                "id": 6351,
                                "name": "U.S. House Wisconsin District 3",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 3rd Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_3rd_Congressional_District",
                                "office_district": 431
                            },
                            "office_district": 431,
                            "url": "https://ballotpedia.org/Wisconsin%27s_3rd_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "General",
                            "stage_party": null,
                            "candidates": [
                                {
                                    "id": 69082,
                                    "race": 31683,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Won",
                                    "votes_for_cand": 199870,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 48575,
                                        "name": "Ronald James Kind",
                                        "first_name": "Ronald James",
                                        "last_name": "Kind",
                                        "url": "https://ballotpedia.org/Ron_Kind"
                                    }
                                },
                                {
                                    "id": 78990,
                                    "race": 31683,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 189524,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 326054,
                                        "name": "Derrick Van Orden",
                                        "first_name": "Derrick",
                                        "last_name": "Van Orden",
                                        "url": "https://ballotpedia.org/Derrick_Van_Orden"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 432,
                    "name": "Wisconsin District 4",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31684,
                            "office": {
                                "id": 3854,
                                "name": "U.S. House Wisconsin District 4",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 4th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_4th_Congressional_District",
                                "office_district": 432
                            },
                            "office_district": 432,
                            "url": "https://ballotpedia.org/Wisconsin%27s_4th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "General",
                            "stage_party": null,
                            "candidates": [
                                {
                                    "id": 69083,
                                    "race": 31684,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Won",
                                    "votes_for_cand": 232668,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 20718,
                                        "name": "Gwen Moore",
                                        "first_name": "Gwen",
                                        "last_name": "Moore",
                                        "url": "https://ballotpedia.org/Gwen_Moore"
                                    }
                                },
                                {
                                    "id": 86863,
                                    "race": 31684,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 70769,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 301297,
                                        "name": "Tim Rogers",
                                        "first_name": "Tim",
                                        "last_name": "Rogers",
                                        "url": "https://ballotpedia.org/Tim_Rogers_(Wisconsin)"
                                    }
                                },
                                {
                                    "id": 86862,
                                    "race": 31684,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 5,
                                            "name": "Independent",
                                            "url": "https://ballotpedia.org/Independent"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 7911,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 47819,
                                        "name": "Robert Raymond",
                                        "first_name": "Robert",
                                        "last_name": "Raymond",
                                        "url": "https://ballotpedia.org/Robert_Raymond"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 433,
                    "name": "Wisconsin District 5",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31685,
                            "office": {
                                "id": 18366,
                                "name": "U.S. House Wisconsin District 5",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 5th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_5th_Congressional_District",
                                "office_district": 433
                            },
                            "office_district": 433,
                            "url": "https://ballotpedia.org/Wisconsin%27s_5th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "General",
                            "stage_party": null,
                            "candidates": [
                                {
                                    "id": 65431,
                                    "race": 31685,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 175902,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 291468,
                                        "name": "Tom Palzewicz",
                                        "first_name": "Tom",
                                        "last_name": "Palzewicz",
                                        "url": "https://ballotpedia.org/Tom_Palzewicz"
                                    }
                                },
                                {
                                    "id": 65365,
                                    "race": 31685,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Won",
                                    "votes_for_cand": 265434,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 50408,
                                        "name": "Scott Fitzgerald",
                                        "first_name": "Scott",
                                        "last_name": "Fitzgerald",
                                        "url": "https://ballotpedia.org/Scott_Fitzgerald"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 434,
                    "name": "Wisconsin District 6",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31686,
                            "office": {
                                "id": 3154,
                                "name": "U.S. House Wisconsin District 6",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 6th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_6th_Congressional_District",
                                "office_district": 434
                            },
                            "office_district": 434,
                            "url": "https://ballotpedia.org/Wisconsin%27s_6th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "General",
                            "stage_party": null,
                            "candidates": [
                                {
                                    "id": 69084,
                                    "race": 31686,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Won",
                                    "votes_for_cand": 238874,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 20002,
                                        "name": "Glenn Grothman",
                                        "first_name": "Glenn",
                                        "last_name": "Grothman",
                                        "url": "https://ballotpedia.org/Glenn_Grothman"
                                    }
                                },
                                {
                                    "id": 65708,
                                    "race": 31686,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 164239,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 25644,
                                        "name": "Jessica King",
                                        "first_name": "Jessica",
                                        "last_name": "King",
                                        "url": "https://ballotpedia.org/Jessica_King_(Wisconsin)"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 435,
                    "name": "Wisconsin District 7",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31687,
                            "office": {
                                "id": 4951,
                                "name": "U.S. House Wisconsin District 7",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 7th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_7th_Congressional_District",
                                "office_district": 435
                            },
                            "office_district": 435,
                            "url": "https://ballotpedia.org/Wisconsin%27s_7th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "General",
                            "stage_party": null,
                            "candidates": [
                                {
                                    "id": 86868,
                                    "race": 31687,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Won",
                                    "votes_for_cand": 252048,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 56044,
                                        "name": "Tom Tiffany",
                                        "first_name": "Tom",
                                        "last_name": "Tiffany",
                                        "url": "https://ballotpedia.org/Tom_Tiffany"
                                    }
                                },
                                {
                                    "id": 85345,
                                    "race": 31687,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 162741,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 293245,
                                        "name": "Tricia Zunker",
                                        "first_name": "Tricia",
                                        "last_name": "Zunker",
                                        "url": "https://ballotpedia.org/Tricia_Zunker"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 436,
                    "name": "Wisconsin District 8",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31688,
                            "office": {
                                "id": 16129,
                                "name": "U.S. House Wisconsin District 8",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 8th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_8th_Congressional_District",
                                "office_district": 436
                            },
                            "office_district": 436,
                            "url": "https://ballotpedia.org/Wisconsin%27s_8th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "General",
                            "stage_party": null,
                            "candidates": [
                                {
                                    "id": 69085,
                                    "race": 31688,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Won",
                                    "votes_for_cand": 268173,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 39493,
                                        "name": "Mike Gallagher",
                                        "first_name": "Mike",
                                        "last_name": "Gallagher",
                                        "url": "https://ballotpedia.org/Michael_Gallagher_(Wisconsin)"
                                    }
                                },
                                {
                                    "id": 60416,
                                    "race": 31688,
                                    "stage_party": null,
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 149558,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 1287,
                                        "name": "Amanda Stuck",
                                        "first_name": "Amanda",
                                        "last_name": "Stuck",
                                        "url": "https://ballotpedia.org/Amanda_Stuck"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "message": null
    }"""

ELECTIONS_BY_STATE_PARTISAN = """    {
        "success": true,
        "data": {
            "election_date": "2020-08-11",
            "districts": [
                {
                    "id": 429,
                    "name": "Wisconsin District 1",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31681,
                            "office": {
                                "id": 2462,
                                "name": "U.S. House Wisconsin District 1",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 1st Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_1st_Congressional_District",
                                "office_district": 429
                            },
                            "office_district": 429,
                            "url": "https://ballotpedia.org/Wisconsin%27s_1st_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": false,
                            "stage_type": "Primary",
                            "stage_party": "Democratic Party",
                            "candidates": [
                                {
                                    "id": 62622,
                                    "race": 31681,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 20608,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 301301,
                                        "name": "Josh Pade",
                                        "first_name": "Josh",
                                        "last_name": "Pade",
                                        "url": "https://ballotpedia.org/Josh_Pade"
                                    }
                                },
                                {
                                    "id": 71354,
                                    "race": 31681,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 28697,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 322063,
                                        "name": "Roger Polack",
                                        "first_name": "Roger",
                                        "last_name": "Polack",
                                        "url": "https://ballotpedia.org/Roger_Polack"
                                    }
                                }
                            ]
                        },
                        {
                            "id": 31681,
                            "office": {
                                "id": 2462,
                                "name": "U.S. House Wisconsin District 1",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 1st Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_1st_Congressional_District",
                                "office_district": 429
                            },
                            "office_district": 429,
                            "url": "https://ballotpedia.org/Wisconsin%27s_1st_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Republican Party",
                            "candidates": [
                                {
                                    "id": 86856,
                                    "race": 31681,
                                    "stage_party": "Republican Party",
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 40273,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 298470,
                                        "name": "Bryan Steil",
                                        "first_name": "Bryan",
                                        "last_name": "Steil",
                                        "url": "https://ballotpedia.org/Bryan_Steil"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 430,
                    "name": "Wisconsin District 2",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31682,
                            "office": {
                                "id": 10859,
                                "name": "U.S. House Wisconsin District 2",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 2nd Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_2nd_Congressional_District",
                                "office_district": 430
                            },
                            "office_district": 430,
                            "url": "https://ballotpedia.org/Wisconsin%27s_2nd_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Democratic Party",
                            "candidates": [
                                {
                                    "id": 64770,
                                    "race": 31682,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 120353,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 37193,
                                        "name": "Mark Pocan",
                                        "first_name": "Mark",
                                        "last_name": "Pocan",
                                        "url": "https://ballotpedia.org/Mark_Pocan"
                                    }
                                }
                            ]
                        },
                        {
                            "id": 31682,
                            "office": {
                                "id": 10859,
                                "name": "U.S. House Wisconsin District 2",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 2nd Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_2nd_Congressional_District",
                                "office_district": 430
                            },
                            "office_district": 430,
                            "url": "https://ballotpedia.org/Wisconsin%27s_2nd_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Republican Party",
                            "candidates": [
                                {
                                    "id": 86859,
                                    "race": 31682,
                                    "stage_party": "Republican Party",
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 18812,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 44392,
                                        "name": "Peter Theron",
                                        "first_name": "Peter",
                                        "last_name": "Theron",
                                        "url": "https://ballotpedia.org/Peter_Theron"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 431,
                    "name": "Wisconsin District 3",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31683,
                            "office": {
                                "id": 6351,
                                "name": "U.S. House Wisconsin District 3",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 3rd Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_3rd_Congressional_District",
                                "office_district": 431
                            },
                            "office_district": 431,
                            "url": "https://ballotpedia.org/Wisconsin%27s_3rd_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Republican Party",
                            "candidates": [
                                {
                                    "id": 74688,
                                    "race": 31683,
                                    "stage_party": "Republican Party",
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 18835,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 323890,
                                        "name": "Jessi Ebben",
                                        "first_name": "Jessi",
                                        "last_name": "Ebben",
                                        "url": "https://ballotpedia.org/Jessi_Ebben"
                                    }
                                },
                                {
                                    "id": 78990,
                                    "race": 31683,
                                    "stage_party": "Republican Party",
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 36395,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 326054,
                                        "name": "Derrick Van Orden",
                                        "first_name": "Derrick",
                                        "last_name": "Van Orden",
                                        "url": "https://ballotpedia.org/Derrick_Van_Orden"
                                    }
                                }
                            ]
                        },
                        {
                            "id": 31683,
                            "office": {
                                "id": 6351,
                                "name": "U.S. House Wisconsin District 3",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 3rd Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_3rd_Congressional_District",
                                "office_district": 431
                            },
                            "office_district": 431,
                            "url": "https://ballotpedia.org/Wisconsin%27s_3rd_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Democratic Party",
                            "candidates": [
                                {
                                    "id": 69082,
                                    "race": 31683,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 53064,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 48575,
                                        "name": "Ronald James Kind",
                                        "first_name": "Ronald James",
                                        "last_name": "Kind",
                                        "url": "https://ballotpedia.org/Ron_Kind"
                                    }
                                },
                                {
                                    "id": 71870,
                                    "race": 31683,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 12765,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 323092,
                                        "name": "Mark A. Neumann",
                                        "first_name": "Mark",
                                        "last_name": "Neumann",
                                        "url": "https://ballotpedia.org/Mark_Neumann_(Wisconsin_congressional_candidate)"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 432,
                    "name": "Wisconsin District 4",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31684,
                            "office": {
                                "id": 3854,
                                "name": "U.S. House Wisconsin District 4",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 4th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_4th_Congressional_District",
                                "office_district": 432
                            },
                            "office_district": 432,
                            "url": "https://ballotpedia.org/Wisconsin%27s_4th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Democratic Party",
                            "candidates": [
                                {
                                    "id": 69083,
                                    "race": 31684,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 68898,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 20718,
                                        "name": "Gwen Moore",
                                        "first_name": "Gwen",
                                        "last_name": "Moore",
                                        "url": "https://ballotpedia.org/Gwen_Moore"
                                    }
                                }
                            ]
                        },
                        {
                            "id": 31684,
                            "office": {
                                "id": 3854,
                                "name": "U.S. House Wisconsin District 4",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 4th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_4th_Congressional_District",
                                "office_district": 432
                            },
                            "office_district": 432,
                            "url": "https://ballotpedia.org/Wisconsin%27s_4th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Republican Party",
                            "candidates": [
                                {
                                    "id": 86863,
                                    "race": 31684,
                                    "stage_party": "Republican Party",
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 6685,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 301297,
                                        "name": "Tim Rogers",
                                        "first_name": "Tim",
                                        "last_name": "Rogers",
                                        "url": "https://ballotpedia.org/Tim_Rogers_(Wisconsin)"
                                    }
                                },
                                {
                                    "id": 71872,
                                    "race": 31684,
                                    "stage_party": "Republican Party",
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 6598,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 301298,
                                        "name": "Cindy Werner",
                                        "first_name": "Cindy",
                                        "last_name": "Werner",
                                        "url": "https://ballotpedia.org/Cindy_Werner"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 433,
                    "name": "Wisconsin District 5",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31685,
                            "office": {
                                "id": 18366,
                                "name": "U.S. House Wisconsin District 5",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 5th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_5th_Congressional_District",
                                "office_district": 433
                            },
                            "office_district": 433,
                            "url": "https://ballotpedia.org/Wisconsin%27s_5th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Democratic Party",
                            "candidates": [
                                {
                                    "id": 65431,
                                    "race": 31685,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 43710,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 291468,
                                        "name": "Tom Palzewicz",
                                        "first_name": "Tom",
                                        "last_name": "Palzewicz",
                                        "url": "https://ballotpedia.org/Tom_Palzewicz"
                                    }
                                }
                            ]
                        },
                        {
                            "id": 31685,
                            "office": {
                                "id": 18366,
                                "name": "U.S. House Wisconsin District 5",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 5th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_5th_Congressional_District",
                                "office_district": 433
                            },
                            "office_district": 433,
                            "url": "https://ballotpedia.org/Wisconsin%27s_5th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": true,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Republican Party",
                            "candidates": [
                                {
                                    "id": 83219,
                                    "race": 31685,
                                    "stage_party": "Republican Party",
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 17829,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 328083,
                                        "name": "Clifford DeTemple",
                                        "first_name": "Clifford",
                                        "last_name": "DeTemple",
                                        "url": "https://ballotpedia.org/Clifford_DeTemple"
                                    }
                                },
                                {
                                    "id": 65365,
                                    "race": 31685,
                                    "stage_party": "Republican Party",
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 60676,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 50408,
                                        "name": "Scott Fitzgerald",
                                        "first_name": "Scott",
                                        "last_name": "Fitzgerald",
                                        "url": "https://ballotpedia.org/Scott_Fitzgerald"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 434,
                    "name": "Wisconsin District 6",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31686,
                            "office": {
                                "id": 3154,
                                "name": "U.S. House Wisconsin District 6",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 6th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_6th_Congressional_District",
                                "office_district": 434
                            },
                            "office_district": 434,
                            "url": "https://ballotpedia.org/Wisconsin%27s_6th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Republican Party",
                            "candidates": [
                                {
                                    "id": 69084,
                                    "race": 31686,
                                    "stage_party": "Republican Party",
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 52247,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 20002,
                                        "name": "Glenn Grothman",
                                        "first_name": "Glenn",
                                        "last_name": "Grothman",
                                        "url": "https://ballotpedia.org/Glenn_Grothman"
                                    }
                                }
                            ]
                        },
                        {
                            "id": 31686,
                            "office": {
                                "id": 3154,
                                "name": "U.S. House Wisconsin District 6",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 6th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_6th_Congressional_District",
                                "office_district": 434
                            },
                            "office_district": 434,
                            "url": "https://ballotpedia.org/Wisconsin%27s_6th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": false,
                            "stage_type": "Primary",
                            "stage_party": "Democratic Party",
                            "candidates": [
                                {
                                    "id": 73552,
                                    "race": 31686,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 7885,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 323313,
                                        "name": "Michael Beardsley",
                                        "first_name": "Michael",
                                        "last_name": "Beardsley",
                                        "url": "https://ballotpedia.org/Michael_Beardsley"
                                    }
                                },
                                {
                                    "id": 63649,
                                    "race": 31686,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Lost",
                                    "votes_for_cand": 4565,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 317776,
                                        "name": "Matthew Boor",
                                        "first_name": "Matthew",
                                        "last_name": "Boor",
                                        "url": "https://ballotpedia.org/Matthew_Boor"
                                    }
                                },
                                {
                                    "id": 65708,
                                    "race": 31686,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 38039,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 25644,
                                        "name": "Jessica King",
                                        "first_name": "Jessica",
                                        "last_name": "King",
                                        "url": "https://ballotpedia.org/Jessica_King_(Wisconsin)"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 435,
                    "name": "Wisconsin District 7",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31687,
                            "office": {
                                "id": 4951,
                                "name": "U.S. House Wisconsin District 7",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 7th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_7th_Congressional_District",
                                "office_district": 435
                            },
                            "office_district": 435,
                            "url": "https://ballotpedia.org/Wisconsin%27s_7th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Republican Party",
                            "candidates": [
                                {
                                    "id": 86868,
                                    "race": 31687,
                                    "stage_party": "Republican Party",
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 62142,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 56044,
                                        "name": "Tom Tiffany",
                                        "first_name": "Tom",
                                        "last_name": "Tiffany",
                                        "url": "https://ballotpedia.org/Tom_Tiffany"
                                    }
                                }
                            ]
                        },
                        {
                            "id": 31687,
                            "office": {
                                "id": 4951,
                                "name": "U.S. House Wisconsin District 7",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 7th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_7th_Congressional_District",
                                "office_district": 435
                            },
                            "office_district": 435,
                            "url": "https://ballotpedia.org/Wisconsin%27s_7th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Democratic Party",
                            "candidates": [
                                {
                                    "id": 85345,
                                    "race": 31687,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 51139,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 293245,
                                        "name": "Tricia Zunker",
                                        "first_name": "Tricia",
                                        "last_name": "Zunker",
                                        "url": "https://ballotpedia.org/Tricia_Zunker"
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": 436,
                    "name": "Wisconsin District 8",
                    "type": "Congress",
                    "ballot_measures": null,
                    "races": [
                        {
                            "id": 31688,
                            "office": {
                                "id": 16129,
                                "name": "U.S. House Wisconsin District 8",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 8th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_8th_Congressional_District",
                                "office_district": 436
                            },
                            "office_district": 436,
                            "url": "https://ballotpedia.org/Wisconsin%27s_8th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Republican Party",
                            "candidates": [
                                {
                                    "id": 69085,
                                    "race": 31688,
                                    "stage_party": "Republican Party",
                                    "party_affiliation": [
                                        {
                                            "id": 1,
                                            "name": "Republican Party",
                                            "url": "https://ballotpedia.org/Republican_Party"
                                        }
                                    ],
                                    "is_incumbent": true,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 50176,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 39493,
                                        "name": "Mike Gallagher",
                                        "first_name": "Mike",
                                        "last_name": "Gallagher",
                                        "url": "https://ballotpedia.org/Michael_Gallagher_(Wisconsin)"
                                    }
                                }
                            ]
                        },
                        {
                            "id": 31688,
                            "office": {
                                "id": 16129,
                                "name": "U.S. House Wisconsin District 8",
                                "level": "Federal",
                                "branch": "Legislative",
                                "chamber": "Lower",
                                "is_partisan": "Partisan all",
                                "type": "Representative",
                                "seat": "Wisconsin's 8th Congressional District",
                                "url": "https://ballotpedia.org/Wisconsin's_8th_Congressional_District",
                                "office_district": 436
                            },
                            "office_district": 436,
                            "url": "https://ballotpedia.org/Wisconsin%27s_8th_Congressional_District_election,_2020",
                            "number_of_seats": 1,
                            "year": 2020,
                            "race_type": "Regular",
                            "is_marquee": false,
                            "office_position": null,
                            "is_ranked_choice": false,
                            "results_certified": true,
                            "stage_type": "Primary",
                            "stage_party": "Democratic Party",
                            "candidates": [
                                {
                                    "id": 60416,
                                    "race": 31688,
                                    "stage_party": "Democratic Party",
                                    "party_affiliation": [
                                        {
                                            "id": 2,
                                            "name": "Democratic Party",
                                            "url": "https://ballotpedia.org/Democratic_Party"
                                        }
                                    ],
                                    "is_incumbent": false,
                                    "is_write_in": false,
                                    "withdrew_still_on_ballot": false,
                                    "cand_status": "Advanced",
                                    "votes_for_cand": 44793,
                                    "ranked_choice_voting_rounds": [],
                                    "person": {
                                        "id": 1287,
                                        "name": "Amanda Stuck",
                                        "first_name": "Amanda",
                                        "last_name": "Stuck",
                                        "url": "https://ballotpedia.org/Amanda_Stuck"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "message": null
    }"""

ELECTIONS_BY_STATE_RCV = """    {
        "id": 93938,
        "name": "San Francisco Board of Supervisors District 5",
        "type": "County subdivision",
        "ballot_measures": null,
        "races": [
          {
            "id": 42896,
            "office": {
              "id": 12637,
              "name": "San Francisco Board of Supervisors District 5",
              "level": "Local",
              "branch": "Legislative",
              "chamber": null,
              "is_partisan": "Nonpartisan all",
              "type": "City council",
              "seat": "District 5",
              "url": null,
              "office_district": 93938
            },
            "office_district": 93938,
            "url": "https://ballotpedia.org/City_elections_in_San_Francisco,_California_(2019)",
            "number_of_seats": 1,
            "year": 2019,
            "race_type": "Special",
            "is_marquee": false,
            "office_position": null,
            "is_ranked_choice": true,
            "results_certified": true,
            "stage_type": "General",
            "stage_party": null,
            "candidates": [
              {
                "id": 59977,
                "race": 42896,
                "stage_party": null,
                "party_affiliation": [
                  {
                    "id": 7,
                    "name": "Nonpartisan",
                    "url": "https://ballotpedia.org/Nonpartisan"
                  }
                ],
                "is_incumbent": true,
                "is_write_in": false,
                "withdrew_still_on_ballot": false,
                "cand_status": "Lost",
                "votes_for_cand": 11538,
                "ranked_choice_voting_rounds": [
                  {
                    "rcv_round": 1,
                    "votes_for": 11208,
                    "status": "Advanced"
                  },
                  {
                    "rcv_round": 2,
                    "votes_for": 51,
                    "status": "Advanced"
                  },
                  {
                    "rcv_round": 3,
                    "votes_for": 279,
                    "status": "Lost"
                  }
                ],
                "person": {
                  "id": 304529,
                  "name": "Vallie Brown",
                  "first_name": "Vallie",
                  "last_name": "Brown",
                  "url": "https://ballotpedia.org/Vallie_Brown"
                }
              },
              {
                "id": 59980,
                "race": 42896,
                "stage_party": null,
                "party_affiliation": [
                  {
                    "id": 7,
                    "name": "Nonpartisan",
                    "url": "https://ballotpedia.org/Nonpartisan"
                  }
                ],
                "is_incumbent": false,
                "is_write_in": false,
                "withdrew_still_on_ballot": false,
                "cand_status": "Lost",
                "votes_for_cand": 1035,
                "ranked_choice_voting_rounds": [
                  {
                    "rcv_round": 1,
                    "votes_for": 950,
                    "status": "Advanced"
                  },
                  {
                    "rcv_round": 2,
                    "votes_for": 85,
                    "status": "Advanced"
                  },
                  {
                    "rcv_round": 3,
                    "votes_for": null,
                    "status": "Lost"
                  }
                ],
                "person": {
                  "id": 314488,
                  "name": "Ryan Lam",
                  "first_name": "Ryan",
                  "last_name": "Lam",
                  "url": "https://ballotpedia.org/Ryan_Lam"
                }
              },
              {
                "id": 59979,
                "race": 42896,
                "stage_party": null,
                "party_affiliation": [
                  {
                    "id": 7,
                    "name": "Nonpartisan",
                    "url": "https://ballotpedia.org/Nonpartisan"
                  }
                ],
                "is_incumbent": false,
                "is_write_in": false,
                "withdrew_still_on_ballot": false,
                "cand_status": "Lost",
                "votes_for_cand": 278,
                "ranked_choice_voting_rounds": [
                  {
                    "rcv_round": 1,
                    "votes_for": 278,
                    "status": "Advanced"
                  },
                  {
                    "rcv_round": 2,
                    "votes_for": null,
                    "status": "Lost"
                  },
                  {
                    "rcv_round": 3,
                    "votes_for": 0,
                    "status": "Lost"
                  }
                ],
                "person": {
                  "id": 314487,
                  "name": "Nomvula O'Meara",
                  "first_name": "Nomvula",
                  "last_name": "O'Meara",
                  "url": "https://ballotpedia.org/Nomvula_O'Meara"
                }
              },
              {
                "id": 59978,
                "race": 42896,
                "stage_party": null,
                "party_affiliation": [
                  {
                    "id": 7,
                    "name": "Nonpartisan",
                    "url": "https://ballotpedia.org/Nonpartisan"
                  }
                ],
                "is_incumbent": false,
                "is_write_in": false,
                "withdrew_still_on_ballot": false,
                "cand_status": "Won",
                "votes_for_cand": 11723,
                "ranked_choice_voting_rounds": [
                  {
                    "rcv_round": 1,
                    "votes_for": 11239,
                    "status": "Advanced"
                  },
                  {
                    "rcv_round": 2,
                    "votes_for": 70,
                    "status": "Advanced"
                  },
                  {
                    "rcv_round": 3,
                    "votes_for": 414,
                    "status": "Won"
                  }
                ],
                "person": {
                  "id": 13552,
                  "name": "Dean Preston",
                  "first_name": "Dean",
                  "last_name": "Preston",
                  "url": "https://ballotpedia.org/Dean_Preston"
                }
              }
            ]
          }
        ]
      }"""

ELECTIONS_BY_STATE_ERROR = """{"success": false, "data": {}, "message": "State and election date must be supplied."}"""
ELECTIONS_BY_STATE_PAGE2 = (
    """{"success": true, "data": "No results.", "message": null}"""
)
