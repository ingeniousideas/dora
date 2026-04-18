# Framework components
import dash
import dash_mantine_components as dmc
from dash import Dash, html, dcc, callback, Output, Input

# Custom components
from components.dag_table import reuse_table
from components.get_figure import fig_bar_single
from components.get_dataframes import figure_dataframe, raw_dataframe

dash.register_page(__name__, path='/deployments', name='Deployment Frequency', order=2)

view = "deploy"

# Load dataframes.
df_deploy_basic = raw_dataframe("deploy")
df_deploy_figure = figure_dataframe("deploy")

layout = dmc.Container([

	# Page title.
	dmc.Title("Deployment Frequency"),

	# Data displayed as figure.
	dmc.Container(
		[
			# Dropdown to select the data.
			dmc.Select(
				label="Select app",
				placeholder="Select app",
				id="deployments-dropdown-selection",
				value=df_deploy_figure.application_id.unique()[0],
				data=df_deploy_figure.application_id.unique()
			),

			# Smaller title for the figure, order=3 gives size of font.
			dmc.Title("Figure of Deployments Per Month", order=3),

			# Graph to show deployment data.
			dcc.Graph(id='deployments-graph-content'),

			# Filtered table callback output.
			html.Div(id='deployments-table-content'),

		],
	),
])

# Callback function to return a figure as defined by the dropdown.
@callback(
		Output('deployments-graph-content', 'figure'),
		Input('deployments-dropdown-selection', 'value')
)
def update_graph(value):

	deploy_fig = fig_bar_single(df_deploy_figure, value, view)

	return deploy_fig

# Callback functino to return table of rows for the specific app as selected.
@callback(
		Output('deployments-table-content', 'children'),
		Input('deployments-dropdown-selection', 'value')
)
def update_table(value):

	df_single_app = df_deploy_basic.loc[df_deploy_basic.application_id==value].copy()

	deploy_table = reuse_table(df_single_app, "Table of Application Feature Deployments")

	return deploy_table