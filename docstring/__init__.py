from docstring.copy_func import copy_func


def docstring(**kwrd_params):
    """
    Generate automatic docstring for the class with a decorator.

    :returns: decorator
    """

    def decorator(self):
        kwrd_params['tag'] = self.doc_cls.Index.name
        if self.__name__.endswith('SelectedResource'):
            kwrd_params['docstring'] = 'selected'
        else:
            kwrd_params['docstring'] = 'base'
        kwrd_params['schema'] = self.schema_cls.__name__
        method = kwrd_params['method']
        base_mth = getattr(self, f'on_base_{method}')
        mth = getattr(self, f'on_{method}', None)
        if not callable(mth):
            setattr(self, f'on_{method}', copy_func(base_mth, f'on_{method}'))
            mth = getattr(self, f'on_{method}', None)
        with open(f'./docstring/{kwrd_params.get("docstring")}/{method}.docstring', 'r') as file:
            mth.__doc__ = file.read().format(**kwrd_params)
        setattr(self, 'tag', {'name': kwrd_params.get('tag'),
                              'description': self.schema_cls.__doc__.strip(' \n')})
        return self
    return decorator
