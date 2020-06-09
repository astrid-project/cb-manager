import types


def docstring(**kwrd_params):
    """Generate automatic docstring for the class with a decorator.

    :returns: decorator
    """

    def copy_func(func, name=None):
        """Copy function with a new name.

        :param func: function to copy
        :param name: new name
        :returns: copied function
        """
        return types.FunctionType(func.__code__, func.__globals__, name or func.__name__,
                                  func.__defaults__, func.__closure__)

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
