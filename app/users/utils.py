# import requests
import logging
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

dotenv_path = os.path.join(os.getcwd(), ".env")
env = load_dotenv(dotenv_path=dotenv_path, override=True)


logger = logging.getLogger(__name__)


def fetch_and_index_hydrology_data():
    """
    This api fetches the data from the given url and
    stores it in elasticsearch and can view from that
    from the kiabana
    """
    es = Elasticsearch(os.getenv("ELASCTIC_HOST"))

    # website is down so this part of code commented instead just hard coded json data
    # response = requests.get(os.getenv("API_URL"))
    # response.raise_for_status()
    # data = response.json()

    # if data.get("status") != "success":
    #     print("Faliled to fetch data")
    #     return

    data = {
        "status": "success",
        "data": [
            {
                "station_no": "115",
                "river_name": "Naugra Gad",
                "location": " Harsing Bagar Darchula",
                "latitude": "29.702",
                "longitude": "80.607",
                "elevation": "784",
                "drainage": "206",
                "published_date_from": "2000",
                "published_date_to": "2019",
            },
            {
                "station_no": "120",
                "river_name": "Chamelia River",
                "location": " Nayalbadi Darchula",
                "latitude": "29.67442",
                "longitude": "80.56268",
                "elevation": "685",
                "drainage": "1166",
                "published_date_from": "1965",
                "published_date_to": "2019",
            },
        ],
    }

    stations = data.get("data", [])

    actions = [
        {
            "_index": "hydrology-stations",
            "_id": stations["station_no"],
            "_source": station,
        }
        for station in stations
    ]

    helpers.bulk(es, actions)
    # for station in stations:
    #     station_id = station.get("station_no")
    #     es.index(index="hydrology-stations", id=station_id, body=station)

    logger.info(f"Index Created {len(stations)}")
