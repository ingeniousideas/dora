import dash_ag_grid as dag
import dash_mantine_components as dmc

"""
	AGGrid component documentation: 			https://dash.plotly.com/dash-ag-grid
	For applying themes to AGGrid component: 	https://dash.plotly.com/dash-ag-grid/styling-themes
	DMC version of AG Grid:						https://www.dash-mantine-components.com/dash-ag-grid
"""

def reuse_table(table_dataframe, table_title):

	return dmc.Container(
		[
			dmc.Title(table_title, order=3), # order is size of text
			# simple grid for the application components
			dmc.Container(
				[
					# simple table for the application data
					dag.AgGrid(
						rowData=table_dataframe.to_dict("records"),
						columnDefs=[{"field": i} for i in table_dataframe.columns],
						className="ag-theme-alpine-dark"
					),
				],
			), # type: ignore

		],
		fluid=True
	)