from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def index():
    # Read data from the CSV file
    plot_data = pd.read_csv('static/data.csv')
    tooltip_data = pd.read_csv('static/historical.csv')

    # Create a line plot with two series using Plotly Express
    # fig = px.line(plot_data, x='Date', y=['Palestinian', 'Israeli'], title='Palestinian/Israeli Death Toll Post Oct. 7', markers=True)

    # fig.update_traces(
    #     hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Deaths: %{y}<br>Dead Kids: %{customdata[0]}<br>Action: %{customdata[1]}',
    #     customdata=tooltip_data[['Dead', 'Action']]
    # )

    fig = go.Figure(go.Scatter(
        x = plot_data["Date"],
        y = plot_data["Palestinian"],
        name = "Palestinian",
        mode = 'lines+markers',
        hovertemplate =
        'Date: %{x}<br>Palestinian Deaths: %{y}<br>Dead Kids: %{customdata[0]}<br>Action: %{customdata[1]}<extra></extra>',
        customdata=tooltip_data[['Dead', 'Action']],
        showlegend = True))

    fig.add_trace(go.Scatter(
        x = plot_data["Date"],
        y = plot_data["Israeli"],
        name = "Israeli",
        mode = 'lines+markers',
        hovertemplate = 'Israeli Deaths: %{y}<extra></extra>',
        showlegend = True))

    fig.update_layout(hovermode="x",
        title = "Palestinian/Israeli Death Toll Post Oct. 7",
        xaxis_title="Date",
        yaxis_title="Deaths (Cumulative)")

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
