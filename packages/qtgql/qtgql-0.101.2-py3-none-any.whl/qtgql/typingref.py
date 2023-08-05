from typing import Any, Optional, Type, Union, get_args, get_origin

from attrs import define


def is_optional(field) -> bool:
    return get_origin(field) is Union and type(None) in get_args(field)


class UnsetType:
    __instance: Optional["UnsetType"] = None

    def __new__(cls: Type["UnsetType"]) -> "UnsetType":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        return cls.__instance

    def __str__(self):
        return ""

    def __repr__(self) -> str:  # pragma: no cover
        return "UNSET"

    def __bool__(self):
        return False


UNSET: Any = UnsetType()


@define
class TypeHinter:
    type: Any  # noqa: A003
    of_type: tuple["TypeHinter", ...] = ()

    @classmethod
    def from_string(cls, tp: str, ns: dict) -> "TypeHinter":
        from typing import List, Union, Dict, Optional, Any, Type, get_type_hints  # noqa

        ns = ns.copy()
        ns.update(locals())

        def tmp(t: tp):  # type: ignore
            ...

        annotation = get_type_hints(tmp, localns=ns, globalns=globals())["t"]

        return cls.from_annotations(annotation)

    @classmethod
    def from_annotations(cls, tp: Any) -> "TypeHinter":
        if args := get_args(tp):
            new_args: list[TypeHinter] = []
            for arg in args:
                new_args.append(TypeHinter.from_annotations(arg))
            return TypeHinter(type=get_origin(tp), of_type=tuple(new_args))  # type: ignore
        return TypeHinter(type=tp)

    def as_annotation(self, object_map: Optional[dict[str, Any]] = None) -> Any:
        if self.type is str:
            return self.type
        # eval forward refs
        if isinstance(self.type, str):
            assert object_map, "can't evaluate forward refs without object_map."
            self.type = object_map[self.type]

        if builder := getattr(
            self.type, "__class_getitem__", getattr(self.type, "__getitem__", None)
        ):
            if self.type is Union:
                return builder(tuple(arg.as_annotation(object_map) for arg in self.of_type))
            return builder(self.of_type[0].as_annotation(object_map))
        return self.type
