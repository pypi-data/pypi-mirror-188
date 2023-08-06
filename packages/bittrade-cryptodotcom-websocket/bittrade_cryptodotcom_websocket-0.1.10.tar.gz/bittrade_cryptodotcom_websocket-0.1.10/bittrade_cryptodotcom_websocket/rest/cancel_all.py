from typing import Literal
from ..connection import wait_for_response
from ..models import (
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    CryptodotcomRequestMessage,
)
from reactivex import Observable, operators, just, throw
from ..events import MethodName

from returns.curry import curry

from typing import Any, Callable, Optional
from ..connection import wait_for_response
from ..models import (
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    CryptodotcomRequestMessage,
    EnhancedWebsocketBehaviorSubject
)
from elm_framework_helpers.output import info_operator
from reactivex import Observable, operators, disposable, empty
from ..events import MethodName
from ccxt import cryptocom
from reactivex.scheduler import NewThreadScheduler

from logging import getLogger

logger = getLogger(__name__)


def wait_for_no_orders(
    messages: Observable[list[dict]],
):
    return messages.pipe(
        operators.filter(lambda x: bool(x)),
        operators.timeout(2.0),
        operators.catch(lambda *_: just(False)),
        operators.map(lambda _: True),
    )


def cancel_all_factory(
    response_messages: Observable[CryptodotcomResponseMessage], open_orders_messages: Observable[list[dict]] | None,  exchange: cryptocom, socket: EnhancedWebsocketBehaviorSubject
) -> Callable[
    [str, Literal['limit', 'trigger', 'all']], Observable[bool]
]:
    """Cancel all factory

    :param: response_messages: The feed of messages that receive response to requests (identified via their id)
    :param: feed_messages: The feed of user messages; IMPORTANT these must be subscribed to user/orders or the cancel all will not be detected and will timeout. If not provided, the cancel all will be called but no check of success is performed
    """
    def cancel_all(
        symbol: str,
        type: Literal['limit', 'trigger', 'all'],
    ):
        uppercase_type = (type or 'limit').upper()
        market_id = exchange.market(symbol)['id']
        
        def subscribe(observer, scheduler=None):
            ws = socket.value
            if open_orders_messages:
                recorded_messages = open_orders_messages.pipe(
                    operators.replay(),
                )
                sub = recorded_messages.connect(scheduler=NewThreadScheduler())
            else:
                logger.warning('Cancel order called; open orders feed not provided, no check will be performed')
                sub = disposable.Disposable()

            def check_should_wait(x: CryptodotcomResponseMessage) -> Observable[Any]:
                if open_orders_messages is None:
                    return empty()
                # 316 just means there was no active order, that's fine
                if x.code == 0:
                    return wait_for_no_orders(
                        recorded_messages
                    )
                if x.code == 316: 
                    return empty()
                return throw(Exception('Refused to cancel orders %s', x.result))

            return disposable.CompositeDisposable(
                sub,
                response_messages.pipe(
                    wait_for_response(
                        ws.send_message(
                            CryptodotcomRequestMessage(
                                MethodName.CANCEL_ALL, params={
                                    "instrument_name": market_id,
                                    "type": uppercase_type
                                }
                            )
                        ),
                        2.0,
                    ),
                    operators.flat_map(check_should_wait),
                ).subscribe(observer, scheduler=scheduler),
            )

        return Observable(subscribe)

    return cancel_all
