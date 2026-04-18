# Framework components
import dash
import pandas as pd
import dash_mantine_components as dmc
from dash import Dash, html, dcc, callback, Output, Input

# Custom components
from components.dag_table import reuse_table
from components.get_dataframes import figure_dataframe, raw_dataframe
from components.get_figure import get_scatter_single

dash.register_page(__name__, path='/restoration', name='Time to Restore', order=5)

view = "incident"

df_incidents_basic = raw_dataframe('incidents')

layout = dmc.Container([

	# Page title.
	dmc.Title("Time to Restore Service"),

	dmc.Container(
		[
			# Smaller title for the figure, order=3 gives size of font.
			dmc.Title("Monthly  Observed Incidents", order=3),

			# Dropdown to select the data.
			dmc.Select(
				label="Select app",
				placeholder="Select app",
				id="incidents-dropdown-selection",
				value=df_incidents_basic.application_id.unique()[0],
				data=df_incidents_basic.application_id.unique()
			),

			# Graph to show deployment data.
			dcc.Graph(id='incident-scatter-graph-content'),

			# Filtered table callback output.
			html.Div(id='incidents-table-content'),
		]
	),
])


# Callback function to return a figure as defined by the dropdown.
@callback(
		Output('incident-scatter-graph-content', 'figure'),
		Input('incidents-dropdown-selection', 'value')
)
def update_scatter_graph(value):

	fig_scat_single = get_scatter_single(df_incidents_basic, value, view)

	return fig_scat_single

@callback(
		Output('incidents-table-content', 'children'),
		Input('incidents-dropdown-selection', 'value')
)
def update_table(value):

	df_single_app = df_incidents_basic.loc[df_incidents_basic.application_id==value].copy()

	incidents_table = reuse_table(df_single_app, "Table of Observed Incidents")

	return reuse_table(df_single_app, "Table of Observed Incidents")