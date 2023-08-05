# Copyright 2022 macanudo527
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Withdrawal CSV Format: 日時 (timestamp), 数量 (amount), 手数料 (transaction fee), 合計 (total), ラベル (user-provided label), アドレス (address), Txid, ステータス (status)

import logging
from csv import reader
from datetime import datetime
from datetime import timezone as DatetimeTimezone
from typing import List, Optional

from pytz import timezone as PytzTimezone
from rp2.logger import create_logger

from dali.abstract_input_plugin import AbstractInputPlugin
from dali.abstract_transaction import AbstractTransaction
from dali.configuration import Keyword
from dali.intra_transaction import IntraTransaction


class InputPlugin(AbstractInputPlugin):

    __BITBANK: str = "Bitbank"
    __BITBANK_PLUGIN: str = "Bitbank_Supplemental_CSV"

    __TIMESTAMP_INDEX: int = 0
    __SENT_AMOUNT: int = 1
    __TRANSACTION_FEE: int = 2
    __TOTAL: int = 3
    __LABEL: int = 4
    __ADDRESS: int = 5
    __TX_ID: int = 6
    __STATUS: int = 7

    __DELIMITER: str = ","

    def __init__(
        self,
        account_holder: str,
        withdrawals_csv_file: str,
        withdrawals_code: str,
        native_fiat: Optional[str] = None,
    ) -> None:

        super().__init__(account_holder=account_holder, native_fiat=native_fiat)
        self.__withdrawals_csv_file: str = withdrawals_csv_file
        # Code of the asset being withdrawn since it is NOT included in the CSV file.
        self.__withdrawals_code: str = withdrawals_code
        self.__logger: logging.Logger = create_logger(f"{self.__BITBANK_PLUGIN}/{self.account_holder}")

    def load(self) -> List[AbstractTransaction]:
        return self.parse_withdrawals_file(self.__withdrawals_csv_file)

    def parse_withdrawals_file(self, file_path: str) -> List[AbstractTransaction]:
        result: List[AbstractTransaction] = []

        with open(file_path, encoding="utf-8") as csv_file:
            lines = reader(csv_file)

            header = next(lines)
            self.__logger.debug("Header: %s", header)
            for line in lines:
                raw_data: str = self.__DELIMITER.join(line)
                self.__logger.debug("Transaction: %s", raw_data)

                jst_timezone = PytzTimezone("Asia/Tokyo")
                jst_datetime: datetime = jst_timezone.localize(datetime.strptime(line[self.__TIMESTAMP_INDEX], "%Y/%m/%d %H:%M:%S"))
                utc_timestamp: str = jst_datetime.astimezone(DatetimeTimezone.utc).strftime("%Y-%m-%d %H:%M:%S%z")

                result.append(
                    IntraTransaction(
                        plugin=self.__BITBANK_PLUGIN,
                        unique_id=line[self.__TX_ID],
                        raw_data=raw_data,
                        timestamp=utc_timestamp,
                        asset=self.__withdrawals_code,
                        from_exchange=self.__BITBANK,
                        from_holder=self.account_holder,
                        to_exchange=Keyword.UNKNOWN.value,
                        to_holder=Keyword.UNKNOWN.value,
                        spot_price=Keyword.UNKNOWN.value,
                        crypto_sent=str(line[self.__TOTAL]),
                        crypto_received=Keyword.UNKNOWN.value,
                    )
                )

        return result
