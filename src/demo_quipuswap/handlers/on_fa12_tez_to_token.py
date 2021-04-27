from decimal import Decimal

import demo_quipuswap.models as models
from demo_quipuswap.types.fa12_token.parameter.transfer import Transfer as TransferParameter
from demo_quipuswap.types.fa12_token.storage import Storage as Fa12TokenStorage
from demo_quipuswap.types.quipu_fa12.parameter.tez_to_token_payment import TezToTokenPayment as TezToTokenPaymentParameter
from demo_quipuswap.types.quipu_fa12.storage import Storage as QuipuFa12Storage
from dipdup.models import HandlerContext, OperationContext


async def on_fa12_tez_to_token(
    ctx: HandlerContext,
    tez_to_token_payment: OperationContext[TezToTokenPaymentParameter, QuipuFa12Storage],
    transfer: OperationContext[TransferParameter, Fa12TokenStorage],
) -> None:
    if ctx.template_values is None:
        raise Exception('This index must be templated')

    decimals = int(ctx.template_values['decimals'])
    symbol = ctx.template_values['symbol']
    trader = tez_to_token_payment.data.sender_address

    min_token_quantity = Decimal(tez_to_token_payment.parameter.min_out) / (10 ** decimals)
    token_quantity = Decimal(transfer.parameter.value) / (10 ** decimals)
    tez_quantity = Decimal(tez_to_token_payment.data.amount) / (10 ** 6)
    assert min_token_quantity <= token_quantity, tez_to_token_payment.data.hash

    trade = models.Trade(
        symbol=symbol,
        trader=trader,
        side=models.TradeSide.BUY,
        quantity=token_quantity,
        price=token_quantity / tez_quantity,
        slippage=(1 - (min_token_quantity / token_quantity)).quantize(Decimal('0.000001')),
        level=transfer.data.level,
        timestamp=transfer.data.timestamp,
    )
    await trade.save()
