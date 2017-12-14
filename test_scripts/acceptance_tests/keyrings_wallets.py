"""
Created on Nov 8, 2017

@author: khoi.ngo

Containing test script of test scenario 04: keyrings wallets.
"""
# !/usr/bin/env python3.6
import json
import os.path

from indy import signus

from libraries import common
from libraries import constant
from libraries.result import Status
from libraries.utils import exit_if_exception, perform
from test_scripts.test_scenario_base import TestScenarioBase


class KeyringsWallets(TestScenarioBase):

    async def execute_test_steps(self):
        # 1. Create and open pool Ledger
        self.steps.add_step("Create and open pool Ledger")
        returned_code = await perform(self.steps, common.prepare_pool_and_wallet, self.pool_name,
                                      self.wallet_name, self.pool_genesis_txn_file)

        self.pool_handle, self.wallet_handle = exit_if_exception(returned_code)

        # 2. verify wallet was created in .indy/wallet
        self.steps.add_step("Verify wallet was created in .indy/wallet")
        wallet_path = constant.work_dir + "/wallet/" + self.wallet_name
        result = os.path.exists(wallet_path)
        if result:
            self.steps.get_last_step().set_status(Status.PASSED)

        # 3. create DID to check the new wallet work well.
        self.steps.add_step("Create DID to check the new wallet work well")
        await perform(self.steps, signus.create_and_store_my_did,
                      self.wallet_handle, json.dumps({"seed": constant.seed_default_trustee}))


if __name__ == '__main__':
    KeyringsWallets().execute_scenario()
