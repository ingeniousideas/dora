import pandas as pd
from pathlib import Path

def raw_dataframe(view) -> pd.DataFrame:

	BASE_DIR = Path(__file__).parent.parent

	if view == "apps":
		raw_file_path = BASE_DIR / 'data/applications.json'
		date_columns = ["deployed_at"]

	elif view == "deploy" or view == "fail_graph":
		raw_file_path = BASE_DIR / 'data/deployment_frequency.json'
		date_columns = ["deployed_at"]

	elif view == "lead":
		raw_file_path = BASE_DIR / 'data/change_lead_time.json'
		date_columns = ["committed_at", "deployed_at"]

	elif view == "fail":
		raw_file_path = BASE_DIR / 'data/change_fail.json'
		date_columns = ["detected_at"]

	elif view == "incidents":
		raw_file_path = BASE_DIR / 'data/incidents.json'
		date_columns = ["incident_start_time", "incident_end_time"]

	df_raw = pd.read_json(
		raw_file_path,
		encoding='utf-8',
		convert_dates=date_columns
		)

	return df_raw

def figure_dataframe(view) -> pd.DataFrame:
		
	df_basic = raw_dataframe(view)

	"""	Update dtaftame for use by the graph callback
			- Reduce the number of columns for simplicity.
			- Add new grouping column "month.
	"""

	if view == "deploy":
		figure_columns = ["application_id","application_name","environment","status","deployed_at"]

	elif view == "lead":
		figure_columns = []

	elif view == "fail":
		figure_columns = ["application_id","application_name","environment","status","deployed_at"]

	elif view == "fail_graph":
		figure_columns = ["application_id","application_name","environment","status","deployed_at"]

	elif view == "incidents":
		figure_columns = []

	# Reduce number of columns
	df_updated = df_basic[figure_columns].copy()

	# Add Month column for grouping.
	df_updated["month"] = df_updated["deployed_at"].dt.month

	if view == "fail_graph":

		return df_updated
	
	elif view == "deploy":
		# create grouped data frame
		df_figure = df_updated.groupby([
			"application_id",
			"month",
			])["month"].count().reset_index(name="count")

		return df_figure