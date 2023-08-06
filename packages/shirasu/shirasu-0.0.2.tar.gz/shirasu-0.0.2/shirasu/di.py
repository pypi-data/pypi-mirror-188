import inspect
from typing import Any, Callable, Awaitable, TypeVar


T = TypeVar('T')


class DependencyError(Exception):
    """
    Base error for dependency injection errors.
    """

    def __init__(self, deps: list[str], prompt: str) -> None:
        super().__init__(f'{prompt}: {", ".join(deps)}')
        self.deps = deps


class UnknownDependencyError(DependencyError):
    """
    Dependency not found.
    """

    def __init__(self, deps: list[str]) -> None:
        super().__init__(deps, 'unknown dependencies')


class CircularDependencyError(DependencyError):
    """
    Circular dependency.
    """

    def __init__(self, deps: list[str]) -> None:
        super().__init__(deps, 'circular dependencies')


class InvalidDependencyError(DependencyError):
    """
    Invalid dependency, which means type mismatch.
    """

    def __init__(self, deps: list[str]) -> None:
        super().__init__(deps, 'wrong dependency types')


class DuplicateDependencyProviderError(DependencyError):
    """
    Duplicate provider.
    """

    def __init__(self, dep: str) -> None:
        super().__init__([dep], 'duplicate dependency provider')


class DependencyInjector:
    """
    Dependency injector based on annotations.
    Note: it does not support positional-only arguments.
    """

    def __init__(self) -> None:
        self._providers: dict[str, Callable[..., Awaitable[Any]]] = {}

    async def _inject_func_args(self, func: Callable[..., Awaitable[Any]], *inject_for: str) -> dict[str, Any]:
        params = inspect.signature(func).parameters

        # Check unknown dependencies.
        if unknown_deps := [dep for dep in params if dep not in self._providers]:
            raise UnknownDependencyError(unknown_deps)

        # Check circular dependencies.
        if circular_deps := [dep for dep in params if dep in inject_for]:
            raise CircularDependencyError(circular_deps)

        args = {
            dep: await self._apply(self._providers[dep], dep, *inject_for)
            for dep in params
        }

        # Check types of injected parameters.
        if invalid_deps := [dep for dep, param in params.items() if not isinstance(args[dep], param.annotation)]:
            raise InvalidDependencyError(invalid_deps)

        return args

    async def _apply(self, func: Callable[..., Awaitable[T]], *apply_for: str) -> T:
        injected_args = await self._inject_func_args(func, *apply_for)
        return await func(**injected_args)

    def inject(self, func: Callable[..., Awaitable[T]]) -> Callable[[], Awaitable[T]]:
        assert inspect.iscoroutinefunction(func), 'injected function must be async.'
        assert all(
            not isinstance(p.annotation, str)
            for p in inspect.signature(func).parameters.values()
        ), 'annotations of injected parameters cannot be string.'

        async def wrapper():
            return await self._apply(func)
        return wrapper

    def provide(self, name: str, func: Callable[..., Awaitable[T]], *, check_duplicate: bool = True) -> None:
        assert inspect.iscoroutinefunction(func), 'dependency provider must be async.'

        if check_duplicate and name in self._providers:
            raise DuplicateDependencyProviderError(name)

        self._providers[name] = func


di = DependencyInjector()
"""
The global dependency injector.
"""


def inject():
    """
    Injects function using decorator.
    :return: the decorator to inject function.
    """

    def deco(func: Callable[..., Awaitable[T]]) -> Callable[[], Awaitable[T]]:
        return di.inject(func)
    return deco


def provide(name: str, *, check_duplicate: bool = True) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """
    Registers provider using decorator.
    :return: the decorator to register provider.
    """

    def deco(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        di.provide(name, func, check_duplicate=check_duplicate)
        return func
    return deco
