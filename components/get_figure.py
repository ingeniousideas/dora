import plotly.express as px

def fig_bar_single(dataframe, app_id, view):

	if view == "deploy":

		# Specify filtered data frame
		df_fig_bar = dataframe[dataframe.application_id==app_id]

		# Set figure parameters
		title = "Total Monthly Deployments by Application"
		x_values = 'month'
		y_values = 'count'
		x_title = "Deployment Month"
		y_title = "Number of Deployments"
		bar_color = None
		color_map = None

	elif view == "fail":

		""" Apply specific ammendments to the dataframe for the fail graph
		"""
		# Filter deploy df to app id
		df_target = dataframe[dataframe['application_id']==app_id]

		# Calculate percentage of status by month
		df_status_grouped = df_target.groupby(['month', 'status']).agg({'status':'count'})
		df_status_percent = df_status_grouped.groupby(level=0).apply(
			lambda x: 100 * x / x.sum())

		# Fix the index (drop the duplicate month level)
		df_status_percent.index = df_status_percent.index.droplevel(1)

		# Rename the column to avoid conflict during reset_index
		df_status_percent = df_status_percent.rename(columns={'status':'percentage'})
		df_fig_bar = df_status_percent.reset_index()


		# Set figure parameters
		title = "Deployment Failure Rates by Month"
		x_values = 'month'
		y_values = 'percentage'
		x_title = "Failure Month"
		y_title = "Percentage (%) Outcomes"
		bar_color = "status"
		color_map = {
			"success":"#636EFA",
			"failed":"#EF553B"
			}

	""" Main function body to create the figure
	"""
	# Create figure
	fig_bar_single = px.bar(
		data_frame=df_fig_bar,
		title=title,
		x=x_values,
		y=y_values,
		color=bar_color,
		color_discrete_map = color_map,
	)

	# Upate the figure layout
	fig_bar_single.update_layout(legend_title_text="Legend")
	fig_bar_single.update_layout(barmode='stack')
	fig_bar_single.update_yaxes(title_text=y_title)
	fig_bar_single.update_xaxes(
		title_text=x_title,
		tickvals=list(range(1,13)),
		ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	)

	# Apply Plotly colour pallet
	fig_bar_single.update_layout(template="plotly_dark")

	return fig_bar_single

def fig_bar_multi(dataframe, view):

	if view == "deploy":

		df_fig_bar = dataframe

		# Set figure parameters
		title = "Total Monthly Deployments by Application"
		x_values = 'month'
		y_values = 'count'
		x_title = "Deployment Month"
		y_title = "Number of Deployments"
		bar_color = 'application_id'
		color_map = None

	elif view == "fail_graph":

		# Calculate percentage of status by month
		df_status_grouped = dataframe.groupby(['month', 'status']).agg({'status':'count'})
		df_status_percent = df_status_grouped.groupby(level=0).apply(
			lambda x: 100 * x / x.sum())

		# Fix the index (drop the duplicate month level)
		df_status_percent.index = df_status_percent.index.droplevel(1)

		# Rename the column to avoid conflict during reset_index
		df_status_percent = df_status_percent.rename(columns={'status':'percentage'})
		df_fig_bar = df_status_percent.reset_index()

		title = "Deployment Failure Rates by Month"
		x_values = 'month'
		y_values = 'percentage'
		x_title = "Failure Month"
		y_title = "Percentage (%) Outcomes"
		bar_color = "status"
		color_map = {
			"success":"#636EFA",
			"failed":"#EF553B"
			}

	fig_bar_multi = px.bar(
		data_frame=df_fig_bar,
		title=title,
		x=x_values,
		y=y_values,
		color=bar_color,
		color_discrete_map = color_map,
	)

	fig_bar_multi.update_layout(legend_title_text="Legend")
	fig_bar_multi.update_layout(barmode='stack')
	fig_bar_multi.update_yaxes(title_text=y_title)
	fig_bar_multi.update_xaxes(
		title_text=x_title,
		tickvals=list(range(1,13)),
		ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	)

	# Apply Plotly colour pallet
	fig_bar_multi.update_layout(template="plotly_dark")

	return fig_bar_multi

def get_scatter_single(dataframe, app_id, view):
	""" Return scatter figure for a single application id.

		Needed for:
			- Lead Time.
			- Time to Restore.

		This will require a parameter of the app_id.

		Optional Trendline and Moving Average plot.
	"""

	# Specify filtered data frame
	df_updated = dataframe[dataframe.application_id==app_id].copy()

	if view == "lead":

		df_updated.sort_values(by=["commit_time"], inplace=True)

		# Set figure parameters
		title = "Lead Time for Changes Scatter Plot"
		x_values = 'commit_time'
		y_values = 'lead_time_hours'
		x_title = "Commit Date"
		y_title = "Lead Time (hours)"
		scatter_color = "application_id"	

	elif view == "incident":

		df_updated.sort_values(by=["started_at"], inplace=True)

		# Set figure parameters
		title = "Time to Recover from Incidents"
		x_values = 'started_at'
		y_values = 'duration_hours'
		x_title = "Incident Date"
		y_title = "Resolution Time (hours)"
		scatter_color = "application_id"

	# https://stackoverflow.com/questions/74520782/plotly-express-overlay-two-line-graphs
	fig_scat_single = px.scatter(
		data_frame=df_updated,
		title=title,	# Label for the figure.
		x=x_values,							# Column for use on x-axis
		y=y_values,							# Column for use on y-axis
		color=scatter_color,					# Column for use on colour grouping
		trendline="ols",					# Add a trendline
		)

	fig_scat_single.update_layout(
		legend_title_text="Legend"
	)

	fig_scat_single.update_yaxes(
		title_text=y_title
	)

	fig_scat_single.update_xaxes(
		title_text=x_title
	)

	# View speicifc post figure creation updates
	if view == "lead":

		# Add trace of a line for EMA
		fig_lead_ema_trace = px.line(
			data_frame=df_updated,
			title="Lead Time for Changes with EMA Line Plot",	# Label for the figure.
			x="commit_time",							# Column for use on x-axis
			y="EMA",							# Column for use on y-axis
			color="application_id",					# Column for use on color grouping
			)

		# Combine the two figures
		fig_scat_single.add_traces(
			list(fig_lead_ema_trace.select_traces())
		)

		# Customize legend labels
		fig_scat_single.data[0].name = f'Lead times'
		# fig_lead_scat_trace.data[1].name = 'Trendline' # This doesn't work. Likely because it's part of the scatter trace.
		fig_scat_single.data[2].name = 'Lead Time EMA'

		fig_scat_single.data[2].line.color = '#00cc96'    # EMA line (green)

	elif view == "incident":

		# Customize legend labels
		fig_scat_single.data[0].name = f'Resolution Times'  # Scatter points

	# Manually set colors from the plotly_dark palette
	# Assuming trace order: [0] scatter points, [1] trendline, [2] EMA
	fig_scat_single.data[0].marker.color = '#636efa'  # Scatter points (purple)
	fig_scat_single.data[1].line.color = '#ef553b'    # Trendline (red)
	
	# Apply Plotly colour pallet
	fig_scat_single.update_layout(template="plotly_dark")

	return fig_scat_single

def get_scatter_multi(dataframe, view):
	""" Return scatter figure for all appliations.

		This will require a parameter of the app_id.

		Optional Trendline and Moving Average plot
	"""
	if view == "lead":

		dataframe.sort_values(by=["commit_time"], inplace=True)

		# Set figure parameters
		title = "Lead Time for Changes Scatter Plot"
		x_values = 'commit_time'
		y_values = 'lead_time_hours'
		x_title = "Commit Date"
		y_title = "Lead Time (hours)"
		scatter_color = "application_id"

	elif view == "incident":

		dataframe.sort_values(by=["started_at"], inplace=True)

		# Set figure parameters
		title = "Time to Recover from Incidents"
		x_values = 'started_at'
		y_values = 'duration_hours'
		x_title = "Incident Date"
		y_title = "Resolution Time (hours)"
		scatter_color = "application_id"


	# https://stackoverflow.com/questions/74520782/plotly-express-overlay-two-line-graphs
	fig_scat_multi = px.scatter(
		data_frame=dataframe,
		title=title,	# Label for the figure.
		x=x_values,							# Column for use on x-axis
		y=y_values,							# Column for use on y-axis
		color=scatter_color,					# Column for use on colour grouping
		trendline="ols",					# Add a trendline
		)

	fig_scat_multi.update_layout(legend_title_text="Legend")
	fig_scat_multi.update_yaxes(title_text=y_title)
	fig_scat_multi.update_xaxes(title_text=x_title)
	
	# Apply Plotly colour pallet
	fig_scat_multi.update_layout(template="plotly_dark")

	return fig_scat_multi