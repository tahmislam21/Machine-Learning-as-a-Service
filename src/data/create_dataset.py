import pandas as pd

def combine_tables(sales_train, calendar, calendar_events, items_weekly_sell_prices):
    """
    Combine the tables calendar, calendar_events, items_weekly_sell_prices and sales_train 

    Parameters
    ----------
    sales_train : pd.DataFrame
        Dataframe with the training sales data

    calendar : pd.DataFrame
        DataFrame with the calendar data
        
    calendar_events : pd.DataFrame
        DataFrame with the calendar_events data
         
    items_weekly_sell_prices : pd.DataFrame
        DataFrame with the weekly items sales prices

    Returns
    -------
    pd.DataFrame
        Returns the combined tables in a dataframe

    """
    # Joining the calendar and calendar_events tables
    combined_calendar = calendar.merge(calendar_events, how='left', on='date')
    print("Combining calendar and Calendar events")
    print(combined_calendar.info())

    # Turning wide format of sales table to long format
    long_sales_train = sales_train.melt(id_vars=['id','item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'], 
                                    var_name='day_num', 
                                    value_name='items_sold')
    
    # Combining the sales table with combined_calendar
    sales_train_calendar = long_sales_train.merge(combined_calendar, how='left', left_on='day_num', right_on='d')

    # Combining the combined sales_train_calendar data with items_weekly_sell_prices
    sales_calendar_prices = sales_train_calendar.merge(items_prices, how='inner', on=['store_id','item_id', 'wm_yr_wk'])
    print("Combining calendar, calendar events, weekly items prices and sales together")
    print(sales_calendar_prices.info())

    return sales_calendar_prices