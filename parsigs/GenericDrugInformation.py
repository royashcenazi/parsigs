import pandas as pd

class generic_drug:
    def __init__(self,brand_name=None,csv_path=None):
        if brand_name != None  and csv_path != None:
            try:
                data = pd.read_csv(csv_path)
                df = pd.DataFrame(data)
                filtered_data = df[df['Brand'] == brand_name]
                if not filtered_data.empty:
                    self.WID = filtered_data.iloc[0, 0]
                    self.ATCCode = filtered_data.iloc[0, 1]
                    self.drug_name = filtered_data.iloc[0, 2]
                    self.Synonym =  filtered_data.iloc[0, 3]
                    self.Brand_drug_name = filtered_data.iloc[0, 4]
            except Exception as e: 
                self = generic_drug()
        else:
            self.WID = 0
            self.ATCCode = None
            self.drug_name = None
            self.Synonym = None
            self.Brand_drug_name = None        