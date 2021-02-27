from json import load, dump


class Config:
    def __init__(self):
        with open("config.json", "r") as fp:
            self.config = load(fp)

    def get_history_worker_api_key(self):
        return self.config["history_worker_api_key"]

    def get_details_workers_api_keys(self):
        return self.config["details_workers_api_keys"]

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

    def get_file_size_binary_power(self):
        return self.config["file_size_binary_power"]

    def get_sleep_duration(self):
        return self.config["sleep_duration"]

    def get_dump_path(self):
        return self.config["dump_path"]

    @staticmethod
    def exists():
        from os.path import exists

        return exists("config.json")

    @staticmethod
    def create_blank():
        config = {
            "history_worker_api_key": "",
            "details_workers_api_keys": [],
            "start_match_id": 0,
            "matches_requested": 0,
            "data_path": "",
            "file_name_pattern": "",
            "worker_name_pattern": "",
            "file_size_binary_power": 0,
            "sleep_duration": 0,
            "dump_path": ""
        }

        with open("config.json", "w") as config_file:
            dump(config, config_file)
