from time import time

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import timekeeper as timek


def main():
    # Define the list to store the timekeepers to add them to the layout
    # and a list with the information necessary to build their callbacks
    # ---------------------V
    TIMEKEEPERS = []     # |
    TIMEK_CALLBACKS = [] # |
    #----------------------^

    app = dash.Dash(__name__)

    app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

    app.layout = html.Div(children=[
        html.H1(children='TimeKeeper Lib'),

        html.Div(children='''
            Press the buttons
        '''),
        # When making a hmtl. or dcc. component, wrap it with the make_with_timekeeper
        # with the corresponding trigger.
        # ---------------------------------------------------------------------V
        timek.make_with_timekeeper(html.Button('Btn1', id='btn1',),          # |
                                  'n_clicks', TIMEKEEPERS, TIMEK_CALLBACKS), # |
        html.Label(id='btn1_label', children='__empty__'),                   # |
        timek.make_with_timekeeper(html.Button('Btn2', id='btn2',),          # |
                                  'n_clicks', TIMEKEEPERS, TIMEK_CALLBACKS), # |
        html.Label(id='btn2_label', children='__empty__'),                   # |
        # ---------------------------------------------------------------------^
        html.Label(id='which_btn', children='No button pressed', style={'fontSize': 30, 'textAlign':'center'})
    ])
    # This section adds the hidden Divs of the timekeepers to the end of the layout
    # -----------------------------------V
    app.layout.children += TIMEKEEPERS # |
    # -----------------------------------^

    # Callbacks
    # This function creates the callbacks linking the original component with its
    # corresponding timekeeper.
    # --------------------------------------------------------V
    timek.build_timekeeper_callbacks(app, TIMEK_CALLBACKS)  # |
    # --------------------------------------------------------^

    # The timekeepers store their info (component id and timestamp) in the
    # 'children' property, where they are stored as strings separated by
    # the linebreak token.
    # ---------------------------------------------V
    @app.callback(                               # |
        Output('btn1_label', 'children'),        # |
        [Input('btn1_timekeeper', 'children')],  # |
        )                                        # |
    def show_time(data):                         # |
        og_id, time = data.split('\n')           # |
        return 'Btn1 timestamp is: ' + str(time) # |
    # ---------------------------------------------^

    @app.callback(
        Output('btn2_label', 'children'),
        [Input('btn2_timekeeper', 'children')],
        )
    def show_time(data):
        og_id, time = data.split('\n')
        return 'Btn2 timestamp is: ' + str(time)

    @app.callback(
        Output('which_btn', 'children'),
        [Input('btn1_timekeeper', 'children'),Input('btn2_timekeeper', 'children')]
    )
    def show_pressed_btn(timek1, timek2):
        # To get the id of the token that triggered the callback simply call
        # get_trigger_id() on all the timekeepers used as input. If data must
        # be passed from the original component, list it as State() in the callback.
        # -----------------------------------------------V
        trigger = timek.get_trigger_id(timek1, timek2) # |
        # -----------------------------------------------^
        if trigger == 'btn1':
            return "Button 1 was pressed"
        elif trigger == 'btn2':
            return "Button 2 was pressed"
        else:
            return


    app.run_server(debug=True)


if __name__ == '__main__':
    main()