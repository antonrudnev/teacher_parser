import argparse
import pandas as pd
from time import time
from pymongo import MongoClient
from settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE, MONGO_COLLECTION


def export_to_csv(file_name, confidence_score):
    with MongoClient(MONGO_HOST, MONGO_PORT) as conn:
        coll = conn[MONGO_DATABASE][MONGO_COLLECTION]
        output_dataset = []
        pages = coll.find({"parser_status": "success", "parsed_features.resolution_score": {"$gte": confidence_score}})
        print("{} pages to export".format(pages.count()))
        for page in pages:
            for name in page["parsed_features"]["resolved_context"]:
                name_data = {**{"url": page["url"][0]},
                             **{"school_ids": page["school_ids"]},
                             **{"school_names": page["schoolnames"]},
                             **{"school_name": page["parsed_features"]["resolved_schools"]["resolved_school"]},
                             **{"school_name_resolved": page["parsed_features"]["school_in_title"]},
                             **{"school_name_conf": page["parsed_features"]["resolved_schools"]["similarity_score"]},
                             **{"name": name["name"]},
                             **{"email": name["email"]},
                             **{"phone": name["phone"]},
                             **{"context": name["role"]},
                             **{"xml": name["xml_context"]},
                             **{"cluster_score": name["cluster_score"]},
                             **{"schema": name["schema"]},
                             **{"name_conf_score_ub": page["parsed_features"]["resolution_score"]}}
                output_dataset.append(name_data)
        df = pd.DataFrame(output_dataset)
        df = df.reindex(
            columns=["school_ids", "school_names", "school_name", "school_name_conf", "school_name_resolved", "url",
                     "name_conf_score_ub", "name", "context", "email", "phone", "cluster_score", "schema", "xml"])
        df.to_csv(file_name, index=False, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, default="results.csv", help="file name to export results")
    parser.add_argument("-c", "--conf", type=float, default=0.3, help="minimum resolution confidence score")
    args = parser.parse_args()
    start_time = time()
    print("Export is started")
    export_to_csv(args.file, args.conf)
    end_time = time()
    print("Export is finished in {:.3f} minutes".format((end_time - start_time) / 60))
