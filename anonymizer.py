import pandas as pd
import random

def generalize_column(df, column):
    """Apply basic generalization/masking rules for known columns."""
    if column == 'Name':
        return df[column].apply(lambda x: f"Name_{x[0].upper()}***" if pd.notna(x) and len(x) > 0 else "Name_***")
    elif column == 'Age':
        return df[column].apply(lambda x: age_bucket(x))
    elif column == 'ZIP_Code':
        return df[column].astype(str).apply(lambda x: x[:3] + '**')
    elif column == 'City':
        return df[column].apply(lambda x: 'City_***')
    elif column == 'Phone':
        return df[column].astype(str).apply(lambda x: x[:5] + '*****')
    elif column == 'Email':
        return df[column].apply(lambda x: mask_email(x))
    elif column == 'Department':
        return df[column].apply(lambda x: 'Dept_***')
    elif column == 'Visit_Date':
        return pd.to_datetime(df[column], errors='coerce').dt.strftime('%Y-%m')
    else:
        return df[column]  # return as-is for Gender, Disease

def age_bucket(age):
    try:
        age = int(age)
        if age < 30:
            return '18-29'
        elif age < 50:
            return '30-49'
        else:
            return '50+'
    except:
        return 'Unknown'

def mask_email(email):
    try:
        user, domain = email.split('@')
        return 'xxxx@' + domain
    except:
        return 'xxxx@domain.com'

def apply_k_anonymity(df, selected_attributes, k):
    df_copy = df.copy()

    # Apply generalization only to selected attributes
    for col in selected_attributes:
        if col in df_copy.columns:
            df_copy[col] = generalize_column(df_copy, col)

    # Check and enforce K-anonymity by dropping rows that don’t meet the K condition
    grouped = df_copy.groupby(selected_attributes)
    valid_groups = [group for name, group in grouped if len(group) >= k]

    if not valid_groups:
        return pd.DataFrame(columns=df.columns)  # Return empty DataFrame if no groups are valid

    result_df = pd.concat(valid_groups).reset_index(drop=True)

    return result_df
