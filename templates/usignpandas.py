
import pandas as pd
ef=pd.read_csv("C:\\Users\\sriva\\OneDrive\\Desktop\\medilearn\\Medicine_Details.csv")

new_data = {
            'Medicine Name': 'hi',
            'Composition':'hlo',
            'Uses': 'loo',
            'Side_effects': 'ppp',
            'Image URL': 'oooo',
            'Manufacturer':'popopop'
        }
ef=ef._append(new_data,ignore_index=True)
kk=ef.to_csv("C:\\Users\\sriva\\OneDrive\\Desktop\\medilearn\\Medicine_Details.csv",index=False)
if kk:
    print("no")
else:
    print("yes")


