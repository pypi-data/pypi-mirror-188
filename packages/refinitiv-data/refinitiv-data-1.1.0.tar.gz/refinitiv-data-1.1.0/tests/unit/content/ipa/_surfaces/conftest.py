from refinitiv.data.content.ipa.surfaces import eti
from tests.unit.conftest import load_json

x_axis = eti.Axis.STRIKE
y_axis = eti.Axis.DATE
one_surface_axis_params = [(x_axis, y_axis)]
one_surface_data_json = load_json(
    "./tests/unit/content/ipa/_surfaces/one_surface_data.json"
)

surfaces_axis_params = []
x_axis = eti.Axis.STRIKE
y_axis = eti.Axis.DATE
surfaces_axis_params.append((x_axis, y_axis))
x_axis = eti.Axis.DATE
y_axis = eti.Axis.STRIKE
surfaces_axis_params.append((x_axis, y_axis))
surfaces_data_json = load_json("./tests/unit/content/ipa/_surfaces/surfaces_data.json")
