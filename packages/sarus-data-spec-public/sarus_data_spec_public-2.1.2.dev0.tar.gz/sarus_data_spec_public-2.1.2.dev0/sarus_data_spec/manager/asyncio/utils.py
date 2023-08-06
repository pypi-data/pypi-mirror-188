import asyncio
import asyncio.events as events
import typing as t

T = t.TypeVar("T")


def sync(coro: t.Coroutine) -> t.Any:
    """This runs an async function synchronously,
    even within an already runnning event loop,
    despite the apparent impossibility
    to nest loops within the same thread"""
    reset_at_completion = True
    try:
        curr_loop = asyncio.get_running_loop()
    except RuntimeError:
        reset_at_completion = False
    new_loop = asyncio.new_event_loop()
    new_loop._check_running = lambda: None  # type:ignore
    # method monkey patched since it raises an error
    # if another loop exists
    result = new_loop.run_until_complete(coro)
    if reset_at_completion:
        # this method allows to set the curr loop
        # as running,standard method asyncio.set_event_loop
        # does not work
        events._set_running_loop(curr_loop)
    return result


def sync_iterator(
    async_iterator_coro: t.Coroutine,
) -> t.Iterator[t.Any]:
    """This methods returns an iterator from an async iterator coroutine.
    It first executes the coroutine to obtain an async generator.
    Then, generator method allows to execute one step at a time the
    anext method of the async generator.
    """

    async_gen = sync(async_iterator_coro)
    # The loop used to generate batches
    new_loop = asyncio.new_event_loop()
    new_loop._check_running = lambda: None  # type:ignore
    # method monkey patched since it raises an error
    # if another loop exists

    def generator() -> t.Iterator[T]:
        """This method creates an iterator. At each generator
        step, the current loop is taken and suspended and the
        anext method of the async generator is executed in
        another loop
        """
        keep_on = True
        while keep_on:
            reset_at_completion = True
            try:
                curr_loop = asyncio.get_running_loop()
            except RuntimeError:
                reset_at_completion = False
            try:
                batch = new_loop.run_until_complete(async_gen.__anext__())

            except StopAsyncIteration:
                keep_on = False
            except Exception as exception:
                raise exception
            else:
                if reset_at_completion:
                    # asyncio.set_event_loop(curr_loop) not working
                    events._set_running_loop(curr_loop)
                yield batch

    return generator()


async def async_iter(data_list: t.Collection[T]) -> t.AsyncIterator[T]:
    """Convert a collection into an AsyncIterator."""
    for data in data_list:
        yield data


async def decoupled_async_iter(
    source: t.AsyncIterator[T], buffer_size: int = 100
) -> t.AsyncIterator[T]:
    """Create a consumer/producer pattern using an asyncio.Queue."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=buffer_size)

    async def producer() -> None:
        async for x in source:
            await queue.put(x)
        await queue.put(None)  # producer finished

    # Launch the iteration of source iterator
    loop = asyncio.get_running_loop()
    loop.create_task(producer())

    while True:
        x = await queue.get()
        if x is None:
            queue.task_done()
            break
        queue.task_done()
        yield x
