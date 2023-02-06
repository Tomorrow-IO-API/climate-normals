import pandas as pd
import plotly.io as pio
from ridgeplot import ridgeplot

locations = [
    ["40.730610, -73.935242", "New York, NY"],
    ["34.052235, -118.243683", "Los Angeles, CA"],
    ["41.875562, -87.624421","Chicago, IL"],
    ["29.760427, -95.369803", "Houston, TX"],
    ["33.448376, -112.074036", "Phoenix, AZ"]
]

fields = [
    'temperatureMin', 'temperatureMax', 'temperatureAvg',
    'dewPointMin', 'dewPointMax', 'dewPointAvg',
    'humidityMin', 'humidityMax', 'humidityAvg',
    'windSpeedMax', 'windSpeedMin', 'windSpeedAvg',
    'windSpeed100Max', 'windSpeed100Min', 'windSpeed100Avg',
    'windGustMin', 'windGustMax', 'windGustAvg',
    'cloudCoverMin', 'cloudCoverMax', 'cloudCoverAvg',
    'precipitationAccumulationSum', 'potentialEvaporationSum'
]

for location in locations:
    filename = f'{location[0]}.csv'
    df = pd.read_csv(filename)
    # Extract the month from the date column and add it as a new column
    df['month'] = pd.to_datetime(df['date'], format='%m-%d', errors='coerce').dt.strftime('%B')
    fields = df.columns.drop(['date', 'month'])
    for field in fields:
        samples = []
        column_names = []
        kde = []
        for month in df['month'].unique():
            df_temp = df[df['month'] == month]
            if len(df_temp[field].values) == 0:
                continue
            values = df_temp[field].values
            kde.append(min(values))
            kde.append(max(values))
            column_names.append(month)
            samples.append(df_temp[field].values)
        # Call the `ridgeplot()` helper with the values of the field for each month
        fig = ridgeplot(samples=samples,
                        labels=column_names,
                        # bandwidth=4,
                        # kde_points=kde,
                        colorscale="sunset",
                        colormode="mean-minmax",
                        coloralpha=0.6,
                        spacing=6/9
                        )
        # The returned Plotly `Figure` is still fully customizable
        fig.update_layout(title=f'Climate Normals at {location[1]}',
                          height=600, width=800,
                          plot_bgcolor="rgba(255, 255, 255, 0.0)",
                          xaxis_gridcolor="rgba(0, 0, 0, 0.1)",
                          yaxis_gridcolor="rgba(0, 0, 0, 0.1)",
                          yaxis_title='month',
                          xaxis_title=f'{field}')
        # show us the work!
        # fig.show()
        pio.write_image(fig, f'{location[1]}_{field}.png', format='png')

