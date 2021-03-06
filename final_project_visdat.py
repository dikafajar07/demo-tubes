import pandas as pd
import numpy as np

from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show, curdoc
from bokeh.models import ColumnDataSource, HoverTool, GroupFilter,CDSView, DateRangeSlider, CustomJS,Dropdown
from bokeh.layouts import row, column, gridplot, layout
from bokeh.models.widgets import Tabs, Panel, Slider, Select, CheckboxGroup
from bokeh.resources import INLINE

from datetime import date


data = pd.read_csv("data/WHO-COVID-19-global-data.csv", parse_dates=['Date_reported'])

data = data[["Date_reported", 'Country', 'New_cases', 'Cumulative_cases','New_deaths','Cumulative_deaths']]
data = data.rename(columns={'Date_reported': 'Date'})

output_notebook(resources=INLINE)

kasbar2 = (data[(data['Country'] == 'Italy') | (data['Country'] == 'India') | (data['Country'] == 'Indonesia')]
               .loc[:, ['Date', 'Country', 'New_cases','Cumulative_cases','New_deaths','Cumulative_deaths']]
               .sort_values(['Date']))

# Membuat file yang dioutputkan
output_file('KasusBaruCov-19.html', 
            title='New Case Covid-19 in Italy and India')

# Mengisolasi data jakarta_data dan jabar_data
it_data2 = kasbar[kasbar['Country'] == 'Italy']
ind_data2 = kasbar[kasbar['Country'] == 'India']
ina_data2 = kasbar[kasbar['Country'] == 'Indonesia']

# Membuat ColumnDataSource objek untuk setiap team
it_cds2 = ColumnDataSource(it_data2)
ind_cds2 = ColumnDataSource(ind_data2)
ina_cds2 = ColumnDataSource(ina_data2)

# Specify the selection tools to be made available
select_tools = ['box_select', 'lasso_select', 'poly_select', 'reset', 'wheel_zoom','box_zoom']


#membuat date slider
date_range_slider = DateRangeSlider(value=(date(2020, 1, 3), date(2022, 1, 18)),
                                    start=date(2020, 1, 3), end=date(2022, 1, 18))
date_range_slider.js_on_change("value", CustomJS(code="""
    console.log('date_range_slider: value=' + this.value, this.toString())
"""))

# Isolasi data data2
it_data2 = kasbar2[kasbar2['Country']=='Italy']
ind_data2 = kasbar2[kasbar2['Country'] == 'India']
ina_data2 = kasbar2[kasbar2['Country'] == 'Indonesia']

# Membuat ColumnDataSource objek
it_cds2 = ColumnDataSource(it_data2)
ind_cds2 = ColumnDataSource(ind_data2)
ina_cds2 = ColumnDataSource(ina_data2)


frames = [ind_data2, it_data2, ina_data2]
datasource = pd.concat(frames)
data_Source = ColumnDataSource(datasource)

# Membuat view untuk setiap data
India_view = CDSView(source=data_Source,
                      filters=[GroupFilter(column_name='Country', 
                                           group='India')])

Ina_view = CDSView(source=data_Source,
                      filters=[GroupFilter(column_name='Country', 
                                           group='Indonesia')])

Italy_view = CDSView(source=data_Source,
                      filters=[GroupFilter(column_name='Country', 
                                           group='Italy')])

common_India_kwargs = {
    'view': India_view,
    'legend_label': 'India'
}
common_Indonesia_kwargs = {
    'view': Ina_view,
    'legend_label': 'Indonesia'
}
common_Italy_kwargs = {
    'view': Italy_view,
    'legend_label': 'Italy'
}

# File yang dioutputkan
output_file('NewCase.html',
            title='Plot kasus baru di Indonesia, India dan Italy')

# Create and configure the figure
fig = figure(x_axis_type='datetime',
             plot_height=600, plot_width=800,
             title='Kasus Baru Covid-19 di India, Indonesia dan Italy (Klik label untuk menyembunyikan)',
             x_axis_label='Date', y_axis_label='New Cases',
             toolbar_location='right', tools=select_tools)

fig.circle(x='Date',
           y='New_cases',
           source=data_Source,
           color='red',
           selection_color='deepskyblue',
           nonselection_color='lightgray',
           nonselection_alpha=0.3, muted_alpha=0, **common_India_kwargs)

fig.circle(x='Date',
           y='New_cases',
           source=data_Source,
           color='blue',
           selection_color='deepskyblue',
           nonselection_color='lightgray',
           nonselection_alpha=0.3, muted_alpha=0, **common_Italy_kwargs)

fig.circle(x='Date',
           y='New_cases',
           source=data_Source,
           color='green',
           selection_color='deepskyblue',
           nonselection_color='lightgray',
           nonselection_alpha=0.3, muted_alpha=0, **common_Indonesia_kwargs)

tooltips = [
            ('Country', '@Country'),
            ('New Cases','@New_cases'),
            ('Cumulative Cases', '@Cumulative_cases'),
            ('New Deaths', '@New_deaths'),
            ('Cumulative Deaths','@Cumulative_deaths'),
           ]

fig.add_tools(HoverTool(tooltips=tooltips))
fig.legend.location = 'top_left'
fig.legend.click_policy = 'hide'
fig.legend.click_policy = 'mute'

# perlihatkan slider
date_range_slider.js_link("value", fig.x_range, "start", attr_selector=0)
date_range_slider.js_link("value", fig.x_range, "end", attr_selector=1)

# show grafik 
layout = layout([date_range_slider], [fig])
show(layout)
curdoc().add_root(layout)
