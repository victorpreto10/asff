import streamlit as st
import pandas as pd
from io import StringIO


# Função para processar o arquivo Excel
def process_file(uploaded_file):
    df = pd.read_excel(uploaded_file, header=1)
    if 'Price' in df.columns and df['Price'].dtype == 'object':
        df['Price'] = df['Price'].str.replace(',', '').astype(float)
    df['Operation'] = df['Qtde'].apply(lambda x: 'Buy' if x > 0 else 'Sell')
    if 'Price' in df.columns:
        df['Total Value'] = df['Price'] * df['Qtde']
        grouped_df = df.groupby(['Operation', 'Ticker Bloomberg']).apply(
            lambda x: pd.Series({
                'Qtde': x['Qtde'].sum(),
                'Weighted Price': (x['Total Value']).sum() / x['Qtde'].sum()
            })).reset_index()
    else:
        grouped_df = df.groupby(['Operation', 'Ticker Bloomberg']).agg({'Qtde': 'sum'}).reset_index()
    return grouped_df


# Função para comparar DataFrame com dados colados
def compare_dataframes(df1, pasted_data):
    TESTDATA = StringIO(pasted_data)
    df2 = pd.read_csv(TESTDATA, sep="\t", header=None)
    df2.columns = ['Operation', 'Ticker Bloomberg', 'Qtde', 'Price']
    return df1.equals(df2)


# Streamlit app
def main():
    st.title('BLISS pro GUGUZINHO')

    # Upload do arquivo Excel
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        processed_data = process_file(uploaded_file)
        st.write('Processed Data')
        st.dataframe(processed_data)

        # Área para colar os dados para comparação
        st.subheader('Paste Data Here for Comparison')
        pasted_data = st.text_area("Paste the data here", height=300)

        if st.button('Compare Data'):
            if compare_dataframes(processed_data, pasted_data):
                st.success('The datasets are identical.')
            else:
                st.error('There are differences between the datasets.')


if __name__ == "__main__":
    main()
