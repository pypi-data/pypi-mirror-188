import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

from conftest import open_platform_session
from refinitiv.data.content import ipa


def convert_DateString_to_float(date_string_array):
    import datetime
    import matplotlib.dates as dates

    date_float_array = []
    for date_string in date_string_array:
        date_string = str(date_string)
        try:
            date_float = dates.date2num(
                datetime.datetime.strptime(date_string, "%Y-%m-%d")
            )
            date_float_array.append(date_float)
        except ValueError:
            date_float = dates.date2num(
                datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
            )
            date_float_array.append(date_float)
    return date_float_array


open_platform_session()

definition = ipa.surface_eti.Definition(
    underlying_definition=ipa.surface_eti.EtiSurfaceDefinition(
        instrument_code="BNPP.PA@RIC"
    ),
    surface_parameters=ipa.surface_eti.EtiCalculationParams(
        price_side=ipa.surface_eti.PriceSide.MID,
        volatility_model=ipa.surface_eti.VolatilityModel.SVI,
        x_axis=ipa.surface_eti.Axis.STRIKE,
        y_axis=ipa.surface_eti.Axis.DATE,
    ),
    surface_tag="1_MATRIX",
    surface_layout=ipa.surface_eti.SurfaceLayout(
        format=ipa.surface_eti.Format.MATRIX, y_point_count=10
    ),
)

res = definition.get_data()

definition = ipa.surfaces.Definition(
    universe=[
        ipa.surface_eti.Definition(
            underlying_definition=ipa.surface_eti.EtiSurfaceDefinition(
                instrument_code="BNPP.PA@RIC"
            ),
            surface_parameters=ipa.surface_eti.EtiCalculationParams(
                price_side=ipa.surface_eti.PriceSide.MID,
                volatility_model=ipa.surface_eti.VolatilityModel.SVI,
                x_axis=ipa.surface_eti.Axis.STRIKE,
                y_axis=ipa.surface_eti.Axis.DATE,
            ),
            surface_tag="1_MATRIX",
            surface_layout=ipa.surface_eti.SurfaceLayout(
                format=ipa.surface_eti.Format.MATRIX, y_point_count=10
            ),
        ),
        ipa.surface_eti.Definition(
            underlying_definition=ipa.surface_eti.EtiSurfaceDefinition(
                instrument_code="BNPP.PA@RIC"
            ),
            surface_parameters=ipa.surface_eti.EtiCalculationParams(
                price_side=ipa.surface_eti.PriceSide.MID,
                volatility_model=ipa.surface_eti.VolatilityModel.SVI,
                x_axis=ipa.surface_eti.Axis.DATE,
                y_axis=ipa.surface_eti.Axis.STRIKE,
            ),
            surface_tag="1_1",
            surface_layout=ipa.surface_eti.SurfaceLayout(
                format=ipa.surface_eti.Format.MATRIX, y_point_count=10
            ),
        ),
    ],
)
response = definition.get_data()
data = response.data
df = response.data.df
print(df)

surface = data.surfaces[0]

# VALUE ON AXIS
curve = surface.get_curve("25.35", ipa.surface_eti.Axis.X)
print("'25.35', X")
print(curve)

curve = surface.get_curve("2021-08-20", ipa.surface_eti.Axis.Y)
print("'2021-08-20', Y")
print(curve)

curve = surface.get_curve(53.1528001887883, ipa.surface_eti.Axis.Z)
print("53.1528001887883, Z")
print(curve)

point = surface.get_point(25.35, "2020-08-20")
print("'2020-08-20', 25.35")
print(point)

# VALUE NOT ON AXIS

curve = surface.get_curve("2021-08-25", ipa.surface_eti.Axis.Y)
print("'2021-08-25', Y")
print(curve)

curve = surface.get_curve("2021-08-30", ipa.surface_eti.Axis.Y)
print("'2021-08-30', Y")
print(curve)

curve = surface.get_curve("2021-09-15", ipa.surface_eti.Axis.Y)
print("'2021-09-15', Y")
print(curve)

curve = surface.get_curve(41, ipa.surface_eti.Axis.X)
print("41, X")
print(curve)

point = surface.get_point(26.45, "2020-08-25")
print("'2020-08-25', 26.45")
print(point)

surface = data.surfaces[1]

X = surface.x.astype(float)
Y, X = np.meshgrid(surface.y, surface.x)

ax = plt.axes(projection="3d")
ax.set_xlabel("moneyness")
ax.set_ylabel("time to expiry")
ax.set_zlabel("volatilities")

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
plt.show()
