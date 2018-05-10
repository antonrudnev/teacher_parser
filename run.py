import argparse
from multiprocessing.pool import Pool
from pymongo import MongoClient
from settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE, MONGO_COLLECTION, MAX_PAGE_SIZE, WORKERS
from time import time, localtime, strftime

try:
    from settings import PAGE_SERVER_URL
    from tornado.httpclient import HTTPClient, HTTPRequest
    from urllib.parse import urlencode
    import json
except ImportError:
    PAGE_SERVER_URL = None
    from extractors import extract_all


def process_page_remotely(page_id, html, input_schools):
    post_fields = [("page_id", page_id), ("html", html)]
    for school in input_schools:
        post_fields.append(("input_schools", school))
    request = HTTPRequest(url=PAGE_SERVER_URL, method='POST', headers=None, body=urlencode(post_fields).encode())
    response = HTTPClient().fetch(request)
    features = json.loads(response.body)["features"]
    return features


def process_page(page_id, html, input_schools, page_number, pages_cnt):
    with MongoClient(MONGO_HOST, MONGO_PORT) as conn:
        coll = conn[MONGO_DATABASE][MONGO_COLLECTION]
        try:
            if PAGE_SERVER_URL:
                features = process_page_remotely(page_id, html, input_schools)
            else:
                features = extract_all(html, input_schools)
            coll.update_one({"_id": page_id},
                            {"$set": {"parsed_features": features,
                                      "parser_status": "ok"}})
            print("Document {} from {} is processed".format(page_number, pages_cnt))
        except Exception as e:
            coll.update_one({"_id": page_id}, {"$set": {"parser_status": "fail"}})
            print("Document {} from {} is failed".format(page_number, pages_cnt))
            print(e)


def process_mongo_collection(workers_number):
    with MongoClient(MONGO_HOST, MONGO_PORT) as conn:
        coll = conn[MONGO_DATABASE][MONGO_COLLECTION]
        pages = coll.find({"html": {"$exists": True},
                           "body": {"$exists": True},
                           "$expr": {"$lt": [{"$strLenCP": {"$arrayElemAt": ["$html", 0]}}, MAX_PAGE_SIZE]}}).limit(10)
        pages_cnt = pages.count()
        with Pool(workers_number) as executor:
            executor.starmap(process_page,
                             ((page["_id"],
                               page["html"][0],
                               page["schoolnames"][0].split(";"),
                               i + 1,
                               pages_cnt,) for i, page in enumerate(pages)))
        print("All pages are processed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workers", type=int, default=WORKERS, help="the exponent")
    args = parser.parse_args()

    start_time = time()
    print(strftime("%d %b %Y %H:%M:%S", localtime(start_time)))
    process_mongo_collection(args.workers)
    print("Done")
    end_time = time()
    print(strftime("%d %b %Y %H:%M:%S", localtime(end_time)))
    print("{:.4f}min".format((end_time - start_time) / 60))
