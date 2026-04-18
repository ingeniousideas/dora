# Framework components
import dash
import dash_mantine_components as dmc
import pandas as pd

# Framework components
from components.dag_table import reuse_table
from components.get_dataframes import raw_dataframe

dash.register_page(__name__, path='/apps', name='Applications', order=1)

# Reference for the applications table.
df_apps = raw_dataframe('apps')

layout = dmc.Container(
	[
		dmc.Title("Applications"),
		
		dmc.Container(
			[
				reuse_table(df_apps, "Table of Applications"),
			],
		),
	],
)