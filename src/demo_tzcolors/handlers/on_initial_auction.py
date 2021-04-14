from dipdup.models import HandlerContext, OperationContext

import demo_tzcolors.models as models

from demo_tzcolors.types.tzcolors_minter.parameter.initial_auction import InitialAuction
from demo_tzcolors.types.tzcolors_auction.parameter.create_auction import CreateAuction


async def on_initial_auction(
    ctx: HandlerContext,
    initial_auction: OperationContext[InitialAuction],
    create_auction: OperationContext[CreateAuction],
) -> None:

    holder, _ = await models.Address.get_or_create(address=create_auction.parameter.token_address)

    token = models.Token(
        id=create_auction.parameter.token_id,
        address=create_auction.parameter.token_address,
        amount=create_auction.parameter.token_amount,
        holder=holder,
        level=create_auction.data.level,
        timestamp=create_auction.data.timestamp,
    )
    await token.save()

    auction = models.Auction(
        id=create_auction.parameter.auction_id,
        token_address=token.address,
        token_id=token.id,
        token_amount=token.amount,
        bid_amount=create_auction.parameter.bid_amount,
        bidder=holder,
        seller=holder,
        end_timestamp=create_auction.parameter.end_timestamp,
        level=create_auction.data.level,
        timestamp=create_auction.data.timestamp,
    )
    await auction.save()

    bid = models.Bid(
        token_id=token.id,
        bidder=holder,
        level=create_auction.data.level,
        timestamp=create_auction.data.timestamp,
    )
    await bid.save()