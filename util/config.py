from json import load


class Config:
    def __init__(self):
        with open("config.json", "r") as fp:
            self.config = load(fp)

    def get_api_key(self):
        return self.config["api_key"]

    def get_start_match_id(self):
        return self.config["start_match_id"]

    def get_matches_requested(self):
        return self.config["matches_requested"]

    def get_data_path(self):
        return self.config["data_path"]

    def get_file_name_pattern(self):
        return self.config["file_name_pattern"]

    def get_worker_name_pattern(self):
        return self.config["worker_name_pattern"]

    def get_worker_count(self):
        return self.config["worker_count"]

    def get_file_size_binary_power(self):
        return self.config["file_size_binary_power"]
