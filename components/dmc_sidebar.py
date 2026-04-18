import dash
import dash_mantine_components as dmc

def dmc_sidebar():
	return	dmc.ScrollArea(
		[
			dmc.NavLink(
				label=page["name"],
				href=page["path"],
				active="exact"
				)
				for page in dash.page_registry.values()
		],
		style={"height":"100%"}
	)