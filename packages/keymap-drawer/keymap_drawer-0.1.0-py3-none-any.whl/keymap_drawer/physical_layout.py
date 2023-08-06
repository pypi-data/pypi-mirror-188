"""
Module containing classes pertaining to the physical layout of a keyboard,
i.e. a sequence of keys each represented by its coordinates, dimensions
and rotation.
"""
from abc import ABC
from functools import cached_property
from typing import Sequence, ClassVar, Literal

from pydantic import BaseModel, validator, root_validator

KEY_W = 59
KEY_H = 54
SPLIT_GAP = KEY_W / 2


class PhysicalKey(BaseModel):
    """Represents a physical key, in terms of its center coordinates, width, height and rotation."""

    x_pos: float
    y_pos: float
    width: float = KEY_W
    height: float = KEY_H
    rotation: float = 0


LayoutType = Literal["ortho", "raw"]


class PhysicalLayout(BaseModel, ABC):
    """Represents the physical layout of keys on the keyboard, as a sequence of keys."""

    keys: Sequence[PhysicalKey]
    ltype: ClassVar[LayoutType]

    class Config:  # pylint: disable=missing-class-docstring
        arbitrary_types_allowed = True
        keep_untouched = (cached_property,)

    def __len__(self) -> int:
        return len(self.keys)

    @cached_property
    def width(self) -> float:
        """Return overall width of layout."""
        return max(k.x_pos + k.width / 2 for k in self.keys)

    @cached_property
    def height(self) -> float:
        """Return overall height of layout."""
        return max(k.y_pos + k.height / 2 for k in self.keys)


def layout_factory(ltype: LayoutType, **kwargs) -> PhysicalLayout:
    """Create and return a physical layout as determined by the ltype argument."""
    match ltype:
        case "ortho":
            return OrthoLayout(**kwargs)
        case "raw":
            return RawLayout(**kwargs)
        case _:
            raise ValueError(f'Physical layout type "{ltype}" is not supported')


class RawLayout(PhysicalLayout):
    """
    Physical layout directly given by a sequence of maps containing center coordinates,
    width, height and optionally rotation of each key.
    """

    ltype: ClassVar[LayoutType] = "raw"

    @validator("keys", pre=True, each_item=True, check_fields=False)
    def parse_keys(cls, val):
        """Parse each item containing a mapping into a PhysicalKey object."""
        return PhysicalKey(**val)


class OrthoLayout(PhysicalLayout):
    """
    Physical layout representing an ortholinear keyboard, as specified by its number of
    rows, columns, thumb keys and whether it is split or not. If split, row/columnn number
    represents the size of one half. Thumb keys can only be used if split.
    """

    split: bool
    rows: int
    columns: int
    thumbs: int | Literal["MIT", "2x2u"] = 0
    ltype: ClassVar[LayoutType] = "ortho"

    @root_validator
    def check_thumbs(cls, vals):
        """Check that the number of thumb keys is specified correctly."""
        thumbs = vals["thumbs"]
        if thumbs:
            if isinstance(thumbs, int):
                assert thumbs <= vals["columns"], "Number of thumbs should not be greater than columns"
                assert vals["split"], "Cannot process non-split layout with thumb keys"
            else:
                assert not vals["split"], (
                    "Non-integer thumb specs (MIT/2x2u) can only be used with non-split layout"
                )
                assert thumbs in ("MIT", "2x2u"), (
                    'Only "MIT" or "2x2u" supported for "thumbs" for non-splits'
                )
                assert vals["columns"] % 2 == 0, (
                    "Cannot use MIT or 2x2u bottom row layout with odd number of columns"
                )
        return vals

    @root_validator(pre=True, skip_on_failure=True)
    def create_ortho_layout(cls, vals):
        """Create a list of PhysicalKeys from given ortho specifications."""
        nrows = vals["rows"]
        ncols = vals["columns"]
        thumbs = vals.get("thumbs", 0)
        keys = []

        def create_row(x: float, y: float, ncols: int = ncols) -> None:
            for _ in range(ncols):
                keys.append(PhysicalKey(x_pos=x + KEY_W / 2, y_pos=y + KEY_H / 2))
                x += KEY_W

        x, y = 0.0, 0.0
        for _ in range(nrows if not thumbs else nrows - 1):
            create_row(x, y)
            if vals["split"]:
                create_row(x + ncols * KEY_W + SPLIT_GAP, y)
            y += KEY_H

        if thumbs:
            y_offset = nrows * KEY_H
            if isinstance(thumbs, int):  # implies split
                create_row((ncols - thumbs) * KEY_W, y_offset, thumbs)
                create_row(ncols * KEY_W + SPLIT_GAP, y_offset, thumbs)
            else:  # implies non-split
                if thumbs == "MIT":
                    create_row(0.0, y_offset, ncols / 2 - 1)
                    create_row((ncols / 2 - 1) * KEY_W, y_offset, 1)
                    create_row(ncols / 2 * KEY_W, y_offset, ncols / 2 - 1)
                else:  # "2x2u"
                    create_row(0.0, y_offset, ncols / 2 - 2)
                    create_row((ncols / 2 - 2) * KEY_W, y_offset, 2)
                    create_row((ncols / 2 + 1) * KEY_W, y_offset, ncols / 2 - 2)

        return vals | {"keys": keys}
