import demo_registrydao.models as models
from demo_registrydao.types.registry.parameter.propose import ProposeParameter
from demo_registrydao.types.registry.storage import RegistryStorage
from dipdup.context import BigMapHandlerContext, HandlerContext, OperationHandlerContext
from dipdup.models import BigMapData, BigMapDiff, OperationData, Origination, Transaction


async def on_propose(
    ctx: OperationHandlerContext,
    propose: Transaction[ProposeParameter, RegistryStorage],
) -> None:
    dao = await models.DAO.get(address=propose.data.target_address)
    await models.Proposal(dao=dao).save()
