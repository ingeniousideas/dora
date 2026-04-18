# Framework components
import dash
import dash_mantine_components as dmc
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd

# Framework components
from components.dag_table import reuse_table
from components.get_figure import fig_bar_multi, get_scatter_multi
from components.get_dataframes import figure_dataframe, raw_dataframe

# Reference for the applications table.
df_apps = raw_dataframe('apps')

# References for the deploy deployment figure.
df_deploy_figure = figure_dataframe("deploy")
figure_deploy = fig_bar_multi(df_deploy_figure, view="deploy")

# References for the deploy failure figure.
df_fail_figure = figure_dataframe("fail_graph")
figure_fail = fig_bar_multi(df_fail_figure, view="fail_graph")

# References for the deploy incidents figure.
df_incidents_basic = raw_dataframe('incidents')
figure_incidents = get_scatter_multi(df_incidents_basic, view="incident")

# References for the deploy lead time figure.
df_lead_basic = raw_dataframe('lead')
figure_lead = get_scatter_multi(df_lead_basic, view="lead")

dash.register_page(__name__, path='/', name='Home', order=0)

layout = dmc.Container(
	[
		# Container for DORA metrics figures.
		dmc.Container(
			[
				dmc.Title("DORA Dashboard", order=1),

				# Stack to create two layers for two Groups. These will each have two of the DORA metic figures with all apps shown.
				# https://www.dash-mantine-components.com/components/stack
				dmc.Stack(
					[
						# Two groups to contain two each of the DORA metric figures
						# https://www.dash-mantine-components.com/components/group
						dmc.Group(
							# props as configured above:
							justify="center",
							gap="md",
							grow=True,
							# other props...
							children=[
								# Graph to show deployment data.
								dcc.Graph(figure=figure_deploy),

								# dmc.Button("Awaiting Content", variant="default"),
								# Graph to show lead time data.
								dcc.Graph(figure = figure_lead),

							]
						),

						dmc.Group(
							# props as configured above:
							justify="center",
							gap="md",
							grow=True,
							# other props...
							children=[
									# Graph to show failure data.
								dcc.Graph(figure=figure_fail),

								# dmc.Button("Awaiting Content", variant="default"),
								# Graph to show lead time data.
								dcc.Graph(figure = figure_incidents),
							]
						),

					]
				),
			]
		),

		# Container just for Applications table view.
		dmc.Container(
			[
				reuse_table(df_apps, "Table of Applications"),
			]
		),
	]
)