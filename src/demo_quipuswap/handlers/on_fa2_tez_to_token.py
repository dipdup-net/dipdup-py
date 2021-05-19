from decimal import Decimal

import demo_quipuswap.models as models
from demo_quipuswap.types.fa2_token.parameter.transfer import TransferParameter
from demo_quipuswap.types.fa2_token.storage import Fa2TokenStorage
from demo_quipuswap.types.quipu_fa2.parameter.tez_to_token_payment import TezToTokenPaymentParameter
from demo_quipuswap.types.quipu_fa2.storage import QuipuFa2Storage
from dipdup.models import OperationHandlerContext, TransactionContext


async def on_fa2_tez_to_token(
    ctx: OperationHandlerContext,
    tez_to_token_payment: TransactionContext[TezToTokenPaymentParameter, QuipuFa2Storage],
    transfer: TransactionContext[TransferParameter, Fa2TokenStorage],
) -> None:
    if ctx.template_values is None:
        raise Exception('This index must be templated')

    decimals = int(ctx.template_values['decimals'])
    symbol, _ = await models.Symbol.get_or_create(symbol=ctx.template_values['symbol'])
    trader, _ = await models.Trader.get_or_create(address=tez_to_token_payment.data.sender_address)

    min_token_quantity = Decimal(tez_to_token_payment.parameter.min_out) / (10 ** decimals)
    assert tez_to_token_payment.data.amount is not None
    token_quantity = sum(Decimal(tx.amount) for tx in transfer.parameter.__root__[0].txs) / (10 ** decimals)
    tez_quantity = Decimal(tez_to_token_payment.data.amount) / (10 ** 6)
    assert min_token_quantity <= token_quantity, tez_to_token_payment.data.hash

    trade = models.Trade(
        symbol=symbol,
        trader=trader,
        side=models.TradeSide.BUY,
        quantity=token_quantity,
        price=token_quantity / tez_quantity,
        slippage=1 - (min_token_quantity / token_quantity),
        level=transfer.data.level,
        timestamp=transfer.data.timestamp,
    )
    await trade.save()

    trader.trades_qty += 1  # type: ignore
    trader.trades_amount += tez_quantity  # type: ignore
    await trader.save()
