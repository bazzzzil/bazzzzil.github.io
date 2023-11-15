from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def index():
    # Read data from the CSV file
    # For debugging
    # plot_data = pd.read_csv('static/data.csv')
    # tooltip_data = pd.read_csv('static/historical.csv')

    # For publishing
    plot_data = pd.read_csv('/home/palaccarchive/pal-acc-archive/static/data.csv')
    tooltip_data = pd.read_csv('/home/palaccarchive/pal-acc-archive/static/historical.csv')

    fig = go.Figure(go.Scatter(
        x = plot_data["Date"],
        y = plot_data["Palestinian"],
        name = "Palestinian",
        mode = 'lines+markers',
        line=dict(color='red'),
        hovertemplate =
        'Date: %{x}<br>Palestinian Deaths: %{y}<br>Children Killed: %{customdata[0]}<br>Action: %{customdata[1]}<extra></extra>',
        customdata=tooltip_data[['Dead', 'Action']],
        showlegend = True))

    fig.add_trace(go.Scatter(
        x = plot_data["Date"],
        y = plot_data["Israeli"],
        name = "Israeli",
        mode = 'lines+markers',
        line=dict(color='blue'),
        hovertemplate = 'Israeli Deaths: %{y}<extra></extra>',
        showlegend = True))

    fig.update_layout(hovermode="x",
        autosize=True,
        title = "Cumulative Deaths Post Oct 7",
        margin=dict(l=0, r=0, t=75, b=0),
        xaxis={'fixedrange':True},
        yaxis={'fixedrange':True},
        legend=dict(
            orientation="h",  # Set the legend orientation to horizontal
            x=0,              # Adjust the x position
            y=1.1             # Adjust the y position
            )
        )

    # Convert the plot to HTML
    plot_html = fig.to_html(full_html=False)

    return render_template('index.html', plot_html=plot_html)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/context')
def context():
    # Read data from the CSV file
    # For debugging
    # isr_data = pd.read_csv('static/isr-deaths-since-2000.csv')
    # pal_data = pd.read_csv('static/pal-deaths-since-2000.csv')

    # For publishing
    isr_data = pd.read_csv('/home/palaccarchive/pal-acc-archive/static/isr-deaths-since-2000.csv')
    pal_data = pd.read_csv('/home/palaccarchive/pal-acc-archive/static/pal-deaths-since-2000.csv')

    isr_data['Date of death'] = pd.to_datetime(isr_data['Date of death'])
    pal_data['Date of death'] = pd.to_datetime(pal_data['Date of death'])

    isr_data['year'] = isr_data['Date of death'].dt.year
    isr_data_yoy = isr_data['year'].value_counts().sort_index()
    pal_data['year'] = pal_data['Date of death'].dt.year
    pal_data_yoy = pal_data['year'].value_counts().sort_index()

    trace1 = go.Bar(
        x=pal_data_yoy.values,
        y=pal_data_yoy.index,
        marker_color='red',
        textposition='auto',
        orientation='h',
        name=f'Palestinian Deaths',
        hovertemplate = 'Year: %{y}<br>Deaths: %{x}'
        )

    trace2 = go.Bar(
        x=isr_data_yoy.values,
        y=isr_data_yoy.index,
        marker_color='blue',
        textposition='auto',
        orientation='h',
        name=f'Israeli Deaths',
        hovertemplate = 'Year: %{y}<br>Deaths: %{x}'
        )
    
    # Plotting with Plotly
    fig = go.Figure([trace1, trace2])

    fig.update_layout(
        title='Comparison of Deaths per Year',
        autosize=True,
        margin=dict(l=0, r=0, t=60, b=70),
        xaxis={'title': "Deaths", 'fixedrange':True},
        yaxis={'title': "Year", 'fixedrange':True, 'tickmode':'array'},
        barmode='relative',
        bargap=0.1,  # Bars point away from each other
        legend=dict(orientation='h', x=-0.2, y=-0.15),
    )

    # Convert the plot to HTML
    context_plot = fig.to_html(full_html=False)

    return render_template('context.html', context_plot=context_plot)

@app.route('/sources')
def sources():
    return render_template('sources.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)