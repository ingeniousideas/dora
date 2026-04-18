import pandas as pd

class DataLoader:
	def __init__(self, file_path: str, date_columns: list[str], encoding: str = 'utf-8'):
		self.file_path = file_path
		self.date_columns = date_columns
		self.encoding = encoding
		self.df = self._load_data()

	def _load_data(self) -> pd.DataFrame:
		return pd.read_json(
			self.file_path,
			encoding=self.encoding,
			convert_dates=self.date_columns
		)

	def add_ema(self, value_column: str, span: int = 5):
		"""Optional: Add Exponential Moving Average column."""
		self.df["EMA"] = self.df[value_column].ewm(span=span, adjust=False).mean()
		return self.df

	def get_dataframe(self) -> pd.DataFrame:
		return self.df