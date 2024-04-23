import pandas as pd
from pathlib import Path

class generic_drug:
    
    def __init__(self, brand_name=None,csv_path=None):
        self.WID= None
        self.ATCCode= None
        self.drug_name= None
        self.Synonym= None
        self.Brand_drug_name= None
        self.set_generic_drug(brand_name,csv_path)
    
    def set_generic_drug(self,brand_name,csv_path) -> None:
        if csv_path == None or brand_name == None:
            pass #Do nothing
        else:
            data = pd.read_csv(csv_path)
            df = pd.DataFrame(data)
            filtered_data = df[df['Brand'] == brand_name]
            if len(filtered_data) == 1: 
                self.WID = filtered_data.iloc[0, 0]
                self.ATCCode = filtered_data.iloc[0, 1]
                self.drug_name = filtered_data.iloc[0, 2]
                self.Synonym =  filtered_data.iloc[0, 3]
                self.Brand_drug_name = filtered_data.iloc[0, 4]