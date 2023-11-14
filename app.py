from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def index():
    # Read data from the CSV file
    # For debugging
    plot_data = pd.read_csv('static/data.csv')
    tooltip_data = pd.read_csv('static/historical.csv')

    # For publishing
    # plot_data = pd.read_csv('/home/palaccarchive/pal-acc-archive/static/data.csv')
    # tooltip_data = pd.read_csv('/home/palaccarchive/pal-acc-archive/static/historical.csv')

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
        xaxis={'title': 'x-axis','fixedrange':True},
        yaxis={'title': 'y-axis','fixedrange':True},
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

@app.route('/sources')
def sources():
    return render_template('sources.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)