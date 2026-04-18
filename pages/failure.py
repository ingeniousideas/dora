# Framework components
import dash
import dash_mantine_components as dmc
from dash import Dash, html, dcc, callback, Output, Input

# Framework components
from components.dag_table import reuse_table
from components.get_figure import fig_bar_single
from components.get_dataframes import figure_dataframe, raw_dataframe

dash.register_page(__name__, path='/failures', name='Failure Rate', order=4)

view = "fail"

# Get dataframes for figures and tables etc.
df_fail_basic = raw_dataframe('fail')
df_deploy_basic = raw_dataframe('deploy')

"""  Update dtaftame for use by the graph callback

	Reduce the number of columns for simplicity.
	Add new grouping column "month.
"""
# Reduce number of columns
df_deploy_graph = df_deploy_basic[["application_id","application_name","environment","status","deployed_at"]].copy()

# Add Month column for grouping.
df_deploy_graph["month"] = df_deploy_graph["deployed_at"].dt.month

# create grouped data frame
df_deploy_graph_groupby = df_deploy_graph.groupby([
	"application_id",
	"application_name",
	"month",
	"environment",
	"status"
	])["month"].count().reset_index(name="count")

layout = dmc.Container([

	# Page title.
	dmc.Title("Change Failure Rate"),

	dmc.Container(
		[
			# Smaller title for the figure, order=3 gives size of font.
			dmc.Title("Deployment Failures Over Time", order=3),

			# Dropdown to select the data.
			dmc.Select(
				label="Select app",
				placeholder="Select app",
				id="failure-dropdown-selection",
				value=df_deploy_graph_groupby.application_id.unique()[0],
				data=df_deploy_graph_groupby.application_id.unique()
			),

			dcc.Graph(id='failure-rate-monthly-graph',
			),

			# Filtered table callback output.
			html.Div(id='failure-table-content'),

		]
	),


])

# Callback to update monthly failure rate graph
@callback(
		Output('failure-rate-monthly-graph', 'figure'),
		Input('failure-dropdown-selection', 'value')
	)
def update_failure_rate_graph(value):

	fail_fig = fig_bar_single(df_deploy_graph, value, view)

	return fail_fig

@callback(
		Output('failure-table-content', 'children'),
		Input('failure-dropdown-selection', 'value')
)
def update_table(value):

	df_single_app = df_fail_basic.loc[df_fail_basic.application_id==value].copy()

	fail_table = reuse_table(df_single_app, "Table of Deployment Failures")

	return fail_table