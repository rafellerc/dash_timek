''' This small set of functions serves the purpose of allowing the callbacks to
find out which one of its inputs has triggered it, the default behaviour is explained
in https://github.com/plotly/dash/issues/59 :

Q: Since only a single Output is allowed in a callback, and all Inputs must feed into it,
    how can we determine which input is being triggered during a callback?

A: This isn't possible in Dash.

or https://community.plot.ly/t/which-component-triggered-the-callback/7366
or https://github.com/plotly/dash/issues/291
'''

from time import time

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


def build_timekeeper_callbacks(app, timek_callbacks):
    """ Builds the callbacks that update the time on each timekeeper
    as the trigger property is changed on the original component.
    The original component sends a message containing its id and
    the current time, separated by the linebreak token, that should be
    used on the other side to recover the data. 
    """
    for info in timek_callbacks:
        @app.callback(
        Output(info['input']+'_timekeeper', 'children'),
        [Input(info['input'], info['trigger'])],
        [State(info['input'], 'id')])
        def update_time(trigger, orig_id):
            # TODO check if the rounding in the string cast can 
            # affect the precision of the comparisons
            return orig_id + "\n" + str(time())

def make_with_timekeeper(o, trigger, timekeeper_list, timek_callbacks):
    """ Makes any given html or dcc object, and associates it with a timekeeper,
    which is a Hidden Div element containing the object's id and the timestamp
    of the last time its trigger property was changed.
    """
    timekeeper = html.Div(id=(o.id + '_timekeeper'),
                          style={'display':'none'},
                          children='TOIS')
    timekeeper_list.append(timekeeper)
    timek_callbacks.append({'input':o.id, 'trigger':trigger})
    return o

def get_trigger_id(*timeks):
    """ Gets the id of the component that triggered the callback,
    based on the timestamp of its timekeeper.
    """
    id_list = []
    time_list = []
    for timek in timeks:
        id_, time_value = timek.split('\n')
        id_list.append(id_)
        time_list.append(float(time_value))
    index = np.argmax(time_list)
    return id_list[index]
    