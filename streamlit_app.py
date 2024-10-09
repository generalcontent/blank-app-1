import streamlit as st
import pandas as pd
import datetime
import os

DATA_FILE = 'purchases.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        data = pd.read_csv(DATA_FILE)
    else:
        data = pd.DataFrame(columns=[
            'Purchase ID', 'Item Name', 'Quantity', 'Price',
            'Purchase Date', 'Supplier', 'Category',
            'Payment Method', 'Notes', 'Other'
        ])
    return data

def save_data(data):
    data.to_csv(DATA_FILE, index=False)

def data_input_and_review():
    st.title('Purchase Entry and Review')

    data = load_data()

    with st.form(key='purchase_form'):
        st.header('Enter Purchase Details')
        purchase_id = st.text_input('Purchase ID')
        item_name = st.text_input('Item Name')
        quantity = st.number_input('Quantity', min_value=0)
        price = st.number_input('Price', min_value=0.0, format="%.2f")
        purchase_date = st.date_input('Purchase Date', value=datetime.date.today())
        supplier = st.text_input('Supplier')
        category = st.selectbox('Category', options=['Electronics', 'Groceries', 'Clothing', 'Other'])
        payment_method = st.selectbox('Payment Method', options=['Cash', 'Credit Card', 'Debit Card', 'Other'])
        notes = st.text_area('Notes')
        other = st.text_input('Other')

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        new_data = {
            'Purchase ID': purchase_id,
            'Item Name': item_name,
            'Quantity': quantity,
            'Price': price,
            'Purchase Date': purchase_date,
            'Supplier': supplier,
            'Category': category,
            'Payment Method': payment_method,
            'Notes': notes,
            'Other': other
        }
        # Convert new_data to a DataFrame and concatenate it with the existing data
        new_data_df = pd.DataFrame([new_data])
        data = pd.concat([data, new_data_df], ignore_index=True)
        save_data(data)
        st.success('Purchase details saved!')

    st.header('Past Purchases')

    if not data.empty:
        st.dataframe(data)

        st.subheader('Edit Purchase Details')
        selected_purchase = st.selectbox(
            'Select Purchase ID to Edit',
            options=data['Purchase ID'].unique()
        )

        if selected_purchase:
            purchase_to_edit = data[data['Purchase ID'] == selected_purchase].iloc[0]

            with st.form(key='edit_form'):
                st.write('Editing Purchase ID:', selected_purchase)
                item_name_edit = st.text_input('Item Name', value=purchase_to_edit['Item Name'])
                quantity_edit = st.number_input('Quantity', min_value=0, value=int(purchase_to_edit['Quantity']))
                price_edit = st.number_input('Price', min_value=0.0, format="%.2f", value=float(purchase_to_edit['Price']))
                purchase_date_edit = st.date_input('Purchase Date', value=pd.to_datetime(purchase_to_edit['Purchase Date']))
                supplier_edit = st.text_input('Supplier', value=purchase_to_edit['Supplier'])
                category_edit = st.selectbox(
                    'Category',
                    options=['Electronics', 'Groceries', 'Clothing', 'Other'],
                    index=['Electronics', 'Groceries', 'Clothing', 'Other'].index(purchase_to_edit['Category'])
                )
                payment_method_edit = st.selectbox(
                    'Payment Method',
                    options=['Cash', 'Credit Card', 'Debit Card', 'Other'],
                    index=['Cash', 'Credit Card', 'Debit Card', 'Other'].index(purchase_to_edit['Payment Method'])
                )
                notes_edit = st.text_area('Notes', value=purchase_to_edit['Notes'])
                other_edit = st.text_input('Other', value=purchase_to_edit['Other'])

                save_edit_button = st.form_submit_button(label='Save Changes')

            if save_edit_button:
                data.loc[data['Purchase ID'] == selected_purchase, 'Item Name'] = item_name_edit
                data.loc[data['Purchase ID'] == selected_purchase, 'Quantity'] = quantity_edit
                data.loc[data['Purchase ID'] == selected_purchase, 'Price'] = price_edit
                data.loc[data['Purchase ID'] == selected_purchase, 'Purchase Date'] = purchase_date_edit
                data.loc[data['Purchase ID'] == selected_purchase, 'Supplier'] = supplier_edit
                data.loc[data['Purchase ID'] == selected_purchase, 'Category'] = category_edit
                data.loc[data['Purchase ID'] == selected_purchase, 'Payment Method'] = payment_method_edit
                data.loc[data['Purchase ID'] == selected_purchase, 'Notes'] = notes_edit
                data.loc[data['Purchase ID'] == selected_purchase, 'Other'] = other_edit

                save_data(data)
                st.success('Purchase details updated!')
    else:
        st.write('No purchases yet.')

def summary_figures():
    st.title('Summary Figures')

    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        password = st.text_input('Enter Password', type='password')
        if st.button('Login'):
            if password == 'yourpassword':  # Replace 'yourpassword' with your actual password
                st.session_state['authenticated'] = True
                st.success('You are logged in')
            else:
                st.error('Incorrect password')
    else:
        data = load_data()

        if data.empty:
            st.write('No data to display.')
        else:
            total_purchases = len(data)
            total_value = data['Price'].sum()
            average_value = data['Price'].mean()

            st.write('**Total Purchases:**', total_purchases)
            st.write('**Total Purchase Value:**', total_value)
            st.write('**Average Purchase Value:**', average_value)

            data['Purchase Date'] = pd.to_datetime(data['Purchase Date'])
            purchases_over_time = data.groupby('Purchase Date').size()

            st.line_chart(purchases_over_time)

        if st.button('Logout'):
            st.session_state['authenticated'] = False

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", ["Data Input and Review", "Summary Figures"])

    if selection == "Data Input and Review":
        data_input_and_review()
    elif selection == "Summary Figures":
        summary_figures()

if __name__ == '__main__':
    main()
