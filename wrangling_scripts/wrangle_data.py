import pandas as pd
import plotly.graph_objs as go
import requests
from collections import defaultdict
from pandas.io.json import json_normalize

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`
def get_data(indicator='SP.RUR.TOTL', countries='au;ca;us', years='2010:2020'):
    # get the World Bank GDP data for Brazil, China and the United States

    payload = {'format': 'json', 'per_page': '500', 'date':years}
    wb_url = ('http://api.worldbank.org/v2/countries/{}/indicators/{}'.format(countries, indicator))
    print('wb url: {}'.format(wb_url))
    r = requests.get(wb_url, params=payload)
    print('got results: r[0] {}'.format(r.json()[0]))

    # put the results in a dictionary where each country contains a list of all the x values and all the y values
    # this will make it easier to plot the results
    data = defaultdict(list)

    for entry in r.json()[1]:
        # check if country is already in dictionary. If so, append the new x and y values to the lists
        if data[entry['country']['value']]:
            data[entry['country']['value']][0].append(int(entry['date']))
            data[entry['country']['value']][1].append(float(entry['value']))
        else: # if country not in dictionary, then initialize the lists that will hold the x and y values
            data[entry['country']['value']] = [[],[]]

    df = json_normalize(r.json()[1])

    df = df[['country.value', 'date', 'value']]
    df.columns = ['country','year','value']
    df['year'] = df['year'].astype('int')
    # current year may have null values so drop nulls
    df = df.dropna()

    return df

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots arable land from 1990 to 2015 in top 10 economies
    # as a line chart
    graph_one = []
    df = get_data('SP.RUR.TOTL', 'au;ca;us', '2010:2020')
    df.columns = ['country','year','population']
    df.sort_values('population', ascending=False, inplace=True)
    countrylist = df.country.unique().tolist()

    for country in countrylist:
        x_val = df[df['country'] == country].year.tolist()
        y_val = df[df['country'] == country].population.tolist()
        graph_one.append(
            go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'lines',
                name = country
            )
        )

    layout_one = dict(title = 'Population Growth for Austrialia, Canada & US <br> between 2010 and 2020',
                xaxis = dict(title = 'year',
                    autotick=False, tick0=2010, dtick=2),
                yaxis = dict(title = 'population'),
                )

# second chart plots ararble land for 2015 as a bar chart
    graph_two = []
    df2 = get_data('SP.POP.GROW', 'au;ca;us', '2010:2020')
    df2.columns = ['country','year','population']
    df2.sort_values('population', ascending=False, inplace=True)
    countrylist2 = df2.country.unique().tolist()

    for country in countrylist2:
        x_val = df2[df2['country'] == country].year.tolist()
        y_val = df2[df2['country'] == country].population.tolist()
        graph_two.append(
            go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'lines',
                name = country
            )
        )

    layout_two = dict(title = 'Rural Population for Austrialia, Canada & US <br> between 2010 and 2020',
                xaxis = dict(title = 'year',
                    autotick=False, tick0=2010, dtick=2),
                yaxis = dict(title = 'population'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    df3 = get_data('SL.IND.EMPL.FE.ZS', 'au;ca;us', '2020')
    df3.columns = ['country','year','percent']
    df3.sort_values('percent', ascending=False, inplace=True)

    graph_three.append(
        go.Bar(
            x = df3.country.tolist(),
            y = df3.percent.tolist(),
            name = 'Country'
        )
    )

    layout_three = dict(title = 'Percent of females employed in industry <br>for Austrialia, Canada & US in 2020',
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = 'percent'),
                )

# fourth chart shows rural population vs arable land
    graph_four = []
    df4 = get_data('SL.SRV.EMPL.FE.ZS', 'au;ca;us', '2020')
    df4.columns = ['country','year','percent']
    df4.sort_values('percent', ascending=False, inplace=True)

    graph_four.append(
        go.Bar(
            x = df4.country.tolist(),
            y = df4.percent.tolist(),
            name = 'Country'
        )
    )

    layout_four = dict(title = 'Percent of females employed in service <br>for Austrialia, Canada & US in 2020',
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = 'percent'),
                )
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures
