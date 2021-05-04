import json
from os.path import dirname, join
from unittest.async_case import IsolatedAsyncioTestCase  # type: ignore
from unittest.mock import ANY, AsyncMock, MagicMock  # type: ignore

from dipdup.config import ContractConfig, OperationHandlerConfig, OperationHandlerTransactionPatternConfig, OperationIndexConfig
from dipdup.datasources.tzkt.cache import OperationCache, OperationGroup
from dipdup.datasources.tzkt.datasource import TzktDatasource
from dipdup.models import OperationData, State


class TzktOperationCacheTest(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.index_config = OperationIndexConfig(
            kind='operation',
            datasource='',
            contracts=[ContractConfig(address='KT1AFA2mwNUMNd4SsujE1YYp29vd8BZejyKW')],
            handlers=[
                OperationHandlerConfig(
                    callback='',
                    pattern=[
                        OperationHandlerTransactionPatternConfig(
                            type='transaction',
                            destination=ContractConfig(address='KT1AFA2mwNUMNd4SsujE1YYp29vd8BZejyKW'),
                            entrypoint='hDAO_batch',
                        )
                    ],
                )
            ],
        )
        self.index_config.state = MagicMock()
        self.index_config.state.save = AsyncMock()
        self.cache = OperationCache()
        await self.cache.add_index(self.index_config)

    async def test_add(self):
        with open(join(dirname(__file__), 'operations.json')) as file:
            operations_message = json.load(file)

        operations = [TzktDatasource.convert_operation(operation_json) for operation_json in operations_message['data']]
        await self.cache.add(operations[0])
        await self.cache.add(operations[1])

        expected_key = OperationGroup(hash='opGZHyGpDt6c8x2mKexrhc8btiMkuyF1EHeL3hQvaNtTxsyzUGu', counter=7057537)

        self.assertEqual([expected_key], list(self.cache._operations.keys()))
        self.assertEqual(2, len(self.cache._operations[expected_key]))

    async def test_process(self):
        callback_mock = AsyncMock()

        with open(join(dirname(__file__), 'operations.json')) as file:
            operations_message = json.load(file)

        operations = [TzktDatasource.convert_operation(operation_json) for operation_json in operations_message['data']]
        for operation in operations:
            await self.cache.add(operation)

        await self.cache.process(callback_mock)

        self.assertIsInstance(callback_mock.await_args[0][0], OperationIndexConfig)
        self.assertEqual(
            callback_mock.await_args[0][1],
            OperationHandlerConfig(
                callback='',
                pattern=[
                    OperationHandlerTransactionPatternConfig(
                        type='transaction',
                        destination=ContractConfig(address='KT1AFA2mwNUMNd4SsujE1YYp29vd8BZejyKW'), entrypoint='hDAO_batch',
                    )
                ],
            ),
        )
        self.assertIsInstance(callback_mock.await_args[0][2], list)
        self.assertIsInstance(callback_mock.await_args[0][2][0], OperationData)
        self.assertIsInstance(callback_mock.await_args[0][3], list)
        self.assertIsInstance(callback_mock.await_args[0][3][0], OperationData)
