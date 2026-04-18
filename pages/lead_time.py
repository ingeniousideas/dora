# Framework components
import dash
import dash_mantine_components as dmc
from dash import Dash, html, dcc, callback, Output, Input

# Framework components
from components.dag_table import reuse_table
from components.get_dataframes import figure_dataframe, raw_dataframe
from components.get_figure import get_scatter_single

dash.register_page(__name__, path='/lead_time', name='Lead Time for Changes', order=3)

view = "lead"

df_lead_basic = raw_dataframe('lead')

""" Update dataframe for use by the graph callback

	Add Exponential Moving Average (EMA) column for trend.
"""
# Add Exponential Moving Average (EMA) column
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html
df_lead_basic["EMA"] = df_lead_basic["lead_time_hours"].ewm(span=5, adjust=False).mean()

layout = dmc.Container([

	# Page title.
	dmc.Title("Lead Time for Changes"),

	dmc.Container(
		[
			# Title for the page.
			dmc.Title("Figure of Change Lead Times", order=3),

			# Dropdown to select the data.
			dmc.Select(
				label="Select app",
				placeholder="Select app",
				id="lead-time-dropdown-selection",
				value=df_lead_basic.application_id.unique()[0],
				data=df_lead_basic.application_id.unique()
			),

			# Graph to show deployment data.
			dcc.Graph(id='lead-scatter-graph-content'),

			# Filtered table callback output.
			html.Div(id='lead-time-table-content'),

		],
	)
])


# Callback function to return a figure as defined by the dropdown.
@callback(
		Output('lead-scatter-graph-content', 'figure'),
		Input('lead-time-dropdown-selection', 'value')
)
def update_scatter_graph(value):

	fig_scat_single = get_scatter_single(df_lead_basic, value, view)

	return fig_scat_single

@callback(
		Output('lead-time-table-content', 'children'),
		Input('lead-time-dropdown-selection', 'value')
)
def update_table(value):

	df_single_app = df_lead_basic.loc[df_lead_basic.application_id==value].copy()

	lead_table = reuse_table(df_single_app, "Table of Commits and Lead Times")

	return lead_table
