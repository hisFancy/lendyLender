#getting libraries needed
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter, StrMethodFormatter, PercentFormatter
import streamlit as st

#Storing vars

#color palette dict
palette = {
    'lendable_green': '#35C187',
    'light_orange': '#F2CF5B',
    'light_gray': '#636363',
    'gray_blue': '#3C6682',
    'pale_red': '#E78587'
}

loansDataUrl = 'files/loans_data.csv'
transactionsDataUrl = 'files/transactions_data.csv'


#loading data
#loans
loans_df = pd.read_csv('files/loans_data.csv')
loans_df["begin_date"] = pd.to_datetime(loans_df["begin_date"], format='%m/%d/%y %H:%M')
loans_df["end_date"] = pd.to_datetime(loans_df["end_date"], format='%m/%d/%y %H:%M')
loans_df["tenor_months"] = ((loans_df["end_date"].dt.year)*12 + loans_df["end_date"].dt.month) - ((loans_df["begin_date"].dt.year)*12 + loans_df["begin_date"].dt.month)



#transaactions
transactions_df = pd.read_csv(transactionsDataUrl)
transactions_df["transaction_date"] = pd.to_datetime(transactions_df["transaction_date"], format='%m/%d/%y %H:%M')

#merging loans and transactions + data reduction
loans_transactions_df = pd.merge(loans_df, transactions_df, on="loan_id", how="left")
loans_transactions_df.drop(["currency_type", "interest_rate_period", "transaction_id"], axis=1, inplace=True)
loans_transactions_df = loans_transactions_df[["loan_id", "account_id", "asset", "principal", "begin_date", "end_date", "tenor_months", "interest_rate", "interest_type", "gross_book_value",  "transaction_date", "transaction_type", "transaction_amount"]]

loans_account_df = loans_df.copy()
loans_account_df = loans_account_df[['account_id', 'loan_id']]
# loans_account_df.groupby("account_id").size().reset_index(name='Count')
# loans_account_df

loan_count_per_account = loans_account_df.groupby('account_id')['loan_id'].nunique().reset_index()

# Count the number of accounts for each unique loan count
account_count_per_loan = loan_count_per_account.groupby('loan_id').size().reset_index(name='account_count')

plt.figure(figsize=(10, 6))
plt.bar(account_count_per_loan['loan_id'], account_count_per_loan['account_count'], color=palette['lendable_green'])

# Set title and labels
plt.title("Number of Loans per Account", fontsize=16, fontweight="bold")
plt.xlabel("Number of Loans")
plt.ylabel("Number of Accounts")

plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

sns.despine()
# Display the plot
import streamlit as st 

st.markdown("*Streamlit* is **really** ***dope***.")
st.pyplot()


loans_category_df = loans_df.groupby('asset').size().reset_index(name='Count')
loans_category_df["percentage"] = loans_category_df["Count"] / loans_category_df["Count"].sum()
loans_category_df = loans_category_df.sort_values(by="Count", ascending=False).reset_index(drop=True)
loans_category_df["cumulative_percentage"] = loans_category_df["percentage"].cumsum()

# Set Seaborn context for a more aesthetic appearance
sns.set_context("notebook")

# Create a figure and axis
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot bar chart for monthly revenue
sns.barplot(x='asset', y='Count', data=loans_category_df, color=palette['lendable_green'], ax=ax1, label='No. of loans')
ax1.set_xlabel('Asset')
ax1.set_ylabel('No. of loans')
ax1.tick_params('y', colors=palette['light_gray'])
ax1.set_xticklabels(loans_category_df['asset'], rotation=20, ha='right')
ax1.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot line chart for cumulative revenue
sns.lineplot(x='asset', y='cumulative_percentage', data=loans_category_df, color=palette['light_orange'], marker='o', ax=ax2, label='Cumulative %')
ax2.set_ylabel('Cumulative %')
ax2.tick_params('y', colors=palette['light_gray'])
ax2.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))

# Add legend
ax1.legend(loc='right', bbox_to_anchor=(1, 0.4))
ax2.legend(loc='right', bbox_to_anchor=(1, 0.5))

# Set title
plt.title('Loans by Asset', fontsize=16, fontweight="bold", y=1.05)

# Add data labels for bar chart
for p in ax1.patches:
    height = p.get_height()
    ax1.annotate(f"{height:,.0f}", (p.get_x() + p.get_width() / 2., height),
                ha="center", va="center", xytext=(0, 10), textcoords="offset points")

# Add data labels for line chart
for x, y, label in zip(loans_category_df["asset"], loans_category_df["cumulative_percentage"], loans_category_df["cumulative_percentage"]):
    ax2.annotate(f"{label*100:.1f}%", (x, y), textcoords="offset points", xytext=(0, 10), ha='right')

# Remove borders
ax2.set_frame_on(False)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_color('gray')
ax1.spines['bottom'].set_color('gray')
ax1.spines['left'].set_color('gray')

st.pyplot()
