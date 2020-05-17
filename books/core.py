import plotly.graph_objects as go
from plotly.offline import plot as offplot
from django.templatetags.static import static


def get_book_progress_plot(points):
    """Return <div> of Plotly plot area for book reading progress."""

    scatter_x, scatter_y = zip(*points)

    plot_trace = go.Line(x=scatter_x,
                         y=scatter_y,
                         mode='lines+markers',
                         marker={
                             "size": 10,
                             "color": 'rgba(0, 0, 200, 1.0)',
                         },
                         hoverinfo='x+y')

    figure = go.Figure(data=[plot_trace])

    config = {
        "displayModeBar": True,
        "modeBarButtons": [
            ["resetScale2d"],
            ["zoom2d"],
            ["lasso2d"],
            ["pan2d"],
        ],
        "scrollZoom": True,
    }

    return offplot(figure, output_type="div", include_plotlyjs=False, config=config)
