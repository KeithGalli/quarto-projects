# This file generated by Quarto; do not edit by hand.
# shiny_mode: core

from __future__ import annotations

from pathlib import Path
from shiny import App, Inputs, Outputs, Session, ui

import pandas as pd
import matplotlib.pyplot as plt
from faicons import icon_svg
from shiny import render, reactive, ui

import itables
from itables import show, init_notebook_mode
import itables.options as opt

listings = pd.read_csv("listings.csv")
reviews = pd.read_csv("reviews.csv")

# reviews_joined = reviews.merge(listings, left_on='listing_id', right_on='id')

COLOR = '#6C757D'

# ========================================================================




def server(input: Inputs, output: Outputs, session: Session) -> None:
    reviews_joined = reviews.merge(listings, left_on='listing_id', right_on='id')

    ui.input_checkbox_group(
        "neighborhood",
        label = "Neighborhood",
        choices = list(reviews_joined['neighborhood'].unique()),
        selected= list(reviews_joined['neighborhood'].unique())
    )


    # ========================================================================

    ui.value_box(
        title = "Number of Listings",
        value = len(listings),
        icon = 'cross',
        color = "secondary"
    )

    # ========================================================================

    dict(
        icon = "house",
        color = "secondary",
        value = len(listings)
    )

    # ========================================================================

    dict(
        icon = "person",
        color = "secondary",
        value = len(reviews)
    )

    # ========================================================================

    dict(
        icon = "star",
        color = "secondary",
        value = f"{reviews['overall'].mean():.2f}"
    )

    # ========================================================================

    import plotly.express as px
    import calendar

    # Calculate the average for each month across all years
    monthly_averages = reviews_joined.groupby(['month', 'neighborhood'])['overall'].mean().reset_index()

    # Add month names
    monthly_averages['month_name'] = monthly_averages['month'].apply(lambda x: calendar.month_abbr[x])

    # Create the plotly figure
    fig = px.line(
        monthly_averages,
        x='month_name',
        y='overall',
        color='neighborhood',
        template='simple_white'
    )

    # Customize the figure
    fig.update_traces(
        line_width=6
    )

    fig.update_layout(
        showlegend=False,
    )

    # Set proper month order
    fig.update_xaxes(categoryorder='array', 
                     categoryarray=[calendar.month_abbr[i] for i in range(1, 13)])

    fig.show();

    # ========================================================================

    ax = reviews['overall'].value_counts().sort_index().plot(kind='bar', color=COLOR)
    ax.set_ylabel('Count', fontsize=18)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=16)
    ax.set_xlabel(None)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=16)
    plt.show();

    # ========================================================================

    import folium

    map_center = [listings['latitude'].mean(), listings['longitude'].mean()]
    m = folium.Map(
        location=map_center,
        zoom_start=12,
        height=500
    )

    for idx, row in listings.iterrows():
        tooltip = f"""
        <h5>Name: {row['name']} <br/>
        Rating: {row['review_scores_rating']} <br/>
        Cost: {row['price']}/night </h5>
        """
    
        _ = folium.Marker(
            [row['latitude'], row['longitude']], 
            tooltip=tooltip, 
            icon=folium.Icon(color='gray', icon='plus')
        ).add_to(m)

    m

    # ========================================================================

    opt.classes = ['display', 'cell-border', 'wrap-text']

    reviews_joined = reviews.merge(listings, left_on='listing_id', right_on='id')

    cols = {
        'name': 'Name', 
        'number_of_reviews': 'Reviews', 
        'review_scores_rating': 'Rating', 
        'review_scores_accuracy': 'Accuracy', 
        'review_scores_cleanliness': 'Cleanliness', 
        'review_scores_checkin': 'Checkin', 
        'review_scores_communication': 'Communication', 
        'review_scores_location': 'Location',  
        'price': 'Price'
    }

    reviews_joined = reviews_joined.rename(columns=cols)
    details = reviews_joined[cols.values()]
    listing_details = details.drop_duplicates(subset=['Name']).reset_index(drop=True)

    # ========================================================================

    @render.ui
    def text():
        return ui.layout_column_wrap(
        ui.value_box(
            title = "Number of Listings",
            value = len(listings),
            showcase = icon_svg('house'),
            theme = 'blue',
        ),
        ui.value_box(
            title = "Number of Listings",
            value = len(listings),
            showcase = icon_svg('house'),
            theme = '#AAAAAA',
        ))

    # ========================================================================

    @reactive.Calc
    def test():
        df = reviews_joined[reviews_joined['neighborhood'].isin(input.neighborhood())]
        return df


    @render.table
    def table():
        df = test()
        return df

    # ========================================================================

    itables.show(listing_details, maxBytes=0)

    # ========================================================================

    output_df = reviews_joined[['Name', 'date', 'comments', 'overall']].reset_index(drop=True)
    itables.show(output_df)

    # ========================================================================



    return None


_static_assets = ["shinyquarto_files","airbnb-dashboard/style.css"]
_static_assets = {"/" + sa: Path(__file__).parent / sa for sa in _static_assets}

app = App(
    Path(__file__).parent / "shinyquarto.html",
    server,
    static_assets=_static_assets,
)
