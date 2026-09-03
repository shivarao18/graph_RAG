import pandas as pd
from sqlalchemy import create_engine
import os

def init_db():
    # Mock Kaggle S&P 500 data
    data = {
        'Ticker': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META'],
        'Company': ['Apple Inc.', 'Microsoft Corp.', 'Alphabet Inc.', 'Amazon.com Inc.', 'Meta Platforms Inc.'],
        'Revenue_Billions': [383.28, 211.91, 307.39, 574.78, 134.90],
        'Sector': ['Technology', 'Technology', 'Communication Services', 'Consumer Cyclical', 'Communication Services']
    }
    
    df = pd.DataFrame(data)
    
    # Create SQLite database
    db_path = 'companies.db'
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Write to SQL
    print("Ingesting data into SQLite (companies.db)...")
    df.to_sql('companies', engine, if_exists='replace', index=False)
    print("Data ingestion complete. Table 'companies' created with the following data:")
    print(df)

if __name__ == "__main__":
    init_db()
