# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class WebVizContinuousLegend(Component):
    """A WebVizContinuousLegend component.


Keyword arguments:

- colorName (string; required)

- colorTables (string | list; optional)

- cssLegendStyles (dict with strings as keys and values of type string; optional)

- horizontal (boolean; optional)

- max (number; required)

- min (number; required)

- title (string; optional)"""
    @_explicitize_args
    def __init__(self, title=Component.UNDEFINED, min=Component.REQUIRED, max=Component.REQUIRED, cssLegendStyles=Component.UNDEFINED, colorName=Component.REQUIRED, horizontal=Component.UNDEFINED, colorTables=Component.UNDEFINED, **kwargs):
        self._prop_names = ['colorName', 'colorTables', 'cssLegendStyles', 'horizontal', 'max', 'min', 'title']
        self._type = 'WebVizContinuousLegend'
        self._namespace = 'webviz_subsurface_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['colorName', 'colorTables', 'cssLegendStyles', 'horizontal', 'max', 'min', 'title']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['colorName', 'max', 'min']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(WebVizContinuousLegend, self).__init__(**args)
