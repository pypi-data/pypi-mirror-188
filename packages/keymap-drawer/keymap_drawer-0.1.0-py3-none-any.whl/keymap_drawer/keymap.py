"""
Module with classes that define the keymap representation, with multiple layers
containing key and combo specifications, paired with the physical keyboard layout.
"""
from itertools import chain
from typing import Literal, Sequence, Mapping, Union

from pydantic import BaseModel, validator, root_validator

from .physical_layout import layout_factory, PhysicalLayout


class LayoutKey(BaseModel):
    """
    Represents a binding in the keymap, which has a tap property by default and
    can optionally have a hold property, or be "held", be a "ghost" key, or be a combo.
    """

    tap: str
    hold: str = ""
    type: Literal[None, "held", "combo", "ghost"] = None

    @classmethod
    def from_key_spec(cls, key_spec: Union[str, "LayoutKey", None]) -> "LayoutKey":
        """Create LayoutKey from a string (for tap), a full LayoutKey or null (empty key)."""
        if key_spec is None:
            return cls(tap="")
        if isinstance(key_spec, str):
            return cls(tap=key_spec)
        return key_spec


class ComboSpec(BaseModel):
    """
    Represents a combo in the keymap, with the trigger position, activated binding (key)
    and layers that it is present on.
    """

    positions: Sequence[int]
    key: LayoutKey
    layers: Sequence[str] = []

    @validator("key", pre=True)
    def get_key(cls, val) -> LayoutKey:
        """Parse each key from its key spec."""
        return LayoutKey.from_key_spec(val)


class Layer(BaseModel):
    """Represents a layer with a sequence of bindings (keys) and combos belonging to that layer."""

    keys: Sequence[LayoutKey]
    combos: Sequence[ComboSpec] = []

    @validator("keys", pre=True)
    def parse_keys(cls, vals) -> Sequence[LayoutKey]:
        """Parse each key on layer from its key spec, flattening the spec if it contains sublists."""
        return [
            LayoutKey.from_key_spec(val)
            for val in chain.from_iterable(
                v if isinstance(v, Sequence) and not isinstance(v, str) else [v] for v in vals
            )
        ]


class KeymapData(BaseModel):
    """Represents all data pertaining to a keymap, including layers, combos and physical layout."""

    layout: PhysicalLayout
    layers: Mapping[str, Layer]
    combos: Sequence[ComboSpec] = []

    @validator("layout", pre=True)
    def create_layout(cls, val) -> PhysicalLayout:
        """Create layout with type given by ltype."""
        assert "ltype" in val, 'Specifying a layout type key "ltype" is mandatory under "layout"'
        print(val)
        return layout_factory(**val)

    @root_validator(skip_on_failure=True)
    def assign_combos_to_layers(cls, vals):
        """
        If combos are given at the root, assign them to layers specified for each,
        or to all layers if not specified.
        """
        for combo in vals["combos"]:
            for layer in combo.layers if combo.layers else vals["layers"]:
                vals["layers"][layer].combos.append(combo)
        return vals

    @root_validator(skip_on_failure=True)
    def check_combo_pos(cls, vals):
        """Validate combo positions are legitimate ones we can draw."""
        for layer in vals["layers"].values():
            for combo in layer.combos:
                assert len(combo.positions) == 2, "Cannot have more than two positions for combo"
                assert all(
                    pos < len(vals["layout"]) for pos in combo.positions
                ), "Combo positions exceed number of keys"
        return vals

    @root_validator(skip_on_failure=True)
    def check_dimensions(cls, vals):
        """Validate that physical layout and layers have the same number of keys."""
        for name, layer in vals["layers"].items():
            assert len(layer.keys) == len(
                vals["layout"]
            ), f"Number of keys do not match layout specification in layer {name}"
        return vals
