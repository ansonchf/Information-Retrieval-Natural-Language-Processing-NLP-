    import pandas as pd
    import datetime as dt
    import requests as request
    
    def make_request(request_params, request_uri):
        # Api Key
        apikey = "d1ae8a54ce6a4385a95dd45b842bbad9"
    
        # base url
        base_url = "http://newsapi.org/v2/"
    
        # headers
        headers = {"Content-Type": "Application/JSON", "Authorization": apikey}
    
        r = request.get(base_url + request_uri, headers=headers, params=request_params)
        return r.json()
    
    def get_everything(from_date, to_date, language, query, domains):
        return make_request({'language': language, 'from': from_date, 'to': to_date, 'q': query, 'domains': domains}, 'everything')
    
    def feed_df(columns, results):
        feed = {column: [] for column in columns}
        # insert values in dictionary
        for result in results:
            for column in columns:
                value = result[column].strip('\n') if result[column] is not None else None
                feed[column].append(value)
    
        return feed
  #%%      
    iterations = 100
    # from when to start the interrogation
    start_date = dt.datetime(2020, 3, 18, 0)
    # which language the results should be in
    language = 'en'
    # what are you looking for, accepts logical expressions
    query = '(Corbyn OR Labour OR Opposition OR Shadow)+Coronavirus'
    #source
    domains = 'bbc.co.uk, independent.co.uk',
    # dataframe columns
    columns = ['publishedAt', 'title']
    
    # set pandas dataframe columns
    df1 = pd.DataFrame(data={'publishedAt': [], 'title': []})
    
    # Interrogate iterations times the api
    # default result set is 20 to increase it uncomment ad adjust the value (max is 100)
    # request_params["pageSize"] = 100
    # in make_request function
    for i in range(0, iterations):
        # increase end date by 2 hours
        end_date = start_date + dt.timedelta(hours=4)
    
        # interrogate the desired api with the parameters defined above, an example below
        api_results = get_everything(start_date, end_date, language, query, domains)
    
        # check if request was accepted
        if api_results['status'] == 'ok':
            # add result to the dataframe
            df1 = df1.append(pd.DataFrame.from_dict(feed_df(columns, api_results['articles'])), ignore_index=True)
    
        # swap start_date with the end_date so to get the next 20 rtesults
        start_date = end_date
    
    # Choose the column 'title' only
    df1_1 = df1.iloc[:,1]
    # Convert dataframe to series
    s1 = pd.Series(df1_1)
    # Delete the duplicates indicated in the series
    s1_1 = s1.drop_duplicates()
    
    # Define the name of the new series without duplicated articles
    NData_CorbynPlus = s1_1
    # Convert the servise to list and export it to a txt file
    NData_CorbynPlus_list = NData_CorbynPlus.values.tolist()
    with open("NCorbynPlus.txt", "w",encoding="utf-8") as output:
        output.write(str(NData_CorbynPlus_list))
# %%
    # from when to start the interrogation
    start_date = dt.datetime(2020, 3, 18, 0)
    
    # Keywords that are selected for the research
    query = '(Corbyn OR Labour OR Opposition OR Shadow)-Coronavirus'

    # set pandas dataframe columns
    df2 = pd.DataFrame(data={'publishedAt': [], 'title': []})
    
    # in make_request function
    for i in range(0, iterations):
        # increase end date by 4 hours
        end_date = start_date + dt.timedelta(hours=4)
    
        # interrogate the desired api with the parameters defined above, an example below
        api_results = get_everything(start_date, end_date, language, query, domains)
    
        # check if request was accepted
        if api_results['status'] == 'ok':
            # add result to the dataframe
            df2 = df2.append(pd.DataFrame.from_dict(feed_df(columns, api_results['articles'])), ignore_index=True)
    
        # swap start_date with the end_date so to get the next 20 rtesults.
        start_date = end_date
        
   # Choose the column 'title' only
   df2_1 = df2.iloc[:,1]
   # Convert dataframe to series
   s2 = pd.Series(df2_1)
   # Delete the duplicates indicated in the series
   s2_1 = s2.drop_duplicates()
   
    # Define the name of the new series without duplicated articles
    NData_CorbynMinus = s2_1
    # Convert the servise to list and export it to a txt file
    NData_CorbynMinus_list = NData_CorbynMinus.values.tolist()
    with open("NCorbynMinus.txt", "w",encoding="utf-8") as output:
        output.write(str(NData_CorbynMinus_list))