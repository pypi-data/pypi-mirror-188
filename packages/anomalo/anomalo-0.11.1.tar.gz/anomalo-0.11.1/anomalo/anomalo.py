#!/usr/bin/env python

import os
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Optional, Sequence, Set
from urllib.parse import urlparse

import fire
import requests

from .encoder import Encoder


SavedObject = Dict[str, Any]


class Client:
    output_style = "json"

    def __init__(
        self,
        api_token=None,
        host=None,
        proto=None,
        ssl_cert_verify=None,
        output_style=None,
    ):
        if output_style:
            self.output_style = output_style
        self.host = host if host else os.environ.get("ANOMALO_INSTANCE_HOST")
        self.api_token = (
            api_token if api_token else os.environ.get("ANOMALO_API_SECRET_TOKEN")
        )

        if not self.host:
            raise RuntimeError(
                "Please specify Anomalo instance host via ANOMALO_INSTANCE_HOST env var"
            )
        if not self.api_token:
            raise RuntimeError(
                "Please specify Anomalo api token via ANOMALO_API_SECRET_TOKEN env var"
            )

        parsed_host_url = urlparse(self.host)
        host_scheme = parsed_host_url.scheme
        if host_scheme:
            self.proto = host_scheme
            self.host = parsed_host_url.netloc
        else:
            self.proto = proto if proto else "https"

        self.request_headers = {"X-Anomalo-Token": self.api_token}

        self.verify = ssl_cert_verify

    def _api_call(self, endpoint, method="GET", **kwargs) -> Any:

        endpoint_url = "{proto}://{host}/api/public/v1/{endpoint}".format(
            proto=self.proto, host=self.host, endpoint=endpoint
        )

        if method in ["PUT", "POST"]:
            request_args = dict(json=kwargs)
        else:
            request_args = dict(params=kwargs)
        r = requests.request(
            method,
            endpoint_url,
            headers=self.request_headers,
            verify=self.verify,
            allow_redirects=False,
            **request_args,
        )

        if not r.ok:
            raise RuntimeError(r.text)
        return r.json() if self.output_style == "json" else r.text

    def ping(self):
        return self._api_call("ping")

    def get_active_organization_id(self):
        return self._api_call("organization").get("id")

    def set_active_organization_id(self, organization_id):
        return self._api_call("organization", method="PUT", id=organization_id).get(
            "id"
        )

    def get_all_organizations(self):
        return self._api_call("organizations")

    def list_warehouses(self):
        return self._api_call("list_warehouses")

    def refresh_warehouse(self, warehouse_id):
        return self._api_call(f"warehouse/{warehouse_id}/refresh", method="PUT")

    def refresh_warehouse_tables(self, warehouse_id, table_full_names):
        if not table_full_names:
            raise RuntimeError("Must specify a list of full table names to sync")
        return self._api_call(
            f"warehouse/{warehouse_id}/refresh",
            method="PUT",
            table_full_names=table_full_names,
        )

    def refresh_warehouse_new_tables(self, warehouse_id):
        return self._api_call(f"warehouse/{warehouse_id}/refresh/new", method="PUT")

    def list_notification_channels(self):
        return self._api_call("list_notification_channels")

    def configured_tables(self, check_cadence_type=None, warehouse_id=None):
        return self._api_call(
            "configured_tables",
            check_cadence_type=check_cadence_type,
            warehouse_id=warehouse_id,
        )

    def get_table_information(self, warehouse_id=None, table_id=None, table_name=None):
        if (not table_id or not warehouse_id) and not table_name:
            raise RuntimeError(
                "Must specify either warehouse_id & table_id or table_name for get_table_information"
            )
        else:
            return self._api_call(
                "get_table_information",
                warehouse_id=warehouse_id,
                table_id=table_id,
                table_name=table_name,
            )

    def get_check_intervals(self, table_id=None, start=None, end=None):
        if not table_id:
            raise RuntimeError("Must specify a table_id for get_check_intervals")
        else:
            results = []
            page = 0
            paged_results = None
            while paged_results is None or len(paged_results) > 0:
                paged_results = self._api_call(
                    "get_check_intervals",
                    table_id=table_id,
                    start=start,
                    end=end,
                    page=page,
                )["intervals"]
                results.extend(paged_results)
                page = page + 1
            return results

    def get_checks_for_table(self, table_id):
        return self._api_call("get_checks_for_table", table_id=table_id)

    def run_checks(self, table_id, interval_id=None, check_ids=None):
        if check_ids:
            if not isinstance(check_ids, list) and not isinstance(check_ids, tuple):
                check_ids = [check_ids]
            check_ids = list(check_ids)  # Convert from Tuple
            return self._api_call(
                "run_checks",
                method="POST",
                table_id=table_id,
                interval_id=interval_id,
                check_ids=check_ids,
            )
        else:
            return self._api_call(
                "run_checks",
                method="POST",
                table_id=table_id,
                interval_id=interval_id,
            )

    def get_run_result(self, job_id):
        return self._api_call("get_run_result", run_checks_job_id=job_id)

    def get_run_result_triage_history(self, job_id):
        return self._api_call("get_run_result_triage_history", run_checks_job_id=job_id)

    def create_check(self, table_id, check_type, **params):
        return self._api_call(
            "create_check",
            table_id=table_id,
            check_type=check_type,
            method="POST",
            params=params,
        )

    def delete_check(self, table_id, check_id):
        return self._api_call(
            "delete_check",
            table_id=table_id,
            check_id=check_id,
            method="POST",
        )

    def clone_check(self, table_id, check_id, new_table_id):
        return self._api_call(
            "clone_check",
            table_id=table_id,
            check_id=check_id,
            new_table_id=new_table_id,
            method="POST",
        )

    def configure_table(
        self,
        table_id,
        *,
        check_cadence_type=None,
        definition=None,
        time_column_type=None,
        notify_after=None,
        time_columns=None,
        fresh_after=None,
        interval_skip_expr=None,
        notification_channel_id=None,
        slack_users=None,
        check_cadence_run_at_duration=None,
    ):
        time_columns = [] if time_columns is None else time_columns
        slack_users = {} if slack_users is None else slack_users

        return self._api_call(
            "configure_table",
            table_id=table_id,
            method="POST",
            check_cadence_type=check_cadence_type,
            definition=definition,
            time_column_type=time_column_type,
            notify_after=notify_after,
            notification_channel_id=notification_channel_id,
            time_columns=time_columns,
            fresh_after=fresh_after,
            interval_skip_expr=interval_skip_expr,
            slack_users=slack_users,
            check_cadence_run_at_duration=check_cadence_run_at_duration,
        )


class CLI(Client):
    output_style = "text"

    def _warehouse_ids(self, warehouse_id: Optional[int] = None) -> Dict[int, str]:
        warehouse_ids = {
            int(wh["id"]): wh["name"] for wh in self.list_warehouses()["warehouses"]
        }
        if warehouse_id:
            warehouse_id = int(warehouse_id)
            if warehouse_id not in warehouse_ids:
                raise Exception(f"Warehouse with ID {warehouse_id} not found")
            return {warehouse_id: warehouse_ids[warehouse_id]}
        return warehouse_ids

    def _table_ids(self, warehouse_id: int, table_id: Optional[int] = None) -> Set[int]:
        table_ids = {
            int(t["table"]["id"])
            for t in self.configured_tables(warehouse_id=warehouse_id)
        }
        if table_id:
            table_id = int(table_id)
            if table_id not in table_ids:
                raise Exception(
                    f"Table ID {table_id} not found in warehouse with ID {warehouse_id}"
                )
            return {table_id}
        return table_ids

    def _retrieve_checks_for_table(self, table_id: int) -> Sequence[SavedObject]:
        result = self.get_checks_for_table(table_id=table_id)
        checks = []
        for raw_check in [c for c in result["checks"] if c["check_static_id"]]:
            checks.append(
                {
                    "params": (
                        raw_check["config"]["params"]
                        | {
                            "check_static_id": raw_check["check_static_id"],
                            "notification_channel": raw_check[
                                "additional_notification_channel_id"
                            ],
                        }
                    ),
                    "check": raw_check["config"]["check"],
                    "_metadata": self._format_metadata(raw_check)["_metadata"],
                }
            )
        return checks

    def _format_metadata(self, config: SavedObject) -> SavedObject:
        config.setdefault("_metadata", {})
        for key in {"created", "created_by", "last_edited_at", "last_edited_by"}:
            if key not in config:
                continue
            config["_metadata"][key] = config.pop(key)
        return config

    def _drop_metadata(self, config: SavedObject) -> SavedObject:
        return {k: v for k, v in config.items() if not k.startswith("_")}

    def _serialize_table_config(self, warehouse_id: int, table_id: int) -> SavedObject:
        table = self.get_table_information(warehouse_id=warehouse_id, table_id=table_id)
        table_config = table["config"]
        table_config.pop("table_id")
        table_config.setdefault("_metadata", {})
        table_config = self._format_metadata(table_config)
        table_config["_metadata"]["full_name"] = table["full_name"]
        return table_config

    def _can_update(self, existing: SavedObject, loading: SavedObject) -> bool:
        def _get_last_edited_at(obj: SavedObject) -> Optional[datetime]:
            ts = obj.get("_metadata", {}).get("last_edited_at")
            if not ts:
                return None
            return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")

        existing_dt = _get_last_edited_at(existing)
        loading_dt = _get_last_edited_at(loading)
        if not existing_dt or not loading_dt:
            return True
        return existing_dt <= loading_dt

    def _load_table_config(
        self, warehouse_id: int, table_id: int, config: SavedObject, force: bool
    ) -> int:
        table_config = self._drop_metadata(config)
        existing_table = self._serialize_table_config(
            warehouse_id=warehouse_id, table_id=table_id
        )
        if self._drop_metadata(existing_table) == table_config:
            return 0
        if not (force or self._can_update(existing_table, config)):
            print(
                f"Skipping stale config for table {config['_metadata']['full_name']}"
                f" (warehouse {warehouse_id}, table {table_id})"
            )
            return 0
        print(
            f"Configuring table {config['_metadata']['full_name']}"
            f" (warehouse {warehouse_id}, table {table_id})"
        )
        self.configure_table(table_id=table_id, **table_config)
        return 1

    def _serialize_checks(
        self, warehouse_id: int, table_id: int
    ) -> Sequence[SavedObject]:
        return self._retrieve_checks_for_table(table_id=table_id)

    def _load_checks(
        self,
        warehouse_id: int,
        table_id: int,
        checks: Sequence[SavedObject],
        force: bool,
    ) -> int:
        if not checks:
            return 0
        existing_checks = {
            c["params"]["check_static_id"]: c
            for c in self._retrieve_checks_for_table(table_id=table_id)
        }
        checks_count = 0
        for check in checks:
            check_config = self._drop_metadata(check)
            static_id = check_config["params"]["check_static_id"]
            if self._drop_metadata(existing_checks[static_id]) == check_config:
                # No changes
                continue
            if not (force or self._can_update(existing_checks[static_id], check)):
                print(
                    f"Skipping stale config for check {static_id}"
                    f" in warehouse {warehouse_id} and table {table_id}"
                )
                return 0
            self.create_check(table_id, check_config["check"], **check_config["params"])
            print(
                f"Loading check {static_id}"
                f" in warehouse {warehouse_id} and table {table_id}"
            )
            checks_count += 1
        return checks_count

    def save_config(
        self,
        filename: str,
        warehouse_id: Optional[int] = None,
        table_id: Optional[int] = None,
    ) -> None:
        self.output_style = "json"
        encoder = Encoder(filename)
        warehouses = self._warehouse_ids(warehouse_id=warehouse_id)
        data_by_warehouse_by_table = defaultdict(dict)
        tables_count = 0
        for wh_id in warehouses.keys():
            wh_id_key = f"warehouse_{wh_id}"
            table_ids = self._table_ids(warehouse_id=wh_id, table_id=table_id)
            for tbl_id in table_ids:
                tbl_id_key = f"table_{tbl_id}"
                table_objects = {
                    k: v
                    for k, v in {
                        "configuration": self._serialize_table_config(wh_id, tbl_id),
                        "quality_checks": self._serialize_checks(wh_id, tbl_id),
                    }.items()
                    if v
                }
                if not table_objects:
                    continue
                data_by_warehouse_by_table[wh_id_key][tbl_id_key] = table_objects
                tables_count += 1
                print(
                    "Found table"
                    f" {table_objects['configuration']['_metadata']['full_name']}"
                    f" (warehouse {wh_id}, table {tbl_id})"
                )
            if wh_id_key in data_by_warehouse_by_table:
                data_by_warehouse_by_table[wh_id_key]["_metadata"] = {
                    "name": warehouses[wh_id]
                }
        encoder.save(data_by_warehouse_by_table)
        if tables_count:
            print(f"Saved {tables_count} tables")

    def load_config(
        self,
        filename: str,
        warehouse_id: Optional[int] = None,
        table_id: Optional[int] = None,
        force: bool = False,
    ) -> None:
        self.output_style = "json"
        encoder = Encoder(filename)
        data_by_warehouse_by_table = encoder.load()
        update_counts = defaultdict(int)
        for wh_id, wh_data in data_by_warehouse_by_table.items():
            wh_data = self._drop_metadata(wh_data)
            wh_id = int(wh_id.removeprefix("warehouse_"))
            if warehouse_id and wh_id != warehouse_id:
                continue
            for tbl_id, table_objects in wh_data.items():
                tbl_id = int(tbl_id.removeprefix("table_"))
                if table_id and tbl_id != table_id:
                    continue
                for key, func in {
                    "configuration": self._load_table_config,
                    "quality_checks": self._load_checks,
                }.items():
                    if key not in table_objects:
                        continue
                    count = func(wh_id, tbl_id, table_objects.get(key), force)
                    if count:
                        update_counts[key] += count
        if update_counts:
            for object_type, count in sorted(update_counts.items()):
                print(f"Table {object_type} changes: {count}")
        else:
            print("No changes to apply")


def main() -> None:
    fire.Fire(CLI, name="anomalo")


if __name__ == "__main__":
    main()
