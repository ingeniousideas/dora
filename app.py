"""
Basic Appshell with header and  navbar that collapses on mobile.
Using reference from here: https://www.dash-mantine-components.com/components/appshell
"""

import dash
import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc

from components.dmc_sidebar import dmc_sidebar

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

layout = dmc.AppShell(
	[
		# Top header section of page layout.
		dmc.AppShellHeader(

			dmc.Group(
				[
					dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
					dmc.Title("DORA View"),
				],
				h="100%",
				px="md",
			),
		),

		# Navbar for the left for navigation.
		dmc.AppShellNavbar(
			id="navbar",
			children=[
				"Navbar",
				dmc_sidebar(),
			],
			p="md",
		),

		# Main section, where the individual pages and anything else will be rendered.
		dmc.AppShellMain(

			dash.page_container,

		),
	],

	# Layout formatting.
	header={"height": 60},
	padding="sm",
	navbar={
		"width": 220,
		"breakpoint": "sm",
		"collapsed": {"mobile": True},
	},
	id="appshell",
)

# Wraps all the above layout in Mantine to use compoents and give colour theme.
app.layout = dmc.MantineProvider(
	defaultColorScheme="dark",
	children=[layout]
	)

# Callback for the purposes of hiding the Navbar if the window size becomes too small, or for when it is viewed on a mobile.
@callback(
	Output("appshell", "navbar"),
	Input("burger", "opened"),
	State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
	navbar["collapsed"] = {"mobile": not opened}
	return navbar

# The app will be served by Gunicorn
server = app.server # Expose Flask server for Gunicorn

if __name__ == "__main__":
	app.run(debug=True, port=8050)